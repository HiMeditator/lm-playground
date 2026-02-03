import asyncio
import os
import json
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
# from openai.types.chat import ChatCompletionUserMessageParam

class MCPClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.messages = [
            { "role": "system", "content": "You are Atri (Chinese: 亚托莉, Japanese: アトリ), the female protagonist of the visual novel ATRI -My Dear Moments-."}
        ]
        self.available_tools = []
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self.openai_compat = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        self.tot_usage = {
            "completion_tokens": 0,
            "prompt_tokens": 0,
            "cached_prompt_tokens": 0,
        }
        self.latest_token = 0

    async def connect_to_server(self, command: str, args: list[str]):
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=None,
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        self.available_tools = [
            {
                "type": "function", 
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            }
            for tool in response.tools
        ]
        # print("MCP Server Connected!")
        # print("[TOOLS]", json.dumps(self.available_tools, indent=2, ensure_ascii=False))

    async def process_query(self, model: str, query: str | None) -> str:
        if self.session is None:
            raise RuntimeError("Session not initialized. Please connect to the server first.")

        if query is not None:
            self.messages.append({"role": "user", "content": query})

        stream = self.openai_compat.chat.completions.create(
            model=model,
            messages=self.messages, # type: ignore
            tools=self.available_tools, # type: ignore
            stream=True,
            stream_options={"include_usage": True}
        )

        # Process response and handle tool calls
        content_deltas = []
        tool_calls_msg = None

        chunk: ChatCompletionChunk
        for chunk in stream:
            # print(chunk)
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta.tool_calls:
                    tool_call = delta.tool_calls[0]
                    if tool_calls_msg is None:
                        tool_calls_msg = {
                            "role": "assistant",
                            "tool_calls": [{
                                "id": tool_call.id,
                                "function": {
                                    "arguments": tool_call.function.arguments or "", # type: ignore
                                    "name": tool_call.function.name, # type: ignore
                                },
                                "type": "function"
                            }]
                        }
                        continue
                    if tool_call.function.arguments: # type: ignore
                        tool_calls_msg["tool_calls"][0]["function"]["arguments"] += tool_call.function.arguments # type: ignore
                elif delta.content:
                    content_deltas.append(delta.content)
                    print(delta.content, end="")
            elif chunk.usage:
                print()
                self.latest_token = chunk.usage.total_tokens or 0
                self.tot_usage["completion_tokens"] += chunk.usage.completion_tokens or 0
                self.tot_usage["prompt_tokens"] += chunk.usage.prompt_tokens or 0
                if chunk.usage.prompt_tokens_details:
                    self.tot_usage["cached_prompt_tokens"] += chunk.usage.prompt_tokens_details.cached_tokens or 0
            
        if tool_calls_msg is not None:
            arguments = tool_calls_msg["tool_calls"][0]["function"]["arguments"]
            if not arguments:
                arguments = {}
            else:
                arguments = json.loads(arguments)
            # print(f'[CALL]', tool_calls_msg["tool_calls"][0])
            result = await self.session.call_tool(
                tool_calls_msg["tool_calls"][0]["function"]["name"],
                arguments,
            )
            # print('[RESULT]', result)
            result_text = result.content[0].text # type: ignore
            self.messages.append(tool_calls_msg) # type: ignore
            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_calls_msg["tool_calls"][0]["id"], # type: ignore
                "content": result_text,
            })
            # print(self.messages)
            return await self.process_query(model, None)

        content = "".join(content_deltas)
        self.messages.append({"role": "assistant", "content": content})
        return content

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()



async def main():
    client = MCPClient(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DASHSCOPE_API_KEY") or "",
    )
    try:
        await client.connect_to_server(
            "uv",
            [
                "--directory",
                "D:\\Projects\\lm-playground",
                "run",
                "mcp-exp/src/atri-mcp/atri_mcp.py"
            ]
        )
        while True:
            print("========== ATRI Chat Agent v0.1.0 ==========")
            print("\tUse 'exit' or 'quit' to exit.")
            print("\tUse 'log' to print chat log.")
            print("\tUse 'usage' to show token usage.")
            query = input("ATRI > ")
            if query == "exit" or query == "quit":
                break
            elif query == "log":
                print(json.dumps(client.messages, indent=2, ensure_ascii=False))
                continue
            elif query == "usage":
                print(json.dumps(client.tot_usage, indent=2, ensure_ascii=False))
                continue
            await client.process_query("qwen-plus", query)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
