import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_wallet(client: AsyncClient):
    """Тест создания кошелька."""
    response = await client.post("/api/v1/wallets")
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["balance"] == "0.00"


@pytest.mark.asyncio
async def test_get_wallet(client: AsyncClient):
    """Тест получения информации о кошельке."""
    create_response = await client.post("/api/v1/wallets")
    assert create_response.status_code == status.HTTP_201_CREATED
    wallet_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert "balance" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_deposit_operation(client: AsyncClient):
    """Тест операции пополнения."""
    operation_data = {"operation_type": "DEPOSIT", "amount": 1000.00}
    create_response = await client.post("/api/v1/wallets")
    assert create_response.status_code == status.HTTP_201_CREATED
    wallet_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert "last_operation" in data
    assert data["last_operation"] == operation_data["operation_type"]
    assert "balance" in data
    assert data["balance"] == "1000.00"

    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.json()["balance"] == "1000.00"

    operation_data["amount"] = -1
    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_withdraw_operation(client: AsyncClient):
    """Тест операции списания."""
    operation_data = {"operation_type": "DEPOSIT", "amount": 1000.00}
    create_response = await client.post("/api/v1/wallets")
    assert create_response.status_code == status.HTTP_201_CREATED
    wallet_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == status.HTTP_201_CREATED

    operation_data["operation_type"] = "WITHDRAW"
    operation_data["amount"] = 500
    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert "last_operation" in data
    assert data["last_operation"] == operation_data["operation_type"]
    assert response.json()["balance"] == "500.00"

    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.json()["balance"] == "500.00"


@pytest.mark.asyncio
async def test_insufficient_funds(client: AsyncClient):
    """Тест операции списания, когда на кошельке недостаточно средств."""
    operation_data = {"operation_type": "WITHDRAW", "amount": 1000.00}
    create_response = await client.post("/api/v1/wallets")
    assert create_response.status_code == status.HTTP_201_CREATED
    wallet_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation", json=operation_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_concurrent_operations(client: AsyncClient):
    """Тест конкурентных операций."""
    create_response = await client.post("/api/v1/wallets")
    assert create_response.status_code == status.HTTP_201_CREATED
    wallet_id = create_response.json()["id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "1000.00"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    tasks = []
    for _ in range(15):
        task = client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": "100.00"},
        )
        tasks.append(task)

    for _ in range(10):
        task = client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "WITHDRAW", "amount": "50.00"},
        )
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == status.HTTP_201_CREATED

    balance_response = await client.get(f"/api/v1/wallets/{wallet_id}")
    final_balance = float(balance_response.json()["balance"])
    assert final_balance == 2000.00  # 1000 + 15*100 - 10*50 = 2000
