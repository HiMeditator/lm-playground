import json
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
from .mcp_client import MCPClient
# from openai.types.chat import ChatCompletionUserMessageParam

class AtriAgent:
    def __init__(self, base_url: str, api_key: str, mcp_config: dict):
        self.base_url = base_url
        self.api_key = api_key
        self.openai_compat = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        self.messages = [
            { "role": "system", "content": "You are Atri (Chinese: 亚托莉, Japanese: アトリ), the female protagonist of the visual novel ATRI -My Dear Moments-."}
        ]
        self.tot_usage = {
            "completion_tokens": 0,
            "prompt_tokens": 0,
            "cached_prompt_tokens": 0,
        }
        self.latest_token = 0
        self.mcp_client = MCPClient(mcp_config)

    async def connect_mcp_servers(self):
        await self.mcp_client.connect_to_servers()

    async def process_query(self, model: str, query: str | None) -> str:
        if query is not None:
            self.messages.append({"role": "user", "content": query})

        stream = self.openai_compat.chat.completions.create(
            model=model,
            messages=self.messages, # type: ignore
            tools=self.mcp_client.available_tools,
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
            name = str(tool_calls_msg["tool_calls"][0]["function"]["name"])
            arguments = tool_calls_msg["tool_calls"][0]["function"]["arguments"]
            if not arguments:
                arguments = {}
            else:
                arguments = json.loads(arguments)
            # print(f'[CALL]', tool_calls_msg["tool_calls"][0])
            result = await self.mcp_client.call_tool(name, arguments)
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
        await self.mcp_client.cleanup()
