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
    def __init__(self, user, name, args, notifyStart=False, reportType=JobReportType.AtTheEnd, tsId=None, prettyName=None):
        self.user = user
        self.name = name
        self.prettyName = prettyName or name
        self.args = args
        self.id = uuid.uuid4()
        self.notifyStart = notifyStart
        self.reportType = reportType
        self.tsId = tsId
    def __str__(self):
        return f"{self.id}-{self.user}-{self.name}-{self.prettyName}-{self.args}-{self.notifyStart}-{self.reportType}-{self.tsId}"
    
class JobResult(object):
    def __init__(self, data, success):
        self.data = data
        self.success = success
     
def _dummyHealthFn():
    pass

def process_job(job: Job, slack_app=None, target_channel=None, healhFn=_dummyHealthFn):
    print(f"{job}")

    ok = True
    data = ""
    with teeUp(job, slack_app, target_channel) as tee:
        try:
            run_job_internal(job.name, job.args, healhFn)
        except Exception as e:
            print(f"Error while running job [{job}]")
            print(traceback.format_exc())
            ok = False
        finally:
            pass
        data = tee.final_result()


    return JobResult(data, ok)

import scripts.script
import scripts.badscript
def run_job_internal(job_name, args, healthFn=_dummyHealthFn):
    match job_name:
        case "good_test":
            scripts.script.main(args)
        case "fail_test":
            scripts.badscript.main(args)
        case _:
            print(f"No job '{job_name}' found")

def teeUp(job: Job, slack_app, target_channel):
    match job.reportType:
        case JobReportType.AtTheEnd:
            filename = f"{job.name}-{job.id}.log"
            return jobs.tee.FileTee(filename, 'w')
        case JobReportType.Live:
            return jobs.tee.LiveSlackTee(slack_app, job.tsId, target_channel)
        case _:
            return jobs.tee.EmpTee()