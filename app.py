import config
import logging
from queue import Queue
from threading import Thread
from slack_bolt import App

logging.basicConfig(level=logging.INFO)

app = App()

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

# Slash Commands or other Slack triggers that need to do long-running work can dump it here
work_queue = Queue()

###### Add Commands Below ################
from commands.serve_task.cmd import Register_serve_task_command 
Register_serve_task_command(app, work_queue, "st")

from commands.basic_example.cmd import Register_example_command
Register_example_command(app, work_queue)
##########################################

# Bootleg backround thread to process long-running work... or you can set up a proper external message queue...
import work_queue_loop
Thread(target=work_queue_loop.get_bg_work_loop(work_queue, app, "bots"), daemon=True).start()

from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

from health import health_check
@flask_app.route("/health", methods=["GET"])
def health_get():
    return health_check()