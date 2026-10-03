from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.security.dependencies import get_current_user
from app.services.bill_extraction_service import extract_bill_data


client = TestClient(app)


CEB_BILL_TEXT = """
Ceylon Electricity Board
Account Number: CEB-1048821
Billing Month: 2026-10
Previous Meter Reading: 18420
Current Meter Reading: 18888
Consumption: 468 kWh
Amount Due: LKR 17,840.00
"""


def test_extracts_required_ceylon_electricity_board_fields():
    result = extract_bill_data(
        CEB_BILL_TEXT,
        "household-bill.txt",
    )

    assert result.provider == "CEB"
    assert result.account_number == "CEB-1048821"
    assert str(result.billing_month) == "2026-10-01"
    assert float(result.consumption_kwh) == 468
    assert float(result.bill_amount_lkr) == 17840
    assert result.confidence == "high"
    assert result.confidence_score == 1.0


def test_calculates_consumption_from_meter_readings():
    result = extract_bill_data(
        """
        Lanka Electricity Company (LECO)
        Account No: LECO-778821
        Billing Month: October 2026
        Previous Reading: 9250
        Current Reading: 9515
        Total Amount: Rs. 12,950.00
        """,
        "leco-bill.txt",
    )

    assert result.provider == "LECO"
    assert float(result.consumption_kwh) == 265
    assert any(
        "calculated from" in warning.lower()
        for warning in result.warnings
    )


def test_extracts_pdf_table_style_header():
    result = extract_bill_data(
        """
        Account Number Customer Type Billing Month
        CEB-1048821 Household 2026-10
        Consumption 468 kWh
        Amount Due LKR 17,840.00
        """,
        "table-bill.txt",
    )

    assert result.account_number == "CEB-1048821"
    assert str(result.billing_month) == "2026-10-01"


def test_bill_extraction_requires_authentication():
    response = client.post(
        "/api/v1/energy/me/bills/extract",
        files={
            "file": (
                "bill.txt",
                CEB_BILL_TEXT,
                "text/plain",
            )
        },
    )

    assert response.status_code in {401, 403}


def test_authenticated_user_can_extract_bill():
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=44,
        is_active=True,
    )

    try:
        response = client.post(
            "/api/v1/energy/me/bills/extract",
            files={
                "file": (
                    "bill.txt",
                    CEB_BILL_TEXT,
                    "text/plain",
                )
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["consumption_kwh"] == "468"
