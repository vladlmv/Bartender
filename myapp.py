from sqlalchemy import Column, Integer, String, Text, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship

# Создаем объект Metadata
metadata = MetaData()

# Создаем базовый класс с использованием этого объекта Metadata
Base = declarative_base(metadata=metadata)


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)

    user_ingredients = relationship("UserIngredient", back_populates="user")


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    user_ingredients = relationship("UserIngredient", back_populates="ingredient")
    cocktails = relationship("Cocktail", back_populates="ingredient")


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

class CocktailIngredient(Base):
    __tablename__ = 'cocktail_ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cocktail_id = Column(Integer, ForeignKey('cocktails.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False)

    cocktail = relationship("Cocktail", back_populates="cocktail_ingredients")
    ingredient = relationship("Ingredient", back_populates="cocktail_ingredients")