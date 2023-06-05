import logging

from slack_bolt import App
from commands.serve_task.cmd import Register_serve_task_command 

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

Register_serve_task_command(app, "st")

from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)