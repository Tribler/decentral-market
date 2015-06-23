import json
import requests
from selenium import webdriver
import time

def paycall(email, amount):
    heads = {
        # API credentials for the API caller business account
        'X-PAYPAL-SECURITY-USERID':    'hugoreinbergen-facilitator_api1.hotmail.com',
        'X-PAYPAL-SECURITY-PASSWORD':  '4SD6JYJ85P7HFTXP',
        'X-PAYPAL-SECURITY-SIGNATURE': 'AiPC9BjkCyDFQXbSkoZcgqH3hpacAH1rfUmkHaF9hKeEjxkZAZwdieE2',
        'X-PAYPAL-APPLICATION-ID':     'APP-80W284485P519543T',
        'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
        'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON'
    }
    payload = {
        "actionType": "PAY",
        "currencyCode": "EUR",
        "receiverList": {
            "receiver": [{
                "amount": amount,
                "email": email
            }]
        },
        # where the sender is redirected
        "returnUrl": "http://google.com",
        "cancelUrl": "http://bing.com",
        "requestEnvelope": {
            "errorLanguage":"en_US",
            # error detail level
            "detailLevel":"ReturnAll"
        }
    }

    req = requests.post('https://svcs.sandbox.paypal.com/AdaptivePayments/Pay/', json.dumps(payload), headers=headers)
    pay_key = req.json()['payKey']
    return 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey=' + pay_key


def dothethings(target_email='example@gmail.com', amount=0.01, own_email='mcgthe-buyer-1@gmail.com', password='lovelive'):
    url = paycall(target_email, amount)
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_id('loadLogin').click()
    time.sleep(2)
    driver.find_element_by_id('login_email').send_keys(own_email)
    driver.find_element_by_id('login_password').send_keys(password)
    driver.find_element_by_id('submitLogin').click()
    time.sleep(2)
    driver.find_element_by_id('submit.x').click()
