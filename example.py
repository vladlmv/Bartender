import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp import Base, Admin, User, Ingredient, Category, Cocktail, UserIngredient, CocktailIngredient

# Данные для JSON и базы
data_to_save = {
    "users": [
        {"login": "john_doe", "password": "password123"},
        {"login": "jane_doe", "password": "password456"}
    ],
    "ingredients": [
        {"name": "vodka"},
        {"name": "lime"},
        {"name": "mint"}
    ],
    "cocktails": [
        {"name": "Mojito", "category": "Classic Cocktails", "instructions": "Mix vodka, lime, mint with ice."},
        {"name": "Bloody Mary", "category": "Spicy Cocktails", "instructions": "Mix vodka, lime, and spices."}
    ],
    "categories": [
        {"name": "Classic Cocktails"},
        {"name": "Spicy Cocktails"}
    ],
    "admins": [
        {"login": "admin5", "password": "adminpass"}
    ]
}

# Сохраняем данные в JSON
with open('data.json', 'w') as file:
    json.dump(data_to_save, file, indent=4)

# Подключение к БД
engine = create_engine('postgresql://postgres:1928@localhost/postgres')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Создание администратора
    for admin_data in data_to_save['admins']:
        existing_admin = session.query(Admin).filter_by(login=admin_data['login']).first()
        if not existing_admin:
            admin = Admin(**admin_data)
            session.add(admin)
            print(f"Админ '{admin_data['login']}' создан.")
        else:
            print(f"Админ '{admin_data['login']}' уже существует.")

    # Создание пользователей
    users = []
    for user_data in data_to_save['users']:
        user = session.query(User).filter_by(login=user_data['login']).first()
        if not user:
            user = User(**user_data)
            session.add(user)
        users.append(user)
    session.flush()

    # Создание ингредиентов
    ingredients = []
    for ingredient_data in data_to_save['ingredients']:
        ingredient = session.query(Ingredient).filter_by(name=ingredient_data['name']).first()
        if not ingredient:
            ingredient = Ingredient(**ingredient_data)
            session.add(ingredient)
        ingredients.append(ingredient)
    session.flush()

    # Создание категорий
    categories = []
    for category_data in data_to_save['categories']:
        category = session.query(Category).filter_by(name=category_data['name']).first()
        if not category:
            category = Category(**category_data)
            session.add(category)
        categories.append(category)
    session.flush()

    # Создание коктейлей
    cocktails = []
    for cocktail_data in data_to_save['cocktails']:
        category = session.query(Category).filter_by(name=cocktail_data['category']).first()
        cocktail = session.query(Cocktail).filter_by(name=cocktail_data['name']).first()
        if not cocktail:
            cocktail = Cocktail(
                name=cocktail_data['name'],
                category_id=category.id,
                instructions=cocktail_data['instructions']
            )
            session.add(cocktail)
        cocktails.append(cocktail)
    session.flush()

    # Привязка UserIngredient
    user_ingredient_data = [
        (users[0], ingredients[0]),  # john_doe - vodka
        (users[0], ingredients[2]),  # john_doe - mint
        (users[1], ingredients[1])   # jane_doe - lime
    ]
    for user, ingredient in user_ingredient_data:
        link = session.query(UserIngredient).filter_by(user_id=user.id, ingredient_id=ingredient.id).first()
        if not link:
            session.add(UserIngredient(user_id=user.id, ingredient_id=ingredient.id))

    # Привязка CocktailIngredient
    cocktail_ingredient_data = [
        (cocktails[0], ingredients[0]),  # Mojito - vodka
        (cocktails[0], ingredients[1]),  # Mojito - lime
        (cocktails[0], ingredients[2]),  # Mojito - mint
        (cocktails[1], ingredients[0]),  # Bloody Mary - vodka
        (cocktails[1], ingredients[1])   # Bloody Mary - lime
    ]
    for cocktail, ingredient in cocktail_ingredient_data:
        link = session.query(CocktailIngredient).filter_by(cocktail_id=cocktail.id, ingredient_id=ingredient.id).first()
        if not link:
            session.add(CocktailIngredient(cocktail_id=cocktail.id, ingredient_id=ingredient.id))

    # Сохраняем
    session.commit()
    print("\n✅ Все тестовые данные успешно добавлены в базу данных.")

except Exception as e:
    session.rollback()
    print(f"\n❌ Ошибка при добавлении данных: {e}")

finally:
    session.close()
