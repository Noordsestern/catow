import os
import asyncio

import requests
from fastapi import FastAPI
from requests import HTTPError
from uvicorn import Server
from uvicorn.config import Config

from Catow.Config import Config as CatowConfig

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(watch_topic())


@app.get("/")
async def root():
    return {"message": "Hello World"}


def run_server():
    print("Run server")
    server = Server(config=(Config(app=app, loop="asyncio", host="0.0.0.0", port=CatowConfig().cmd_args.port)))
    server.run()


async def watch_topic():
    while True:
        try:
            future = asyncio.run_coroutine_threadsafe(requests.get(CatowConfig().cmd_args.camundaurl))
            response = future.result()
            response.raise_for_status()
        except Exception as e:
            print(f'Failed to contact Camunda:\n{e}')

        await asyncio.sleep(1)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--camundaurl", default='http://localhost:8080', help="URL of Camunda platform")
    #parser.add_argument('--version', action='version', version=f'Camunda Topic Watcher Webservice {get_version()}')
    parser.add_argument("-p", "--port", default=os.environ.get('CATOW_PORT', default=5003), type=int, help="Port of Camunda Topic Watcher Webservice")
    args = parser.parse_args()

    CatowConfig().cmd_args = args

    run_server()


if __name__ == "__main__":
    main()



