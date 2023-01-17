from fastapi import APIRouter, HTTPException, status
from mysql.connector import Error
from pydantic import ValidationError
from utilities import ReportList, send_mail, ValidateEmail, get_crypto_price, CryptoList, CurrencyList
from db import show_single_cryptocurrency_transactions, show_all_transactions, extract_activities_name_column,\
    show_wallet, extract_name_column

router = APIRouter(tags=["reports"])


@router.get("/show_wallet_content")
def show_wallet_content():
    # handle connection issues
    try:

        # empty wallet case
        if not extract_name_column():
            return "No assets in the wallet."
        # return wallet content
        else:
            return show_wallet()

    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


@router.get("/show_activities")
def show_activities(show_report_for: ReportList, enter_email_to_get_the_report: str = None):
    msg = ""

    # handle connection issues
    try:

        activities_crypto_names = extract_activities_name_column()

        # show all transactions for all currencies
        if (show_report_for == "All transactions") and activities_crypto_names:
            report = show_all_transactions()
        # show all transaction for given currency
        elif show_report_for in activities_crypto_names:
            report = show_single_cryptocurrency_transactions(show_report_for)
        # returns a message if try to invoke a report about currency not in the record
        else:
            report = "There are no such transactions."

        # send email if such is provided and report is not empty
        if enter_email_to_get_the_report and \
                (report != "There are no such transactions."):

            # check for valid email
            try:
                ValidateEmail(email=enter_email_to_get_the_report)
            except ValidationError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid email.")

            send_mail(enter_email_to_get_the_report, show_report_for, report)
            msg = f"Report is sent to email: {enter_email_to_get_the_report}"

        return report, msg

    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


@router.get("/exchange_rate")
def exchange_rate(crypto_name: CryptoList, currency: CurrencyList,
                  quantity_to_check: int):
    # restrict acceptable quantity
    if not 1 <= quantity_to_check <= 1000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Allowed quantity is from 1(min) to 1000(max).")

    selected_cripto_price = get_crypto_price(crypto_name, currency)
    res = quantity_to_check * selected_cripto_price

    return f"{quantity_to_check} {crypto_name}/s = {round(res, 2)} {currency}."
