import uuid
from jobs.tee import Tee
import jobs.jira_reporter.script
import jobs.jira_reporter.badscript
import os
import traceback

class Job(object):
    def __init__(self, user, name, args):
        self.user = user
        self.name = name
        self.args = args
    def __str__(self):
        return f"{self.user} - {self.name} - {self.args}"
     

def process_job(job: Job):
    jobid = uuid.uuid4()
    print(f"{jobid} - {job}")
    args = [job.name] + job.args
    filename = f"{job.name}-{jobid}.log"

    with Tee(filename, 'w'):
        try:
            run_job_internal(job.name, args)
            print(f"@{job.user}: Your job has been completed.")
        except Exception as e:
            print(f"@{job.user}: Sorry, I ran into an error while running your job\n Job Details: [{job}]")
            print(traceback.format_exc())
        finally:
            pass
    
    data = ""
    with open(filename,'r') as file:
        data = file.read()
        
    os.remove(filename)
    return data
    

def run_job_internal(job_name, args):
    match job_name:
        case "jira":
            jobs.jira_reporter.script.main(args)
        case "fail_test":
            jobs.jira_reporter.badscript.main(args)
        case _:
            print(f"No job '{job_name}' found")
    