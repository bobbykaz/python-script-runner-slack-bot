Init_Modal = {
	"type": "modal",
	"callback_id": "serve-task-view-id",
	"title": {
		"type": "plain_text",
		"text": "Serve Generic Task",
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
	},
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Please input the item ID and how many items to add."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Server Environment"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Choose Environment",
					"emoji": False
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Dev",
							"emoji": False
						},
						"value": "dev"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage",
							"emoji": False
						},
						"value": "stage"
					}
				]
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input"
			},
			"label": {
				"type": "plain_text",
				"text": "Item ID",
				"emoji": False
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input"
			},
			"label": {
				"type": "plain_text",
				"text": "Amount",
				"emoji": False
			}
		}
	]
}