from pathlib import Path
import src.app as app
import json

def test_model_exists():
    arquivo_path = Path("model/model.pkl")
    assert arquivo_path.is_file(), "Model file does not exist at the specified path."

def test_model_version_exists():
    arquivo_path = Path("model/model_metadata.json")
    assert arquivo_path.is_file(), "Model version file does not exist at the specified path."

def test_handler_call():
    payload = {
        "Age": "40",
        "Annual_Income": "100000",
        "Monthly_Inhand_Salary": "8000",
        "Num_Bank_Accounts": "2",
        "Num_Credit_Card": "4",
        "Interest_Rate": "10",
        "Num_of_Loan": "2",
        "Delay_from_due_date": "4",
        "Num_of_Delayed_Payment": "11",
        "Changed_Credit_Limit": "6",
        "Num_Credit_Inquiries": "3",
        "Outstanding_Debt": "2000",
        "Credit_Utilization_Ratio": "30",
        "Credit_History_Age": "200",
        "Total_EMI_per_month": "50",
        "Amount_invested_monthly": "250",
        "Monthly_Balance": "400",
        "Occupation": "Doctor",
        "Credit_Mix": "Good",
        "Payment_of_Min_Amount": "No",
        "Payment_Behaviour": "High_spent_Large_value_payments"
    }

    event = {"data": payload}
    response = app.handler(event, None)

    response['body'] = json.loads(response['body'])

    assert isinstance(response["body"]["prediction"], int), "Prediction should be an integer"
    assert response["body"]["prediction"] > 0, "Prediction should be a non-negative integer"
    assert response["statusCode"] == 200, "Status code should be 200 OK"