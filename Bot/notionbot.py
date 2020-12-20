from notion.client import NotionClient
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from notion.block import TextBlock


summary= requests.get('https://http://standnote.herokuapp.com/summarizer/')
message= summary.message
# page_url=summary.page_url
# tokenv2= summary.token_v2



env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
client=NotionClient(token_v2=os.environ['Token_v2'])
page=client.get_block("https://www.notion.so/Test-1-4266b2f62827486a84d96814b51027c9")

page.title = "Stand Up Notes :"
    newchild=page.children.add_new(TextBlock,title="Here's your standup meeting notes. \n•  Let's after 23 hours. \n•  It was like a entire paragraph, right? So? But when whenever we want the summary of the meeting its like which party told one thing right? \n•  Like let's say the client old is and but when the Summarisation works its like entire voice is converted into text and no segregation is done right? No arrangement of text or no no sensible format like first this client. \n•  then this organiser then client then organiser kind of stuff so it really becomes")
