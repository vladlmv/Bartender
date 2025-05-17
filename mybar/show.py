from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mybar.myapp import Cocktail, Ingredient  # Импорт моделей

# Подключение к базе данных
engine = create_engine("postgresql://postgres:1928@localhost/postgres")
Session = sessionmaker(bind=engine)
session = Session()


def get_ingredients_for_cocktail(cocktail_name):
    # Получаем коктейль по названию
    cocktail = session.query(Cocktail).filter_by(name=cocktail_name).first()

    if not cocktail:
        print(f"Коктейль с названием '{cocktail_name}' не найден.")
        return

    # Получаем все ингредиенты, которые входят в этот коктейль
    ingredients = [cocktail_ingredient.ingredient.name for cocktail_ingredient in cocktail.cocktail_ingredients]

    print(f"Ингредиенты коктейля '{cocktail_name}':")
    for ingredient in ingredients:
        print(ingredient)


# Пример вызова функции
get_ingredients_for_cocktail("Mojito")  # Замените на название коктейля, который хотите найти
