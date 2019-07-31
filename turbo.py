import requests
import json
import threading
import time
import random

#deal with config.json

with open("config.json") as file:
    config = json.load(file)

username = config['username']
password = config['password']

targets = config['targetUsernames']

#this is so I can dynamically change the endpoint
endpoint = 'https://www.instagram.com/<username>/'


def turbo(nam):

    #login to instagram, create a session and get a csrf for later
    s = requests.session()

    print(f"[{nam}] Logging Into {username}...")
    url1 = "https://www.instagram.com/accounts/login/"

    r1 = s.get(url1)

    csrf1 = r1.cookies.get_dict()['csrftoken']

    url2 = 'https://www.instagram.com/accounts/login/ajax/'
    urlf = "https://www.instagram.com/accounts/edit/"

    h2 = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/login/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-csrftoken': csrf1,
        'x-instagram-ajax': '1',
        'x-requested-with': 'XMLHttpRequest'
    }

    data2 = {
        'username': username,
        'password': password,
        'queryParams': '{}'
    }

    r2 = s.post(url2, headers=h2, data=data2)

    if r2.json()['authenticated'] == False:
        print(f'[{nam}] ERROR LOGGING IN...')
        exit()

    csrf = r2.cookies.get_dict()['csrftoken']
    print(f'[{nam}] Logged In Initiating Turbo...')
    turboin = True

    hf = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/edit/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-csrftoken': csrf,
        'x-instagram-ajax': '1',
        'x-requested-with': 'XMLHttpRequest'
    }

    headers_my_data = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/edit/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-csrftoken': csrf,
        'x-instagram-ajax': '1',
        'x-requested-with': 'XMLHttpRequest'
    }

    my_data_response = s.get(urlf, headers=headers_my_data)

    #start monitoring the username
    while turboin == True:
        res = requests.get(endpoint.replace("<username>", nam))
        if res.status_code == 404:
            print(f'[{nam}] NAME AVAILABLE TAKING IT')

            dat1 = s.get(urlf, headers=hf)
            dat2=dat1.json()
            df = {
                'first_name': dat2['first_name'],
                'email': dat2['email'],
                'username': nam,
                'phone_number': dat2['phone_number'],
                'gender': dat2['gender'],
                'biography': dat2['biography'],
                'external_url': dat2['external_url'],
                'chaining_enabled': 'on'
            }
            #change the acc to the turbo name
            rf = s.post(urlf, headers=hf, data=df)
            print(f'[{nam}] Completed Turbo Killing Thread')
            turboin = False


if __name__ == '__main__':
    print("INSTATURBO")
    print("XO | TCWTEAM | @ehxohd")
    print("")
    print("-" * 30)
    print(f"Username: {username}")
    print("Password: {}".format("*" * len(password)))
    print("# Of Targets: {}".format(str(len(targets))))
    print(f"Endpoint: {endpoint}")
    print("-" * 30)
    print("")
    tin = input("Would you like to start (y/n)?: ")
    if tin.lower() == "y":
        for x in targets:
            #print(x)
            t = threading.Thread(target=turbo, args=(x, ))
            t.start()
    else:
        exit()
