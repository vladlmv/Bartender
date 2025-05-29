from django.forms import DateTimeField
from sqlalchemy import Column, Integer, String, Text, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship
from passlib.context import CryptContext  # Импортируем для хеширования

# Создаем объект Metadata
metadata = MetaData()

# Создаем базовый класс с использованием этого объекта Metadata
Base = declarative_base(metadata=metadata)

# Создаем объект для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False)
    _password = Column("password", Text, nullable=False)  # Изменили название столбца, чтобы скрыть пароль

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        """Хешируем пароль перед установкой."""
        self._password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверка пароля."""
        return pwd_context.verify(password, self._password)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_registration = Column(String(20), nullable=True)
    login = Column(String(50), unique=True, nullable=False)
    _password = Column("password", Text, nullable=False)  # Изменили название столбца

    user_ingredients = relationship("UserIngredient", back_populates="user")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        """Хешируем пароль перед установкой."""
        self._password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверка пароля."""
        return pwd_context.verify(password, self._password)


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    user_ingredients = relationship("UserIngredient", back_populates="ingredient")
    cocktails = relationship("Cocktail", back_populates="ingredient")
    cocktail_ingredients = relationship("CocktailIngredient", back_populates="ingredient")


class UserIngredient(Base):
    __tablename__ = 'user_ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="user_ingredients")
    ingredient = relationship("Ingredient", back_populates="user_ingredients")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    cocktails = relationship("Cocktail", back_populates="category")


class Cocktail(Base):
    __tablename__ = 'cocktails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    instructions = Column(Text)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE'))

    category = relationship("Category", back_populates="cocktails")
    ingredient = relationship("Ingredient", back_populates="cocktails")

    # исправлено здесь
    cocktail_ingredients = relationship('CocktailIngredient', back_populates='cocktail')


class CocktailIngredient(Base):
    __tablename__ = 'cocktail_ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cocktail_id = Column(Integer, ForeignKey('cocktails.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False)

    # должно совпадать с 'cocktail_ingredients' выше
    cocktail = relationship("Cocktail", back_populates="cocktail_ingredients")
    ingredient = relationship("Ingredient", back_populates="cocktail_ingredients")
