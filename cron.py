import requests
import os
from bs4 import BeautifulSoup

app_token = os.environ['PUSHOVER_APP_TOKEN']
user_key = os.environ['PUSHOVER_USER_KEY']
filename = os.environ['STATE_FILE_PATH']

if not os.path.exists(filename):
    open(filename, 'w+').close()
    with open(filename, 'a') as f:
        f.write('nil')

filecontent = ""
with open(filename,'r') as f:
    filecontent = f.read()

festool_url = 'https://www.festoolrecon.com/'
r = requests.get(festool_url)
soup = BeautifulSoup(r.text, 'html.parser')
title = soup.find('h1', attrs={'class': 'product-single__title'}).text

if title != filecontent:
    print(f'The Festool Recon Offering has changed to "{title}"')
    with open(filename, 'w') as f:
        f.write(title)
else:
    print(f'The Festool Recon Offering is still "{filecontent}"')
    exit(0)

message = f'The Festool Recon Offering is "{title}"'
data = {
	'token': app_token,
	'user': user_key,
	'message': message
}

print('Sending push notification')
pushover_url = "https://api.pushover.net/1/messages.json"
requests.post(pushover_url, data=data)
