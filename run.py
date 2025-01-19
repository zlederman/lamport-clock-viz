import multiprocessing as mp
import argparse

from src.server import start_server
import uvicorn






if __name__ == "__main__":
    app = start_server()
    uvicorn.run(app, host="0.0.0.0", port=8000)