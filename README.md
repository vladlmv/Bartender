Bartender

1. Концепция приложения
Приложение помогает пользователям находить и создавать коктейли: как из ингредиентов, которые уже есть у пользователя, так и из тех, которые нужно докупить.

2. Схема БД
   
USERS (пользователи)

id (SERIAL, PK) – уникальный идентификатор пользователя

login (VARCHAR(50), UNIQUE, NOT NULL) – имя пользователя

password (TEXT, NOT NULL) – пароль

is_admin (BOOLEAN, DEFAULT FALSE) – признак администратора

USER_INGREDIENTS (ингредиенты пользователя)

id (SERIAL, PK) – уникальный идентификатор

user_id (INTEGER, FK → USERS.id, ON DELETE CASCADE) – связь с пользователем

ingredient_id (INTEGER, FK → INGREDIENTS.id, ON DELETE CASCADE) – связь с ингредиентом

INGREDIENTS (ингредиенты)

id (SERIAL, PK) – уникальный идентификатор ингредиента

name (VARCHAR(100), UNIQUE, NOT NULL) – название ингредиента

CATEGORIES (категории коктейлей)

id (SERIAL, PK) – уникальный идентификатор

name (VARCHAR(50), UNIQUE, NOT NULL) – название категории

COCKTAILS (коктейли)

id (SERIAL, PK) – уникальный идентификатор коктейля

name (VARCHAR(100), UNIQUE, NOT NULL) – название коктейля

category_id (INTEGER, FK → CATEGORIES.id, NOT NULL) – категория коктейля

instructions (TEXT) – рецепт приготовления

ingredients (INT[] или JSONB, NOT NULL) – список ингредиентов коктейля (ссылки на INGREDIENTS.id)

Схема отношений

USERS (1) → (∞) USER_INGREDIENTS (∞) ← (1) INGREDIENTS

COCKTAILS (∞) → (1) CATEGORIES

COCKTAILS (∞) ↔ (∞) INGREDIENTS (через поле ingredients)

3. API схема

Аутентификация

POST /api/auth/register/ – Регистрация нового пользователя

POST /api/auth/login/ – Вход пользователя

POST /api/auth/logout/ – Выход пользователя

Ингредиенты

GET /api/ingredients/ – Получить список всех ингредиентов

Ингредиенты пользователя

GET /api/user-ingredients/ – Получить список ингредиентов текущего пользователя

POST /api/user-ingredients/ – Добавить новый ингредиент

DELETE /api/user-ingredients/ – Удалить ингредиент

Коктейли

GET /api/cocktails/ – Получить список всех коктейлей

GET /api/cocktails/{id}/ – Получить информацию о конкретном коктейле

POST /api/cocktails/ – Добавить новый коктейль (только для админов)

DELETE /api/cocktails/{id}/ – Удалить коктейль (только для админов)

Поиск коктейлей по ингредиентам

GET /api/cocktails/by-ingredients/ – Получить коктейли, которые можно приготовить из имеющихся ингредиентов пользователя

GET /api/cocktails/missing-ingredients/ – Получить коктейли, для которых не хватает ингредиентов, с указанием недостающих

Категории коктейлей

GET /api/categories/ – Получить список всех категорий

GET /api/categories/{id}/ – Получить информацию о конкретной категории

POST /api/categories/ – Добавить новую категорию (только для админов)

DELETE /api/categories/{id}/ – Удалить категорию (только для админов)

6. Используемые технологии

Frontend: HTML, CSS, AlpineJS, Django templates

Backend: Python, Django

БД: PostgreSQL
