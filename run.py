import multiprocessing as mp
import argparse
import os

from src.server import start_server
import uvicorn






if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app = start_server()
    uvicorn.run(app, host="0.0.0.0", port=8000)