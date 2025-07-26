from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
import json
import os

app = FastAPI()

# ----------- Helper functions to load/save data -----------

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# ----------- Load existing data (or empty dicts) -----------

loans = load_data("loans.json")
transactions = load_data("transactions.json")

# ----------- Data Models -----------

class LoanRequest(BaseModel):
    customer_id: str
    principal: float
    years: int
    rate: float

class PaymentRequest(BaseModel):
    loan_id: str
    amount_paid: float

# ----------- Loan API -----------

@app.post("/loan")
def lend(loan: LoanRequest):
    loan_id = f"{loan.customer_id}_{len(loans)+1}"
    total_emis = loan.years * 12
    r = loan.rate / (12 * 100)

    if r == 0:
        emi = loan.principal / total_emis
    else:
        emi = loan.principal * r * math.pow(1 + r, total_emis) / (math.pow(1 + r, total_emis) - 1)

    total_amount = round(emi * total_emis, 2)
    emi = round(emi, 2)

    loans[loan_id] = {
        "customer_id": loan.customer_id,
        "principal": loan.principal,
        "years": loan.years,
        "rate": loan.rate,
        "total_amount": total_amount,
        "monthly_emi": emi,
        "emis_left": total_emis
    }
    transactions[loan_id] = []

    save_data("loans.json", loans)
    save_data("transactions.json", transactions)

    return {"loan_id": loan_id, "total_amount": total_amount, "monthly_emi": emi}

# ----------- Payment API -----------

@app.post("/payment")
def make_payment(payment: PaymentRequest):
    loan_id = payment.loan_id

    if loan_id not in loans:
        raise HTTPException(status_code=404, detail="Loan ID not found")

    loan = loans[loan_id]

    if loan["emis_left"] <= 0:
        raise HTTPException(status_code=400, detail="Loan fully paid")

    expected_emi = loan["monthly_emi"]
    if payment.amount_paid < expected_emi:
        raise HTTPException(status_code=400, detail=f"Minimum EMI payment should be {expected_emi}")

    loan["total_amount"] = round(loan["total_amount"] - payment.amount_paid, 2)
    loan["emis_left"] -= 1
    transactions[loan_id].append(payment.amount_paid)

    save_data("loans.json", loans)
    save_data("transactions.json", transactions)

    return {
        "message": "Payment received",
        "remaining_amount": loan["total_amount"],
        "emis_left": loan["emis_left"]
    }

# ----------- View Loan Details -----------

@app.get("/loan/{loan_id}")
def get_loan(loan_id: str):
    if loan_id not in loans:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loans[loan_id]

# ----------- View All Payments -----------

@app.get("/transactions/{loan_id}")
def get_transactions(loan_id: str):
    if loan_id not in transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return {"payments": transactions[loan_id]}
