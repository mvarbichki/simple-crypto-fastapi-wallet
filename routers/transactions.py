from fastapi import APIRouter, HTTPException, status
from mysql.connector import Error
from utilities import CryptoList, currency_privet_key_generator, refer_to_key, RecipientList
from db import deposit_new_crypto, extract_name_column, add_to_existing_crypto, subtract_from_existing_crypto, \
    extract_owned_assets, extract_single_quantity, send_whole_crypto, activity_record

router = APIRouter(tags=["transactions"])


@router.post("/deposit_cryptocurrency")
def deposit_cryptocurrency(crypto_name: CryptoList, quantity: int):
    # handle connection issues
    try:

        # restrict acceptable quantity
        if not 1 <= quantity <= 1000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Allowed quantity is from 1(min) to 1000(max).")

        # after the checks add the transfer info to activity table
        activity_record("received", crypto_name, quantity, "you")

        # if crypto is already in the DB it will add the desired quantity to the existing currency
        if crypto_name in extract_name_column():
            add_to_existing_crypto(quantity, crypto_name)
            return {"transaction status": f"{quantity} {crypto_name}/s added to assets successfully!"}
        # if crypto not in the DB it will create it
        else:
            # generate private key bound to the given crypto
            privet_key = currency_privet_key_generator()
            deposit_new_crypto(crypto_name, quantity, privet_key)
            return {"transaction status": f"{quantity} {crypto_name}/s received successfully!"}

    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


@router.delete("/send_cryptocurrency")
def send_cryptocurrency(crypto_name: CryptoList, recipient: RecipientList, quantity: int):
    # handle connection issues
    try:

        # check if user own the crypto
        if crypto_name in extract_name_column():

            total_current_quantity = extract_single_quantity(crypto_name)

            # refers to the currency private key to proceed the transaction
            key = refer_to_key(crypto_name)

            # sent a portion of the crypto
            if (1 <= quantity < total_current_quantity) and (quantity != total_current_quantity):
                subtract_from_existing_crypto(quantity, crypto_name)

                # after the checks add the transfer info to activity table
                activity_record("sent", crypto_name, quantity, recipient)

                return {"transaction status": f"{quantity} {crypto_name}/s sent successfully!"
                                              f" Key: {key[:2]}" + "*******"}
            # sent all of a crypto
            elif quantity == total_current_quantity:
                send_whole_crypto(crypto_name)

                # after the checks add the transfer info to activity table
                activity_record("sent", crypto_name, quantity, recipient)

                return {"transaction status": f"All {quantity} {crypto_name}/s sent successfully!"
                                              f" Key: {key[:2]}" + "*******"}
            # handles wrong quantity
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Can not send {quantity} of {crypto_name}!"
                                           f" You own {total_current_quantity}. Please enter a valid quantity")

        #  handles the case when the user try to send asset that are not exists in the wallet
        else:
            # empty wallet case
            if not extract_name_column():
                msg = "No assets in the wallet."
            else:
                msg = f"You do not own {crypto_name}! Owned asset/s: {extract_owned_assets()}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=msg)
    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
