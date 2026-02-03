from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self, mcp_config: dict):
        self.mcp_config = mcp_config
        self.server_list = []
        self.available_tools = []
        self.tool_to_server = {}
        self.session: dict[str, ClientSession] = {}
        self.exit_stack: dict[str, AsyncExitStack] = {}
        self.stdio = {}
        self.write = {}

    async def _connect_to_server(self, server:str, cfg: dict):
        server_params = StdioServerParameters(
            command=cfg["command"],
            args=cfg["args"],
            env=cfg["env"] if "env" in cfg else None,
        )
        self.exit_stack[server] = AsyncExitStack()
        stdio_transport = await self.exit_stack[server].enter_async_context(stdio_client(server_params))
        self.stdio[server], self.write[server] = stdio_transport
        self.session[server] = await self.exit_stack[server].enter_async_context(
            ClientSession(self.stdio[server], self.write[server])
        )
        await self.session[server].initialize()
        response = await self.session[server].list_tools()
        self.available_tools.extend([
            {
                "type": "function", 
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            }
            for tool in response.tools
        ])
        for tool in response.tools:
            if self.tool_to_server.get(tool.name) is not None:
                print(f"[WARNING] Tool {tool.name} already exists. Overwriting...")
            self.tool_to_server[tool.name] = server
        self.server_list.append(server)
        print(f"MCP Server: {server} is connected!")

    async def connect_to_servers(self) -> None:
        for server, cfg in self.mcp_config.items():
            await self._connect_to_server(server, cfg)
        print("[SERVERS]", self.server_list)
        print("[TOOLS]", [tool["function"]["name"] for tool in self.available_tools])

    async def call_tool(self, name: str, args: dict):
        server = self.tool_to_server[name]
        print(f"[TOOL] {name} called with args: {args}")
        return await self.session[server].call_tool(name, args)

    async def cleanup(self) -> None:
        for i in range(len(self.server_list) - 1, -1, -1):
            server = self.server_list[i]
            await self.exit_stack[server].aclose()
