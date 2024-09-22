import logging
from health import health_update
from time import sleep
from queue import Empty
from jobs.processor import Job,JobResult, process_job
from config import WORK_QUEUE_POLL_INTERVAL_SECONDS
import traceback

def get_bg_work_loop(commands, slack_app, targetChannel):

    def create_start_message(job: Job):
        user = f"<@{job.user}>"
        msgText = f"Hey {user}, I'm starting your {job.prettyName} task now."
        msg = slack_app.client.chat_postMessage(channel=targetChannel,text=msgText)
        job.tsId = msg['ts']
    
    def create_error_message(job: Job, data):
        msgText = f"Something went wrong with your {job.prettyName} task. See the following details, or ask someone for help. \n{data}"
        slack_app.client.chat_postMessage(channel=targetChannel, thread_ts= job.tsId, text=msgText, icon_emoji=":no_entry:")
        logging.info(f"Graceful error on command {job}")

    def create_success_message(job: Job, results):
        msgText = f"Done with your {job.prettyName} task!{results}"
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
                    result: JobResult = process_job(job=command, slack_app=slack_app, target_channel=targetChannel, healhFn=health_update)
                    if result.success:
                        create_success_message(command, result.data)
                    else:
                        create_error_message(command, result.data)
                except Exception:
                    logging.error(f"Unhandled error on command {command}")
                    create_error_message(command, traceback.format_exc())
            except Empty:
                sleep(WORK_QUEUE_POLL_INTERVAL_SECONDS)
            except Exception:
                logging.error("uh oh!")

            sleep(1)
    
    return bg_work_loop