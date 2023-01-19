# simple-crypto-wallet
Please note that the project aims to show Python-MySQL DB interactions, but not to work as a real crypto wallet.
The app receives and sends cryptocurrency and writes all activities in the DB.
It could show reports for all or single transactions and send the report to email by demand.
The app shows the actual price for a cryptocurrency and calculates it by a given quantity in USD, EUR, or BGN
(keep in mind that the site API refreshes every 60 seconds for crypto price changes). Uploading of the .env file is skipped for security reasons.

The database is located in the railway.app. The app is deployed on deta.sh and can be tested here: https://ctotbg.deta.dev/docs#/

DB tables are truncate daily (at 23:59 GMT+2) by tables_cleaning_script.py via Windows Task Scheduler to prevent the database from overflowing.
