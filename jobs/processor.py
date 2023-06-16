import uuid
import jobs.tee
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
        return f"{self.id}-{self.user}-{self.name}-{self.args}-{self.notifyStart}-{self.reportType}-{self.tsId}"
    
class JobResult(object):
    def __init__(self, data, success):
        self.data = data
        self.success = success
     

def process_job(job: Job, slack_app=None):
    print(f"{job}")
    args = [job.name] + job.args
    filename = f"{job.name}-{job.id}.log"

    ok = True
    with jobs.tee.FileTee(filename, 'w'):
        try:
            run_job_internal(job.name, args)
        except Exception as e:
            print(f"Error while running job [{job}]")
            print(traceback.format_exc())
            ok = False
        finally:
            pass
    
    data = ""
    with open(filename,'r') as file:
        data = file.read()
        
    os.remove(filename)
    return JobResult(data, ok)
    
import scripts.script
import scripts.badscript
import scripts.print_over_time
def run_job_internal(job_name, args):
    match job_name:
        case "good_test":
            scripts.script.main(args)
        case "fail_test":
            scripts.badscript.main(args)
        case "slow_test":
            scripts.print_over_time.main(args)
        case _:
            print(f"No job '{job_name}' found")

def teeUp(job: Job, app):
    match job.reportType:
        case JobReportType.AtTheEnd:
            filename = f"{job.name}-{job.id}.log"
            return jobs.tee.FileTee(filename, 'w')
        case JobReportType.Live:
            return jobs.tee.EmpTee()#jobs.tee.LiveSlackTee()
        case _:
            return jobs.tee.EmpTee()