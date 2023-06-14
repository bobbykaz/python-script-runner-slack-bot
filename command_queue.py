from health import health_update
from time import sleep

from queue import Empty

def get_bg_work_loop(commands, slack_app):
    def bg_work_loop():
        while True:
            health_update()
            try:
                command = commands.get_nowait()
                msg = slack_app.client.chat_postMessage(channel="bots",text=f"Starting:\n```{command}```")
                print(command)
                slack_app.client.chat_postMessage(channel="bots",text=f"Finished:\n```{command}```")
            except Empty:
                pass
            sleep(10)
    
    return bg_work_loop