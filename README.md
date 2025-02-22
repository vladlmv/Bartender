# Bartender
1. Концепция приложения.
Приложение будет помогать пользователям создавать коктейли как на основе только имеющихся ингредиентов, так и ингредиентов, которые необходимо приобрести.

3. Схема БД.

•  ADMINS (администраторы)

•	id (SERIAL, PK) – уникальный идентификатор администратора

•	login (VARCHAR(50), UNIQUE, NOT NULL) – имя администратора

•	password (TEXT, NOT NULL) – пароль

•  USERS (пользователи)

•	id (SERIAL, PK) – уникальный идентификатор пользователя

•	login (VARCHAR(50), UNIQUE, NOT NULL) – имя пользователя

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

 ![image](https://github.com/user-attachments/assets/12c1cd9c-a27e-4a34-8c55-ef1e99471f50)


Схема отношений:

•	ADMINS (1) → (∞) INGREDIENTS

•	ADMINS (1) → (∞) CATEGORIES

•	ADMINS (1) → (∞) COCKTAILS

•	USERS (1) → (∞) USER_INGREDIENTS (∞) ← (1) INGREDIENTS

•	COCKTAILS (∞) → (1) CATEGORIES

•	COCKTAILS (∞) ↔ (∞) INGREDIENTS (через COCKTAIL_INGREDIENTS)

3. API схема.
   Аутентификация
   
•	POST /api/auth/register/ – Регистрация нового пользователя

•	POST /api/auth/login/ – Вход пользователя

•	POST /api/auth/logout/ – Выход пользователя

   Ингредиенты
   
•	GET /api/ingredients/ – Получить список всех ингредиентов

   Ингредиенты пользователя
   
•	GET /api/user-ingredients/ – Получить список ингредиентов текущего пользователя

•	POST /api/user-ingredients/ – Добавить новый ингредиент

•	DELETE /api/user-ingredients/ – Удалить ингредиент


   Коктейли
   
•	GET /api/cocktails/ – Получить список всех коктейлей

•	GET /api/cocktails/{id}/ – Получить информацию о конкретном коктейле

•	POST /api/cocktails/ – Добавить новый коктейль (для администраторов)

•	DELETE /api/cocktails/{id}/ – Удалить коктейль (для администраторов)

   Поиск коктейлей по ингредиентам
   
•	GET /api/cocktails/by-ingredients/ – Получить коктейли, которые можно приготовить из имеющихся ингредиентов пользователя

•	GET /api/cocktails/missing-ingredients/ – Получить коктейли, для которых не хватает ингредиентов, с указанием недостающих продуктов

   Категории коктейлей
   
•	GET /api/categories/ – Получить список всех категорий

•	GET /api/categories/{id}/ – Получить информацию о конкретной категории

•	POST /api/categories/ – Добавить новую категорию (для администраторов)

•	DELETE /api/categories/{id}/ – Удалить категорию (для администраторов)


5. Используемые технологии
   
Front: HTML + CSS, django AlpineJS

Back: python, django

БД: PostgresSQL

