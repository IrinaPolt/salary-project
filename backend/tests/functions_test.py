import pytest

from httpx import AsyncClient
from fastapi import FastAPI, Depends

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)


NEW_USER = {
    "email": "test@mail.ru",
    "first_name": "Test",
    "last_name": "Test",
    "password": "password"
}

NEW_PROMOTION = {
    "user_id": 1,
    "position": "test position",
    "promotion_date": "2024-06-08 02:15:00"
}

NEW_WAGE = {
    "user_id": 1,
    "rate": 100
}


class TestRoutes:

    @pytest.mark.asyncio
    async def test_users_route_exists(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("users:create-user"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_users_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("users:create-user"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_promotions_route_exists(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("promotions:create-promotion"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_promotions_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("promotions:create-promotion"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_wages_route_exists(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("wages:create-wage"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_wages_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("wages:create-wage"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_valid_input_creates_user(
            self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(
            app.url_path_for("users:create-user"),
            json={"new_user": NEW_USER})
        assert res.status_code == HTTP_201_CREATED
        assert NEW_USER["first_name"] == res.json()["first_name"]
        assert NEW_USER["last_name"] == res.json()["last_name"]
        assert NEW_USER["email"] == res.json()["email"]


class TestCreatePromotion:
    @pytest.mark.asyncio
    async def test_valid_input_creates_promotion(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(
            app.url_path_for("promotions:create-promotion"),
            json={"new_promotion": NEW_PROMOTION})
        assert res.status_code == HTTP_201_CREATED
        assert NEW_PROMOTION["user_id"] == res.json()["user_id"]
        assert NEW_PROMOTION["position"] == res.json()["position"]


class TestCreateWage:
    @pytest.mark.asyncio
    async def test_valid_input_creates_wage(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(
            app.url_path_for("wages:create-wage"),
            json={"new_wage": NEW_WAGE})
        assert res.status_code == HTTP_201_CREATED
        assert NEW_WAGE["user_id"] == res.json()["user_id"]
        assert NEW_WAGE["rate"] == res.json()["rate"]


class TestAuth:

    @pytest.mark.asyncio
    async def test_login(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        data = {
            "email": NEW_USER["email"],
            "password": NEW_USER["password"]
        }
        res = await client.post(
            app.url_path_for("users:login"),
            params=data)

        assert res.status_code == HTTP_200_OK
        assert "access_token" in res.json()

    @pytest.mark.asyncio
    async def test_protected_info(
            self, app: FastAPI, client: AsyncClient
    ) -> None:
        data = {
            "email": NEW_USER["email"],
            "password": NEW_USER["password"]
        }
        res = await client.post(
            app.url_path_for("users:login"),
            params=data)
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        res = await client.get(
            app.url_path_for("users:check"),
            headers=headers)
        assert res.status_code == HTTP_200_OK
        assert res.json()["rate"] == NEW_WAGE["rate"]
        assert res.json()["position"] == NEW_PROMOTION["position"]
