import urllib2
import urllib
from urllib2 import HTTPRedirectHandler
import cookielib
from cookielib import CookieJar

REFERRAL_CODE = 'XXXXXX'
PASSWORD = 'zzzzzz'

def register_account(name):
    step1_params = {
        "nickname": name,
        "first_name" : "zzz",
        "last_name" : "zzz", 
        "email" : name + "@example.com",
        "email2" : name + "@example.com",
        "password1" : PASSWORD,
        "password2" : PASSWORD
        }
    step1_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer" : "http://heroesofnewerth.com/create_account.php",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7",
        }
    step1_data = urllib.urlencode(step1_params)

    step2_params = {
        "f": "purchaseNew",
        "promocode": "",
        "purchase_id": "",
        "nickname": name,
        "first_name": "zzzz",
        "last_name": "zzzz",
        "email" : name + "@example.com",
        "bill_first_name": "", 
        "bill_last_name": "",
        "card_number": "",
        "month": "01",
        "year": "2009",
        "cvv": "",
        "io_HoN_BBq": "",
        "zip": ""
        }
    step2_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer" : "http://heroesofnewerth.com/create_account2.php",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7",
        }
    step2_data = urllib.urlencode(step2_params)

    referral_url = "http://heroesofnewerth.com/ref.php?r=" + REFERRAL_CODE
    referral_request = urllib2.Request(referral_url)
    referral_response = urllib2.urlopen(referral_request)

    create_account_url = "http://heroesofnewerth.com/create_account.php"
    create_account_request = urllib2.Request(create_account_url, step1_data, step1_headers)
    create_account_response = urllib2.urlopen(create_account_request)
    
    cookies = CookieJar()
    cookies.extract_cookies(referral_response,referral_request)
    cookie_handler= urllib2.HTTPCookieProcessor( cookies )

    redirect_handler = HTTPRedirectHandler()
    
    opener = urllib2.build_opener(redirect_handler,cookie_handler)
    referral_response = opener.open(referral_request)
    create_response = opener.open(create_account_request)
    
    confirm_account_url = "http://heroesofnewerth.com/create_account2.php"
    confirm_account_request = urllib2.Request(confirm_account_url, step2_data, step2_headers)
    confirm_account_response = urllib2.urlopen(confirm_account_request)

    confirm_response = opener.open(confirm_account_request)

    return True
