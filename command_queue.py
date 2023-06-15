import logging
from health import health_update
from time import sleep
from queue import Empty
from jobs.processor import Job,JobResult, process_job
import traceback

def get_bg_work_loop(commands, slack_app, targetChannel):

    def create_start_message(job: Job):
        user = f"<@{job.user}>"
        msgText = f"Hey {user}, I'm starting your {job.name} task now."
        msg = slack_app.client.chat_postMessage(channel=targetChannel,text=msgText)
        job.tsId = msg['ts']
    
    def create_error_message(job: Job, data):
        msgText = f"Something went wrong with your {job.name} task. See the following details, or ask someone for help. \n ```{data}```"
        slack_app.client.chat_postMessage(channel=targetChannel, thread_ts= job.tsId, text=msgText, icon_emoji=":no_entry:")
        logging.info(f"Graceful error on command {job}")

    def create_success_message(job: Job, results):
        msgText = f"Done with your {job.name} task! Your job generated the following:\n ```{results}```"
        slack_app.client.chat_postMessage(channel=targetChannel, thread_ts= job.tsId, text=msgText, icon_emoji=":white_check_mark:")
        logging.info(f"Finished command {job}")


    def bg_work_loop():
        while True:
            health_update()
            try:
                command: Job = commands.get_nowait()
                logging.info(f"Processing command {command}")
                try:
                    create_start_message(command)
                    result: JobResult = process_job(command)
                    if result.success:
                        create_success_message(command, result.data)
                    else:
                        create_error_message(command)
                except Exception:
                    logging.error(f"Unhandled error on command {command}")
                    create_error_message(command, traceback.format_exc())
            except Empty:
                pass
            except Exception:
                logging.error("uh oh!")
            sleep(5)
    
    return bg_work_loop