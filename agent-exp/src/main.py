import asyncio
import os
import json
from agent import AtriAgent
from colorama import Fore, Style, init

init(autoreset=True)

async def main():
    client = AtriAgent(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DASHSCOPE_API_KEY") or "",
        mcp_config={
            "atri-mcp": {
                "command": "uv",
                "args": [
                    "--directory",
                    "D:\\Projects\\lm-playground",
                    "run",
                    "mcp-exp/src/atri-mcp/atri_mcp.py"
                ]
            },
            "fetch": {
                "command": "npx",
                "args": [
                    "mcp-fetch-server"
                ],
                "env": {
                    "DEFAULT_LIMIT": "50000"
                }
            }
        }
    )
    try:
        await client.connect_mcp_servers()
        while True:
            print(f"{Fore.GREEN}========== ATRI Chat Agent v0.1.0 ==========")
            print(f"{Fore.GREEN}\tUse 'exit' or 'quit' to exit.")
            print(f"{Fore.GREEN}\tUse 'log' to print chat log.")
            print(f"{Fore.GREEN}\tUse 'usage' to show token usage.")
            print(f"{Fore.GREEN}\tUse 'context' to show context usage.")
            print(f"{Fore.GREEN}\tUse 'reset' to reset chat context.{Style.RESET_ALL}")
            query = input(f"{Fore.BLUE}ATRI > {Style.RESET_ALL}")
            if query == "exit" or query == "quit":
                break
            elif query == "log":
                print(json.dumps(client.messages, indent=2, ensure_ascii=False))
                continue
            elif query == "usage":
                print(json.dumps(client.tot_usage, indent=2, ensure_ascii=False))
                continue
            elif query == "context":
                print(client.context_usage)
                continue
            elif query == "reset":
                client.clear_context()
                print("Context reset.")
                continue
            await client.process_query("qwen-plus", query)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
