import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headers = {
        # API credentials for the API caller business account
        'X-PAYPAL-SECURITY-USERID':    'hugoreinbergen-facilitator_api1.hotmail.com',
        'X-PAYPAL-SECURITY-PASSWORD':  '4SD6JYJ85P7HFTXP',
        'X-PAYPAL-SECURITY-SIGNATURE': 'AiPC9BjkCyDFQXbSkoZcgqH3hpacAH1rfUmkHaF9hKeEjxkZAZwdieE2',
        'X-PAYPAL-APPLICATION-ID':     'APP-80W284485P519543T',
        'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
        'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON'
    }

def paycall(email, amount, headers=headers):
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


def make_a_payment(target_email='example@gmail.com', price=0.01, own_email='mcgthe-buyer-1@gmail.com', password='lovelive'):
    url = paycall(target_email, price)
    driver = webdriver.Firefox()
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'loadLogin'))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'login_email'))
        ).send_keys(own_email)
        driver.find_element_by_id('login_password').send_keys(password)
        driver.find_element_by_id('submitLogin').click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'submit.x'))
        ).click()
    finally:
        driver.quit()
