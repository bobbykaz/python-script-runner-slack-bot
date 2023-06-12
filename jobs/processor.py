import uuid
import jobs.tee
import jobs.jira_reporter.script
import jobs.jira_reporter.badscript
import os
import enum
import traceback

class JobReportType(enum.Enum):
    AtTheEnd = 1
    Live = 2
    NoReport = 3

class Job(object):
    def __init__(self, user, name, args, notifyStart=False, reportType=JobReportType.AtTheEnd, tsId=None):
        self.user = user
        self.name = name
        self.args = args
        self.id = uuid.uuid4()
        self.notifyStart = notifyStart
        self.reportType = reportType
        self.tsId = tsId
    def __str__(self):
        return f"{self.user}-{self.name}-{self.args}-{self.notifyStart}-{self.reportType}-{self.tsId}"
     

def process_job(job: Job, slack_app=None):
    print(f"{job}")
    args = [job.name] + job.args
    filename = f"{job.name}-{job.id}.log"

    with jobs.tee.FileTee(filename, 'w'):
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

def teeUp(job: Job, app):
    match job.reportType:
        case JobReportType.AtTheEnd:
            filename = f"{job.name}-{job.id}.log"
            return jobs.tee.FileTee(filename, 'w')
        case JobReportType.Live:
            return jobs.tee.LiveSlackTee()
        case _:
            return jobs.tee.EmpTee()