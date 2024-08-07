from market import db
from sqlalchemy import String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from market import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement='auto')
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False, default=1000)
    items: Mapped[list["Item"]] = relationship("Item", back_populates='owned_user')

    def __repr__(self) -> str:
        return f"User: {self.username}"
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def does_password_match(self, attemped_password: str):
        return bcrypt.check_password_hash(self.password_hash, attemped_password)


class Item(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement='auto')
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    barcode: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True, unique=False)
    owner : Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    owned_user: Mapped["User"] = relationship("User", back_populates='items')

    def __repr__(self) -> str:
        return f"Item: {self.name}"
