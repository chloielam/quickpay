from fastapi import FastAPI

from app.transactions.transactions_routes import router as transactions_router
from app.users.users_routes import router as users_router


app = FastAPI(
    title="QuickPay",
    description="A digital micro-payment system"
)

app.include_router(transactions_router)
app.include_router(users_router)

@app.get("/")

def check_health():
    return {"message": "QuickPay is running!"}
