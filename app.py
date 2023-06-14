import logging
from queue import Queue, Empty
from threading import Thread
from time import sleep
from slack_bolt import App
from commands.serve_task.cmd import Register_serve_task_command 
from health import health_check, health_update

logging.basicConfig(level=logging.DEBUG)
#creds loaded from env var
app = App()

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

@app.command("/hello-bolt-python")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")

commands = Queue()

Register_serve_task_command(app, commands, "st")

from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def bg_work_loop():
    while True:
        health_update()
        try:
            command = commands.get_nowait()
            msg = app.client.chat_postMessage(channel="bots",text=f"Starting:\n```{command}```")
            print(command)
            app.client.chat_postMessage(channel="bots",text=f"Finished:\n```{command}```")
        except Empty:
            pass
        sleep(10)

Thread(target=bg_work_loop, daemon=True).start()

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/health", methods=["GET"])
def health_get():
    return health_check()