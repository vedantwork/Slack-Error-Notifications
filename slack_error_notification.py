import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
#Create a .env file and store your SLACK_TOKEN there
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# Enter your channel name in place of notifications-alerts
client.chat_postMessage(channel='#notifications-alerts', text="Hello World !!")


#if you want to create a function to sent notification via a function here's what you can do
slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))  # Update this line
slack_channel = "#error-notification" #your channel name here
repo_name = "nova-identity-auth-server-v2" #the repo or the service you want 
def get_message_reaction_counts():
    try:
        # Get the channel ID from the channel name
        response = slack_client.conversations_list()
        channels = response["channels"]
        channel_id = next(
            (ch["id"] for ch in channels if ch["name"] == slack_channel.lstrip("#")),
            None,
        )

        if not channel_id:
            return {
                "with_react": "Channel not found",
                "without_react": "Channel not found",
            }

        # Fetch messages from the channel
        messages_response = slack_client.conversations_history(channel=channel_id)
        messages = messages_response["messages"]

        # Get the bot's user ID
        bot_info_response = slack_client.auth_test()
        bot_user_id = bot_info_response["user_id"]

        # Count the bot's messages
        bot_messages = [msg for msg in messages if msg.get("user") == bot_user_id]
        with_react_count = sum(1 for message in bot_messages if "reactions" in message)
        without_react_count = len(bot_messages) - with_react_count

        return {
            "with_react": with_react_count,
            "without_react": without_react_count + 1,
            "total_errors":with_react_count + without_react_count + 1,
        }

    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return {"with_react": None, "without_react": None}

def send_slack_message(url: str, payload: str, error_message: str, method: str):
    message_counts = get_message_reaction_counts()
    counts_text = (
        f" Solved: {message_counts.get('with_react', 'N/A')}\n\n"
        f" Unsolved: {message_counts.get('without_react', 'N/A')}\n\n"
        f" Total Errors: {message_counts.get('total_errors', 'N/A')}"
    )
    message = {
        "attachments": [
            {
                "color": "#FF0000",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"*Service:* *{repo_name}*\n\n"
                                f"*Request URL:* {url}\n\n"
                                f"*Method:* *{method}*\n\n"
                                f"*Payload:*\n*```{payload}```*\n\n"
                                f"*Error Message:*\n*```{error_message}```*\n\n"
                            ),
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "*:memo: Please address this issue as soon as possible. If tagged, you're responsible for investigating, resolving, and testing the issue in a staging environment.*",
                            },
                            {
                                "type": "image",
                                "image_url": "https://cdn.iconscout.com/icon/free/png-256/free-notification-icon-download-in-svg-png-gif-file-formats--alert-bell-alarm-user-interface-icons-2460127.png",  # Replace with your own icon if needed
                                "alt_text": counts_text,
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Hover over the icon to track the status.*",
                            }
                        ],
                    },
                ],
            }
        ]
    }

    try:
        response = slack_client.chat_postMessage(channel=slack_channel, **message)
        return response
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
        return None

#This is a customize function that will only get few lines from your traceback
def get_main_part_of_traceback():
    full_traceback = traceback.format_exc()
    traceback_lines = full_traceback.splitlines()
    if len(traceback_lines) > 5:
        main_traceback_part = "\n".join(traceback_lines[-5:])
    else:
        main_traceback_part = full_traceback
    return main_traceback_part


    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        request.state.body = body
        method = request.method
        try:
            response = await call_next(request)
            if response.status_code == 500:
                full_url = str(request.url)
                body = request.state.body.decode("utf-8")
                error_message = "500 Internal Server Error occurred"
                send_slack_message(full_url, body, error_message, method)
            return response
        except Exception as exc:
            main_traceback = get_main_part_of_traceback()
            full_url = str(request.url)
            body = request.state.body.decode("utf-8")
            error_message = (
                f"Unhandled exception: {str(exc)}\n\nTraceback:\n{main_traceback}"
            )
            send_slack_message(full_url, body, error_message, method)
            return JSONResponse(
                status_code=500,
                content={"code": 500, "msg": "Internal Server Error", "exc": str(exc)},
            )

