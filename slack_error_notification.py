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
