import json
import urllib2
import webbrowser

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
    req = urllib2.Request("https://svcs.sandbox.paypal.com/AdaptivePayments/Pay/", json.dumps(payload), heads)
    pay_key = json.loads(urllib2.urlopen(req).read())['payKey']
    webbrowser.open_new_tab("https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="+pay_key)