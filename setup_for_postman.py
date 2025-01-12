import asyncio

try:
    from app.core.init_db import create_user
except (ImportError, NameError) as e:
    raise ImportError(
        'Не удалось импортировать функцию `create_user` из модуля '
        '`app.core.init_db`. Создайте суперпользователя самостоятельно.'
    ) from e


class UserCreationError(Exception):
    """Ошибка при создании пользователя."""


if __name__ == '__main__':
    try:
        asyncio.run(create_user('root@admin.ru', 'root', is_superuser=True))
    except Exception as e:
        raise UserCreationError(
            'Не удалось создать суперпользователя. Создайте '
            'суперпользователя самостоятельно, используя следующие учетные '
            'данные:\n'
            'email: root@admin.ru\n'
            'password: root'
        ) from e
