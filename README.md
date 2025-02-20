# Bartender
1. Концепция приложения.
Приложение будет помогать пользователям создавать коктейли как на основе только имеющихся ингредиентов, так и ингредиентов, которые необходимо приобрести. 
2. Схема БД.
•  USERS (пользователи)
•	id (SERIAL, PK) – уникальный идентификатор пользователя
•	username (VARCHAR(50), UNIQUE, NOT NULL) – имя пользователя
•	password (TEXT, NOT NULL) – пароль
•  USER_INGREDIENTS (ингредиенты пользователя)
•	id (SERIAL, PK) – уникальный идентификатор
•	user_id (INTEGER, FK → USERS.id, ON DELETE CASCADE) – связь с пользователем
•	ingredient_id (INTEGER, FK → INGREDIENTS.id, ON DELETE CASCADE) – связь с ингредиентом
•  INGREDIENTS (ингредиенты)
•	id (SERIAL, PK) – уникальный идентификатор ингредиента
•	name (VARCHAR(100), UNIQUE, NOT NULL) – название ингредиента
•  COCKTAILS (коктейли)
•	id (SERIAL, PK) – уникальный идентификатор коктейля
•	name (VARCHAR(100), UNIQUE, NOT NULL) – название коктейля
•	category_id (INTEGER, FK → CATEGORIES.id, NOT NULL) – категория коктейля
•	instructions (TEXT) – рецепт приготовления
•	ingredient_id (INTEGER, FK → INGREDIENTS.id, ON DELETE CASCADE) – ингредиент
•  CATEGORIES (категории коктейлей)
•	id (SERIAL, PK) – уникальный идентификатор
•	name (VARCHAR(50), UNIQUE, NOT NULL) – название категории
 ![image](https://github.com/user-attachments/assets/a80320cc-3901-4950-a7e0-0edf68f2589c)

Схема отношений:
•	USERS (1) → (∞) USER_INGREDIENTS (∞) ← (1) INGREDIENTS
•	COCKTAILS (∞) → (1) CATEGORIES
•	COCKTAILS (∞) ↔ (∞) INGREDIENTS (через COCKTAIL_INGREDIENTS)
3. API схема.
1. Аутентификация
•	POST /api/auth/register/ – Регистрация нового пользователя
•	POST /api/auth/login/ – Вход пользователя
•	POST /api/auth/logout/ – Выход пользователя
2. Ингредиенты
•	GET /api/ingredients/ – Получить список всех ингредиентов
3. Ингредиенты пользователя
•	GET /api/user-ingredients/ – Получить список ингредиентов текущего пользователя
4. Коктейли
•	GET /api/cocktails/ – Получить список всех коктейлей
•	GET /api/cocktails/{id}/ – Получить информацию о конкретном коктейле
•	POST /api/cocktails/ – Добавить новый коктейль (для администраторов)
•	DELETE /api/cocktails/{id}/ – Удалить коктейль (для администраторов)
5. Поиск коктейлей по ингредиентам
•	GET /api/cocktails/by-ingredients/ – Получить коктейли, которые можно приготовить из имеющихся ингредиентов пользователя
•	GET /api/cocktails/missing-ingredients/ – Получить коктейли, для которых не хватает ингредиентов, с указанием недостающих продуктов
6. Категории коктейлей
•	GET /api/categories/ – Получить список всех категорий
•	GET /api/categories/{id}/ – Получить информацию о конкретной категории
•	POST /api/categories/ – Добавить новую категорию (для администраторов)
•	DELETE /api/categories/{id}/ – Удалить категорию (для администраторов)
4. Используемые технологии
Front: HTML + CSS
Back: python, django
БД: PostgresSQL

