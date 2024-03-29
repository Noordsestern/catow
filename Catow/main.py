import os
import asyncio
import json
import requests

# Webservice
from fastapi import FastAPI
from uvicorn import Server
from uvicorn.config import Config

from Catow.Config import Config as CatowConfig

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.run_coroutine_threadsafe(watch_topic(), asyncio.get_event_loop())


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
            response = requests.get(f'{CatowConfig().cmd_args.camundaurl}/engine-rest/external-task/count?topicName={CatowConfig().cmd_args.topic}&notlocked=true&active=true&withRetriesLeft=true', timeout=(3.05, 5))
            response.raise_for_status()
            #print(response.text)
            response_body = json.loads(response.text)
            count = response_body["count"]
            if count > 0:
                print(f"Start Robot for amount of process instances: {count}")
                try:
                    response = requests.get(CatowConfig().cmd_args.roboturl, timeout=(3.05, 5))
                    response.raise_for_status()
                except Exception as e:
                    print(f'[WARN] Failed to trigger robot:\n{e}')
            else:
                #print("Nothing to do here.")
                pass
        except Exception as e:
            print(f'Failed to contact Camunda:\n{e}')

        await asyncio.sleep(CatowConfig().cmd_args.interval)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=os.environ.get('CATOW_PORT', default=5003), type=int,
                        help="Port of Camunda Topic Watcher Webservice")
    parser.add_argument("-c", "--camundaurl", default='http://localhost:8080', help="URL of Camunda platform")
    parser.add_argument("-t", "--topic", default="aTopic", type=str,
                        help="Topic of service task to listen for on Camunda")
    parser.add_argument("-r", "--roboturl", default='http://localhost:5004/robotframework/run/all', type=str,
                        help="Url to be called when workload is detected")
    #parser.add_argument('--version', action='version', version=f'Camunda Topic Watcher Webservice {get_version()}')
    parser.add_argument("-i", "--interval", default=3, type=int,
                        help="Polling interval in seconds")

    args = parser.parse_args()

    CatowConfig().cmd_args = args
    print(f"Camunda Topic Watcher configured:\n{CatowConfig().cmd_args}")

    run_server()


if __name__ == "__main__":
    main()



