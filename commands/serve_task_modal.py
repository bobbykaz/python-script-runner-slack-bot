def get_init_modal(id_prefix):
	return {
		"type": "modal",
		"callback_id": f"{id_prefix}-serve-task-view-id",
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
				"block_id":"environment_select_block",
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Server Environment"
				},
				"accessory": {
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Environment",
						"emoji": False
					},
					"action_id": f"{id_prefix}-environment_select",
					"initial_option":{
							"text": {
								"type": "plain_text",
								"text": "Dev",
								"emoji": False
							},
							"value": "dev"
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
				"block_id":"item_id_block",
				"type": "input",
				"element": {
					"type": "plain_text_input",
					"action_id": f"{id_prefix}-item_id_label",
				},
				"label": {
					"type": "plain_text",
					"text": "Item ID",
					"emoji": False
				}
			},
			{
				"block_id":"item_amt_block",
				"type": "input",
				"element": {
					"type": "plain_text_input",
					"action_id": f"{id_prefix}-item_amt_label",
				},
				"label": {
					"type": "plain_text",
					"text": "Amount",
					"emoji": False
				}
			}
		]
	}