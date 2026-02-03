## init

```bash
uv sync
cd qwen3-tts-exp
modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-Base --local_dir ./Qwen3-TTS-12Hz-1.7B-Base
```

## plays

### agent-exp

一个简单的聊天 Agent，使用了 MCP 和 Function Calling 

```bash
uv run ./agent-exp/src/main.py
```

### aicmd

使用自然语言让 AI 生成和执行终端命令

使用的模型为 deepseek-chat

```bash
uv build --package aicmd
```

### mcp-exp

MCP 服务器样例

- atri-mcp 一个简单的 MCP 服务器
- mcp-logger 充当 MCP Client 和 Server 的中间人，并将通信数据保存到 `mcp-exp/src/mcp-logger/dist` 文件夹中
- llm-logger 充当模型调用和云端模型服务的中间服务器，并将通信数据保存到 `mcp-exp/src/llm-logger/dist` 文件夹中

MCP 配置（`[REPO_PATH]` 替换为项目路径）：

```json
{
  "mcpServers": {
    "atri-mcp": {
      "disabled": true,
      "timeout": 10,
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "[REPO_PATH]",
        "run",
        "mcp-exp/src/atri-mcp/atri_mcp.py"
      ]
    },
    "atri-mcp-logger": {
      "disabled": true,
      "timeout": 10,
      "type": "stdio",
      "command": "python",
      "args": [
        "[REPO_PATH]/mcp-exp/src/mcp-logger/mcp_logger.py",
        "uv",
        "--directory",
        "[REPO_PATH]",
        "run",
        "mcp-exp/src/atri-mcp/atri_mcp.py"
      ]
    }
  }
}
```

### pkg-exp

项目打包示例

```
uv build --package flat_example
uv build --package src_example
```

### qwen3-tts-exp

Qwen3-TTS 的简单使用

直接使用 Jupyter Notebook

