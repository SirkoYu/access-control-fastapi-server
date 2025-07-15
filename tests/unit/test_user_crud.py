from unittest.mock import patch

import pytest
from src.schemas.user import UserCreate, UserUpdate, UserUpdatePatrical
from tests.conftest import hash_password
import src.crud.user as crud

@pytest.mark.asyncio
@patch("src.crud.user.hash_password", hash_password)
async def test_create_and_get_user(db_session):
    user_in = UserCreate(
        first="John",
        last="Doe",
        email="john@example.com",
        password="securepass",
    )
    user = await crud.create_user(user_in, db_session)

    assert user.id is not None
    assert user.first == "John"
    assert user.last == "Doe"
    assert user.email == "john@example.com"
    assert user.password_hash.startswith("hashed-")

    fetched = await crud.get_user(db_session, user.id)
    assert fetched is not None
    assert fetched.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    user = await crud.create_user(UserCreate(
        first="Alice", last="Smith", email="alice@example.com", password="123456"
    ), db_session)
    found = await crud.get_user_by_email(db_session, "alice@example.com")
    assert found is not None
    assert found.id == user.id


@pytest.mark.asyncio
@patch("src.crud.user.hash_password", hash_password)
async def test_update_user(db_session):
        user = await crud.create_user(UserCreate(
            first="Old", last="Name", email="old@example.com", password="pass"
        ), db_session)

        updated = await crud.update_user(db_session, UserUpdate(
            first="New", last="Name", email="new@example.com", password="newpass"
        ), user)

        assert updated.first == "New"
        assert updated.email == "new@example.com"
        assert updated.password_hash == "hashed-newpass"


@pytest.mark.asyncio
async def test_partial_update_user(db_session):
        user = await crud.create_user(UserCreate(
            first="Part", last="User", email="part@example.com", password="pwd"
        ), db_session)

        patched = await crud.update_user(db_session, UserUpdatePatrical(
            first="Changed"
        ), user, partial=True)

        assert patched.first == "Changed"
        assert patched.last == "User"


@pytest.mark.asyncio
async def test_delete_user(db_session):
        user = await crud.create_user(UserCreate(
            first="Delete", last="Melody", email="delete@example.com", password="del"
        ), db_session)

        await crud.delete_user(db_session, user)
        found = await crud.get_user(db_session, user.id)
        assert found is None


@pytest.mark.asyncio
async def test_get_users(db_session):
        await crud.create_user(UserCreate(
            first="Anna", last="Smith", email="a@example.com", password="abc123"
        ), db_session)
        await crud.create_user(UserCreate(
            first="Bob", last="Brown", email="b@example.com", password="def456"
        ), db_session)

        users = await crud.get_users(db_session)
        assert len(users) >= 2


@pytest.mark.asyncio
async def test_get_users_with_roles(db_session):
        user = await crud.create_user(UserCreate(
            first="Role", last="Test", email="role@example.com", password="test"
        ), db_session)
        users = await crud.get_users_with_roles(db_session)
        assert any(u.id == user.id for u in users)


@pytest.mark.asyncio
async def test_get_user_with_roles(db_session):
        user = await crud.create_user(UserCreate(
            first="Single", last="Role", email="singlerole@example.com", password="123"
        ), db_session)
        result = await crud.get_user_with_roles(db_session, user.id)
        assert result is not None
        assert result.id == user.id


@pytest.mark.asyncio
async def test_get_users_with_access_logs(db_session):
        user = await crud.create_user(UserCreate(
            first="Log", last="Test", email="log@example.com", password="log"
        ), db_session)
        users = await crud.get_users_with_access_logs(db_session)
        assert any(u.id == user.id for u in users)


@pytest.mark.asyncio
async def test_get_user_with_access_logs(db_session):
        user = await crud.create_user(UserCreate(
            first="Access", last="One", email="access@example.com", password="111"
        ), db_session)
        result = await crud.get_user_with_accesslogs(db_session, user.id)
        assert result is not None
        assert result.id == user.id


@pytest.mark.asyncio
async def test_get_users_with_current_presence(db_session):
        user = await crud.create_user(UserCreate(
            first="Presence", last="All", email="presence@example.com", password="pres"
        ), db_session)
        users = await crud.get_users_with_current_presence(db_session)
        assert any(u.id == user.id for u in users)


@pytest.mark.asyncio
async def test_get_user_with_current_presence(db_session):
        user = await crud.create_user(UserCreate(
            first="Presence", last="One", email="cp@example.com", password="111"
        ), db_session)
        result = await crud.get_user_with_current_presence(db_session, user.id)
        assert result is not None
        assert result.id == user.id
