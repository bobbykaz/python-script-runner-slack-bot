import logging
import pprint
from slack_bolt import App
import commands.serve_task.modal

def Register_serve_task_command(app, work_queue, id_prefix):
    modal = commands.serve_task.modal.ServeTaskModal(id_prefix)
    
    @app.command("/serve-task")
    def handle_command(body, ack, respond, client, logger):
        logger.info(body)
        ack()
        res = client.views_open(
        trigger_id=body["trigger_id"],
        view=modal.modal()
        )
        logger.info(res)

    @app.action(modal.env_select_id)
    def handle_some_action(ack, body, logger):
        ack()

    @app.view(modal.view_id)
    def view_submission(ack, body, logger):
        print("IN VIEW_SUBMISSION")
        ack()
        response_values = body["view"]["state"]["values"]
        pprint.pprint(response_values)
        res_env = response_values['environment_select_block'][modal.env_select_id]['selected_option']['value']
        res_id = response_values['item_id_block'][modal.item_id]['value']
        res_amt = response_values['item_amt_block'][modal.item_amt_id]['value']
        logger.info(f"{res_env} {res_id} {res_amt}")
        work_queue.put_nowait({ 'command':'serve-task', 'args': [res_env,res_id,res_amt] })
    

