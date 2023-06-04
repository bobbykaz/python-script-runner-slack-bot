import logging
import pprint
from slack_bolt import App
import commands.serve_task_modal

def Register_serve_task_command(app):
    @app.command("/serve-task")
    def handle_command(body, ack, respond, client, logger):
        logger.info(body)
        ack()
        res = client.views_open(
        trigger_id=body["trigger_id"],
        view=commands.serve_task_modal.Init_Modal
        )
        logger.info(res)

    @app.view("serve-task-view-id")
    def view_submission(ack, body, logger):
        print("IN VIEW_SUBMISSION")
        ack()
        pprint.pprint(body)
        logger.info(body["view"]["state"]["values"])
    

