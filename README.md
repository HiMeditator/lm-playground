## init

```bash
uv sync
cd qwen3-tts-exp
modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-Base --local_dir ./Qwen3-TTS-12Hz-1.7B-Base
```

## plays

### qwen3-tts-exp

Qwen3-TTS 的简单使用

直接使用 Jupyter Notebook

### pkg-exp

项目打包示例

```
uv build --package flat_example
uv build --package src_example
```

### aicmd

使用自然语言让 AI 生成和执行终端命令

使用的模型为 deepseek-chat

```bash
uv build --package aicmd
```
