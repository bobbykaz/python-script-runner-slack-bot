from slack_bolt import App
from jobs.processor import Job

def Register_example_command(app: App, work_queue):
    
    @app.command("/hello-bolt-python")
    def handle_command(body, ack, respond, client, logger):
        ack()
        work_queue.put_nowait(Job(user=body['user_id'], name="example", args=["Sample 1", "Sample 2"]))
        respond(text="OK, working on it!")
    

