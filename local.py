from jobs.processor import process_job
from jobs.job import Job
import sys

if __name__ == "__main__":
    args = sys.argv
    job = Job("", args[1], args[2:])
    process_job(job)