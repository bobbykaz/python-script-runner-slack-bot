import os

BOT_LOG_CHANNEL = os.environ.get("BOT_LOG_CHANNEL") or "bots"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
WORK_QUEUE_POLL_INTERVAL_SECONDS =  int(os.environ.get("WORK_QUEUE_POLL_INTERVAL_SECONDS") or "5")
HEALTH_CHECK_FAIL_THRESHOLD_SECONDS = int(os.environ.get("WORK_QUEUE_POLL_INTERVAL_SECONDS") or "180")

if SLACK_BOT_TOKEN is None:
    raise(Exception("SLACK_BOT_TOKEN environment variable is required"))
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
if SLACK_SIGNING_SECRET is None:
    raise(Exception("SLACK_SIGNING_SECRET environment variable is required"))