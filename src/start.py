# src/start.py
import uvicorn

from modules.webapp import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)