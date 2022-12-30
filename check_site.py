from bs4 import BeautifulSoup
import logging
import os
import requests
import sys
import traceback

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

logger = logging.getLogger('check_site')

app_token = os.environ['PUSHOVER_APP_TOKEN']
user_key = os.environ['PUSHOVER_USER_KEY']
filename = os.environ['STATE_FILE_PATH']
festool_url = 'https://www.festoolrecon.com/'
pushover_url = "https://api.pushover.net/1/messages.json"

def main():
    if not os.path.exists(filename):
        with open(filename, 'w+') as f:
            f.write('nil')

    cached_tool = ""
    with open(filename,'r') as f:
        cached_tool = f.read()

    current_tool = get_current_tool()

    if current_tool != cached_tool:
        logger.info(f'The Festool Recon Offering has changed to "{current_tool}"')
        with open(filename, 'w') as f:
            f.write(current_tool)
        send_notification(tool_name=current_tool)
    else:
        logger.info(f'The Festool Recon Offering is still "{cached_tool}"')

def get_current_tool():
    logger.info('Getting current tool')
    r = requests.get(festool_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    current_tool = soup.find('h1', attrs={'class': 'product-single__title'}).text
    logger.info(f'Current tool is {current_tool}')
    return current_tool

def send_notification(tool_name):
    logger.info('Sending push notification')
    data = {
    	'token': app_token,
    	'user': user_key,
    	'message': f'The Festool Recon offering has changed to "{tool_name}" {festool_url}'
    }
    requests.post(pushover_url, data=data)
    logger.info('Sent push notification')

if __name__=="__main__":
    try:
        main()
    except Exception:
        logger.error(traceback.format_exc())
