import slack 
import os
import functools
import pdb
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask,Response
from slackeventsapi import SlackEventAdapter
import requests
from datetime import datetime,timedelta


summary= requests.get('https://http://standnote.herokuapp.com/summarizer/')
message= summary.message
time_of_meeting=summary.time
# signing_secret=summary.signing_secret
# slack_token= summary.slack_token
# channel_id= summary.channel_id



env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

bp = Blueprint('auth', __name__, url_prefix='/auth')
client_id = 'XXXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXXX'
oauth_scope = 'channels:read,chat:write:bot,users:read,users:read.email'


app=Flask(__name__)
slack_event_adapter=SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client= slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

SCHEDULED_MESSAGES=[
    {'text':message,'post_at':(datetime.now()+timedelta(seconds=30)).timestamp(),'channel':'C01G8SLT4KB'}
]


@bp.route('/redirect', methods=['GET'])
def authorize():
    authorize_url = f"https://slack.com/oauth/authorize?scope={ oauth_scope }&client_id={ client_id }"

    return redirect(authorize_url)

@bp.route('/callback', methods=["GET", "POST"])
def callback():
    auth_code = request.args['code']
    client = slack.WebClient(token="")
    oauth_info = client.oauth_access(
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code
    )

access_token = oauth_info['access_token']
client = slack.WebClient(token=access_token)
user_id = oauth_info['user_id']
response = client.users_info(user=user_id)

# @slack_event_adapter.on('message')
# def message(payload):
#     event=payload.get('event',{})
#     channel_id=event.get('channel')
#     user_id=event.get('user')
#     text=event.get('text')
#     if(BOT_ID!=user_id and text=="Summary"):
#         client.chat_postMessage(channel=channel_id,text="Slave spirituals often had hidden double meanings. On one level, spirituals referenced heaven, Jesus, and the soul, but on another level, the songs spoke about slave resistance. For example, according to Frederick Douglass, the song “O Canaan, Sweet Canaan” spoke of slaves’ longing for heaven, but it also expressed their desire to escape to the North. Careful listeners heard this second meaning in the following lyrics: “I don’t expect to stay / Much longer here. / Run to Jesus, shun the danger. / I don’t expect to stay.” When slaves sang this song, they could have been speaking of their departure from this life and their arrival in heaven; however, they also could have been describing their plans to leave the South and run, not to Jesus, but to the North. Slaves even used songs like “Steal Away to Jesus (at midnight)” to announce to other slaves the time and place of secret, forbidden meetings. What whites heard as merely spiritual songs, slaves discerned as detailed messages. The hidden meanings in spirituals allowed slaves to sing what they could not say.")


def schedule_messages(messages):
    ids=[]
    for msg in messages:
        response= client.chat_scheduleMessage(channel=msg['channel'],text=msg['text'],post_at=msg['post_at'])
        id_=response['id']
    ids.append(id_)
    return ids


if __name__=="__main__":
    schedule_messages(SCHEDULED_MESSAGES)
    app.run(debug=True)