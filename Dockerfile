#
# docker build . -t your-repo/hello-bolt
#
FROM python:3.11.4-slim-buster as builder
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install -U pip && pip install -r requirements.txt

FROM python:3.11.4-slim-buster as app
WORKDIR /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY *.py /app/
COPY commands/ /app/commands/
COPY jobs/ /app/jobs/
COPY scripts/ /app/scripts/
ENTRYPOINT gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 0 app:flask_app

#
# docker run -e SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET -e SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN -e PORT=3000 -p 3000:3000 -it your-repo/hello-bolt
#