import logging
import pprint
from slack_bolt import App
import commands.serve_task_modal

serve_task_prefix = ""
def Register_serve_task_command(app, id_prefix):
    serve_task_prefix = id_prefix
    @app.command("/serve-task")
    def handle_command(body, ack, respond, client, logger):
        logger.info(body)
        ack()
        res = client.views_open(
        trigger_id=body["trigger_id"],
        view=commands.serve_task_modal.get_init_modal(serve_task_prefix)
        )
        logger.info(res)

    @app.action(f"{id_prefix}-environment_select")
    def handle_some_action(ack, body, logger):
        ack()

    @app.view(f"{id_prefix}-serve-task-view-id")
    def view_submission(ack, body, logger):
        print("IN VIEW_SUBMISSION")
        ack()
        response_values = body["view"]["state"]["values"]
        pprint.pprint(response_values)
        res_env = response_values['environment_select_block'][f"{id_prefix}-environment_select"]['selected_option']['value']
        res_id = response_values['item_id_block'][f"{id_prefix}-item_id_label"]['value']
        res_amt = response_values['item_amt_block'][f"{id_prefix}-item_amt_label"]['value']
        logger.info(f"{res_env} {res_id} {res_amt}")
    

