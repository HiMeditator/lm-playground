## Ref https://github.com/MarkTechStation/VideoCode/blob/main/MCP%E7%BB%88%E6%9E%81%E6%8C%87%E5%8D%97-%E7%95%AA%E5%A4%96%E7%AF%87/llm_logger.py

import os
import httpx
import json
from datetime import datetime
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse


class AppLogger:
    def __init__(self, log_file):
        """Initialize the logger with a file that will be cleared on startup."""
        self.log_file = log_file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("")

    def log(self, info: str, message):
        """Log a message to both file and console."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            sep = ""
            if info and message:
                sep = " "
            try:
                josn_obj = json.loads(message)
                f.write(f"{info}{sep}{json.dumps(josn_obj, ensure_ascii=False, indent=4)}\n")
            except:
                f.write(f"{info}{sep}{message}\n")
        print(message)


LOG_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "dist"
)
os.makedirs(LOG_DIR, exist_ok=True)
formatted_time = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOG_DIR, f"{formatted_time}.log")

app = FastAPI(title="LLM API Logger")
logger = AppLogger(LOG_FILE)


@app.post("/chat/completions")
async def proxy_request(request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')
    logger.log("[REQUEST]", body_str)
    
    body = await request.json()
    logger.log("[RESPONSE]", "")

    async def event_stream():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                    "POST",
                    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                    json=body,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "text/event-stream",
                        "Authorization": request.headers.get("Authorization") or "",
                    }
            ) as response:
                async for line in response.aiter_lines():
                    logger.log("", line)
                    yield f"{line}\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
