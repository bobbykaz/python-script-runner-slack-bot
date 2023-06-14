import logging
from queue import Queue
from threading import Thread
from slack_bolt import App
from commands.serve_task.cmd import Register_serve_task_command 
from health import health_check
import command_queue

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
Thread(target=command_queue.get_bg_work_loop(commands, app), daemon=True).start()

from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/health", methods=["GET"])
def health_get():
    return health_check()