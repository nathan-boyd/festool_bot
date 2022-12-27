import requests
import os
from bs4 import BeautifulSoup
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

logger = logging.getLogger('check_site')

app_token = os.environ['PUSHOVER_APP_TOKEN']
user_key = os.environ['PUSHOVER_USER_KEY']
filename = os.environ['STATE_FILE_PATH']

if not os.path.exists(filename):
    open(filename, 'w+').close()
    with open(filename, 'a') as f:
        f.write('nil')

cached_tool = ""
with open(filename,'r') as f:
    cached_tool = f.read()

festool_url = 'https://www.festoolrecon.com/'
r = requests.get(festool_url)
soup = BeautifulSoup(r.text, 'html.parser')
current_tool = soup.find('h1', attrs={'class': 'product-single__title'}).text

if current_tool != cached_tool:
    logger.info(f'The Festool Recon Offering has changed to "{current_tool}"')
    with open(filename, 'w') as f:
        f.write(current_tool)
else:
    logger.info(f'The Festool Recon Offering is still "{cached_tool}"')
    exit(0)

message = f'The Festool Recon Offering is "{current_tool}"'
data = {
	'token': app_token,
	'user': user_key,
	'message': message
}

logger.info('Sending push notification')
pushover_url = "https://api.pushover.net/1/messages.json"
requests.post(pushover_url, data=data)
