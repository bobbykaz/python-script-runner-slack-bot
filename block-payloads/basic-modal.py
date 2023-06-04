helper_script_1_model = {
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
					"text": "Select an item",
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
				],
				"action_id": "environment-action"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "item-id-action"
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
				"type": "plain_text_input",
				"action_id": "item-amount-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Amount",
				"emoji": False
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Go!",
						"emoji": False
					},
					"value": "submit",
					"action_id": "click-accept"
				}
			]
		}
	]
}