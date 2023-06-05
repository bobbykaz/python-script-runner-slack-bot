import os
import logging
from slack_bolt import App
from commands.serve_task.cmd import Register_serve_task_command 

logging.basicConfig(level=logging.DEBUG)
# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.command("/hello-bolt-python")
def handle_command(body, ack, respond, client, logger):
    logger.info(body)
    ack(
        text="Accepted!",
        blocks=[
            {
                "type": "section",
                "block_id": "b",
                "text": {
                    "type": "mrkdwn",
                    "text": ":white_check_mark: Accepted!",
                },
            }
        ],
    )

    respond(
        blocks=[
            {
                "type": "section",
                "block_id": "b",
                "text": {
                    "type": "mrkdwn",
                    "text": "You can add a button alongside text in your message. ",
                },
                "accessory": {
                    "type": "button",
                    "action_id": "a",
                    "text": {"type": "plain_text", "text": "Button"},
                    "value": "click_me_123",
                },
            }
        ]
    )

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view-id",
            "title": {
                "type": "plain_text",
                "text": "Bobby App Title",
            },
            "submit": {
                "type": "plain_text",
                "text": "Bobby Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Bobby Cancel",
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {"type": "plain_text_input"},
                    "label": {
                        "type": "plain_text",
                        "text": "Label",
                    },
                },
                {
                    "type": "input",
                    "block_id": "es_b",
                    "element": {
                        "type": "external_select",
                        "action_id": "es_a",
                        "placeholder": {"type": "plain_text", "text": "Select an item"},
                        "min_query_length": 0,
                    },
                    "label": {"type": "plain_text", "text": "Search"},
                },
                {
                    "type": "input",
                    "block_id": "mes_b",
                    "element": {
                        "type": "multi_external_select",
                        "action_id": "mes_a",
                        "placeholder": {"type": "plain_text", "text": "Select an item"},
                        "min_query_length": 0,
                    },
                    "label": {"type": "plain_text", "text": "Search (multi)"},
                },
            ],
        },
    )
    logger.info(res)


@app.options("es_a")
def show_options(ack):
    print("IN SHOW_OPTIONS")
    ack({"options": [{"text": {"type": "plain_text", "text": "Maru"}, "value": "maru"}]})


@app.options("mes_a")
def show_multi_options(ack):
    print("IN SHOW_MULTI_OPTIONS")
    ack(
        {
            "option_groups": [
                {
                    "label": {"type": "plain_text", "text": "Group 1"},
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "Option 1"},
                            "value": "1-1",
                        },
                        {
                            "text": {"type": "plain_text", "text": "Option 2"},
                            "value": "1-2",
                        },
                    ],
                },
                {
                    "label": {"type": "plain_text", "text": "Group 2"},
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "Option 1"},
                            "value": "2-1",
                        },
                    ],
                },
            ]
        }
    )


@app.view("view-id")
def view_submission(ack, body, logger):
    print("IN VIEW_SUBMISSION")
    ack()
    logger.info(body["view"]["state"]["values"])


@app.action("a")
def button_click(ack, body, respond):
    print("IN BUTTON_CLICK")
    ack()

    user_id = body["user"]["id"]
    # in_channel / dict
    respond(
        {
            "response_type": "in_channel",
            "replace_original": False,
            "text": f"<@{user_id}> clicked a button! (in_channel)",
        }
    )
    # ephemeral / kwargs
    respond(
        replace_original=False,
        text=":white_check_mark: Done!",
    )

Register_serve_task_command(app, "st")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 80)))