import random
import json
from enum import Enum
from db import extract_key
import yagmail
from os import environ as env
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr
from requests import Session


# fake crypto privet key generator
def currency_privet_key_generator():
    key = ''.join(
        (random.choice("AaBbCcDdEeFfGgHhIiKkLlMmNnOoPpQqRrSsTtVvXxYyZz0123456789") for i in range(5)))
    return key


def refer_to_key(crypto_name):
    key = extract_key(crypto_name)
    return key


# dropdown menu
class CryptoList(str, Enum):
    btc = "Bitcoin"
    eth = "Ethereum"
    ada = "Cardano"
    ltc = "Litecoin"


# dropdown menu
class RecipientList(str, Enum):
    exc = "to some exchange"
    rec = "to some recipient"


# dropdown menu
class ReportList(str, Enum):
    at = "All transactions"
    btc = "Bitcoin"
    eth = "Ethereum"
    ada = "Cardano"
    ltc = "Litecoin"


# dropdown menu
class CurrencyList(str, Enum):
    usd = "USD"
    eur = "EUR"
    bgn = "BGN"


def send_mail(email_to, report_name, report):
    try:
        # create SMTP instance. Credentials are stored in .env
        yag = yagmail.SMTP(env.get("GMAIL_ADDRESS"), env.get("GMAIL_APP_PWD"))
        yag.send(email_to, f"Simple C-Hot Wallet report: {report_name}", report)

    # handle sending issues
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unable to send the email {e}")


# check for valid email
class ValidateEmail(BaseModel):
    email: EmailStr


# get crypto prices from coinmarketcap.com
def get_crypto_price(crypto_name, currency):
    # handle problems
    try:
        url = env.get("COINMARKETCAP_URL")
        lower_cn = crypto_name.lower()
        second_layer = ""

        # sets the second layer for the different currencies since on the website they are different for each crypto
        if lower_cn == "bitcoin":
            second_layer = "1"
        elif lower_cn == "ethereum":
            second_layer = "1027"
        elif lower_cn == "cardano":
            second_layer = "2010"
        elif lower_cn == "litecoin":
            second_layer = "2"

        parameters = {
            "slug": lower_cn,
            "convert": currency
        }

        headers = {
            "Accepts": "application/json",  # return json format as response
            "X-CMC_PRO_API_KEY": env.get("COINMARKETCAP_API")  # API key
        }

        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)

        # load in json format and get only the price
        res = json.loads(response.text)["data"][second_layer]["quote"][currency]["price"]

        return round(res, 2)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unable to retrieve data: {e}")
