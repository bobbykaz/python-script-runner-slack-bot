# python-slack-bot
Basic slack bot in python

Set up:
1. new app in slack
2. Oauth Permissions Section, add `chat:write` scope, save token
3. Basic info, save signing secret
4. Notifications - add `/slack/events` route, let the app verify
5. Commands - add `/slack/events` route for ALL slash commands
6. Interactivity - add `/slack/events` route to both the UI interactivity AND the External UI options on this page.

Run:
`flask --app app run -p 80`

Examples:
https://github.com/slackapi/bolt-python/tree/main/examples