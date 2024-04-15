# Simple crypto wallet

FEATURES

The project aims to show Python-MySQL interactions (via SQL statements), but not to work as a real crypto wallet.
The app receives and sends cryptocurrency and writes all activities in the database.
It can show reports for all or single transactions and send the report to email by demand.
The app shows the actual price for a cryptocurrency and calculates it by a given quantity in USD, EUR, or BGN via API. The site API refreshes every 60 seconds for crypto price changes.
It can be tested via the FastAPI web endpoint - localhost/docs.
In addition, tables_cleaning_script.py is used to truncate tables to data for testing purposes and writing logs about this event.
