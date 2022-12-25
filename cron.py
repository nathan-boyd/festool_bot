import requests
import os
from bs4 import BeautifulSoup

url = 'https://www.festoolrecon.com/'

app_token = os.getenv('PUSHOVER_APP_TOKEN')
if not app_token:
    raise Exception('PUSHOVER_USER_KEY not set!')

user_key = os.getenv('PUSHOVER_USER_KEY')
if not user_key:
    raise Exception('PUSHOVER_USER_KEY not set!')

filename = "/tmp/festool_state.txt"
if not os.path.exists(filename):
    open(filename, 'w+').close()
    with open(filename, 'a') as f:
        f.write('nil')

filecontent = ""
with open(filename,'r') as f:
    filecontent = f.read()


# requesting to get the content of the url
r = requests.get(url)

# parsing the html content
soup = BeautifulSoup(r.text, 'html.parser')

# getting the value of 'product-single__title' element
title = soup.find('h1', attrs={'class': 'product-single__title'}).text

message = f'The FestoolRecon Offering is "{title}"'

if title != filecontent:
    print(f'The Festool Recon Offering has changed to {title}')
    with open(filename, 'w') as f:
        f.write(title)
else:
    print(f'The Festool Recon Offering is still {filecontent}')
    exit(0)

print('sending push notification')

#push notification to iPhone using Pushover API
url = "https://api.pushover.net/1/messages.json"

#data to be sent to Pushover API
data = {
	'token': app_token,
	'user': user_key,
	'message': message
}

#send the request
requests.post(url, data=data)
