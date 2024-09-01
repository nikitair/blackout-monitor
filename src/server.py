from fastapi import FastAPI, Request
import subprocess
import uvicorn
from pydantic import BaseModel
from logging_config import logger


app = FastAPI()

class PingRequest(BaseModel):
    ip: str


@app.get("/")
def index():
    return {"data": None}


@app.post("/ping")
async def ping(request: PingRequest):
    # try:
    ip = request.ip
    logger.info(f"ping ip - ({ip})")
    
    ping_response = subprocess.run(
        ["ping", "-c", "1", ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    status_code = ping_response.returncode
    message = ping_response.stdout.decode()
    error = ping_response.stderr.decode()
    
    logger.info(f"ping status code - ({status_code})")
    logger.info(f"ping message - ({message})")
    logger.info(f"ping error - ({error})")
    
    return {
        "status_code": status_code,
        "message": message,
        "error": error
    }
        
    # except Exception:
    #     return {"message": "Bad Data received"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)