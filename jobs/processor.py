import uuid
from jobs.job import Job
from jobs.tee import Tee
import jobs.jira_reporter.script
import os

def process_job(job: Job):
    jobid = uuid.uuid4()
    print(f"{jobid} - {job}")
    args = [job.name] + job.args
    filename = f"{job.name}-{jobid}.log"
    logger = Tee(filename, 'w')
    match job.name:
        case "jira":
            jobs.jira_reporter.script.main(args)
        case _:
            print("No job found")
    del logger
    print("Deleted tee")
    data = ""
    with filename as file:
        data = file.read()
    os.remove(filename)
    return data
    
    