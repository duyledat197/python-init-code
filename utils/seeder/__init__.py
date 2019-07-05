from config import UserRole, EMAIL_ADMIN, DEFAULT_PASSWORD_ADMIN
from model import User
from model.db import db


def init_admin():
    try:
        admin_existed = db.session.query(User.query.filter(User.role == UserRole.ADMIN.value).exists()).scalar()
        if admin_existed:
            return
        user_admin = User(
            role=UserRole.ADMIN.value,
            email=EMAIL_ADMIN,
            name='admin'
        )
        user_admin.set_password(DEFAULT_PASSWORD_ADMIN)
        user_admin.save(session=db.session)
    except Exception as e:
        print(f'error init admin: {str(e)}')
