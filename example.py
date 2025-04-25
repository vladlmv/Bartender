import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp import Base, Admin, User, Ingredient, Category, Cocktail, UserIngredient, CocktailIngredient

# Пример данных для записи в JSON-файл
data_to_save = {
    "users": [
        {"user_id": 1, "login": "john_doe", "password": "password123"},
        {"user_id": 2, "login": "jane_doe", "password": "password456"}
    ],
    "ingredients": [
        {"ingredient_id": 1, "name": "vodka"},
        {"ingredient_id": 2, "name": "lime"},
        {"ingredient_id": 3, "name": "mint"}
    ],
    "cocktails": [
        {"cocktail_id": 1, "name": "Mojito", "category_id": 1, "instructions": "Mix vodka, lime, mint with ice."},
        {"cocktail_id": 2, "name": "Bloody Mary", "category_id": 2, "instructions": "Mix vodka, lime, and spices."}
    ],
    "categories": [
        {"category_id": 1, "name": "Classic Cocktails"},
        {"category_id": 2, "name": "Spicy Cocktails"}
    ],
    "admins": [
        {"admin_id": 1, "login": "admin", "password": "adminpass"}
    ]
}

# Запись данных в JSON-файл
with open('data.json', 'w') as file:
    json.dump(data_to_save, file, indent=4)

# Подключение к базе данных
engine = create_engine('postgresql://postgres:1928@localhost/postgres')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Создание тестового администратора
admin1 = Admin(login='admin', password='adminpass')
session.add(admin1)

# Создание пользователей
user1 = User(login='john_doe', password='password123')
user2 = User(login='jane_doe', password='password456')
session.add_all([user1, user2])
session.flush()  # Чтобы присвоились id

# Создание ингредиентов
ingredient1 = Ingredient(name='vodka')
ingredient2 = Ingredient(name='lime')
ingredient3 = Ingredient(name='mint')
session.add_all([ingredient1, ingredient2, ingredient3])
session.flush()

# Добавление UserIngredients
user_ingredient1 = UserIngredient(user_id=user1.id, ingredient_id=ingredient1.id)
user_ingredient2 = UserIngredient(user_id=user1.id, ingredient_id=ingredient3.id)
user_ingredient3 = UserIngredient(user_id=user2.id, ingredient_id=ingredient2.id)
session.add_all([user_ingredient1, user_ingredient2, user_ingredient3])

# Создание категорий
category1 = Category(name='Classic Cocktails')
category2 = Category(name='Spicy Cocktails')
session.add_all([category1, category2])
session.flush()

# Создание коктейлей
cocktail1 = Cocktail(name='Mojito', category_id=category1.id, instructions='Mix vodka, lime, mint with ice.')
cocktail2 = Cocktail(name='Bloody Mary', category_id=category2.id, instructions='Mix vodka, lime, and spices.')
session.add_all([cocktail1, cocktail2])
session.flush()

# Связи CocktailIngredient
cocktail_ingredient1 = CocktailIngredient(cocktail_id=cocktail1.id, ingredient_id=ingredient1.id)  # vodka
cocktail_ingredient2 = CocktailIngredient(cocktail_id=cocktail1.id, ingredient_id=ingredient2.id)  # lime
cocktail_ingredient3 = CocktailIngredient(cocktail_id=cocktail1.id, ingredient_id=ingredient3.id)  # mint
cocktail_ingredient4 = CocktailIngredient(cocktail_id=cocktail2.id, ingredient_id=ingredient1.id)  # vodka
cocktail_ingredient5 = CocktailIngredient(cocktail_id=cocktail2.id, ingredient_id=ingredient2.id)  # lime
session.add_all([
    cocktail_ingredient1, cocktail_ingredient2, cocktail_ingredient3,
    cocktail_ingredient4, cocktail_ingredient5
])

# Вывод информации
print("\n--- Users ---")
for user in session.query(User).all():
    print(f'User ID: {user.id}, Login: {user.login}')

print("\n--- Ingredients ---")
for ingredient in session.query(Ingredient).all():
    print(f'Ingredient ID: {ingredient.id}, Name: {ingredient.name}')

print("\n--- Cocktails ---")
for cocktail in session.query(Cocktail).all():
    print(f'Cocktail ID: {cocktail.id}, Name: {cocktail.name}, Instructions: {cocktail.instructions}')

print("\n--- Admins ---")
for admin in session.query(Admin).all():
    print(f'Admin ID: {admin.id}, Login: {admin.login}')

# Сохранение и завершение сессии
session.commit()
session.close()

print("\nТестовые данные успешно добавлены в базу данных.")
