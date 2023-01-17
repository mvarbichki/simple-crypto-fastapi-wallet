from fastapi import FastAPI
from routers import transactions, reports
# install uvicorn, python-dotenv,mysql-connector-python, yagmail, email-validator


app = FastAPI(
    title="Simple C-Hot Wallet",
    version="0.1.0",
    description="Cryptocurrency wallet for BTC, ETH, ADA, LTC",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}  # hide schemas from swagger documentation
)

# integrate api routers
app.include_router(transactions.router)
app.include_router(reports.router)
