import logging
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Получение базы данных пользователей."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Получение стратегии JWT."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],  # type: ignore
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters',
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail',
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        logger.info('Пользователь %s зарегистрирован.', user.email)


async def get_user_manager(user_db=Depends(get_user_db)):
    """Получение менеджера пользователей."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
