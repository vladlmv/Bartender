from mybar.database import init_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Auth CRUD operations
def register_user(login: str, password: str):
    """Register a new user and return user object"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute('SELECT 1 FROM "users" WHERE login = %s', (login,))
        if cursor.fetchone():
            raise ValueError("User already exists")

        hashed_password = pwd_context.hash(password)
        cursor.execute(
            'INSERT INTO "users" (login, password) VALUES (%s, %s) RETURNING id, login',
            (login, hashed_password)
        )
        user_data = cursor.fetchone()
        conn.commit()
        return {'id': user_data[0], 'login': user_data[1]}  # Возвращаем словарь с данными
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def verify_user(login: str, password: str):
    """Verify user credentials"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT id, password FROM "users" WHERE login = %s',
            (login,)
        )
        user = cursor.fetchone()

        if not user:
            return None

        user_id, hashed_password = user
        if pwd_context.verify(password, hashed_password):
            return user_id
        return None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_user_hashed_password(user_id: int):
    """Get the hashed password for a given user ID."""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM "users" WHERE id = %s', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def update_user_password(user_id: int, new_password: str):
    """Update a user's password in the database."""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        hashed_new_password = pwd_context.hash(new_password)
        cursor.execute(
            'UPDATE "users" SET password = %s WHERE id = %s',
            (hashed_new_password, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0 # Returns True if a row was updated, False otherwise
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def add_admin(login: str, password: str): # НОВАЯ ФУНКЦИЯ ДЛЯ ДОБАВЛЕНИЯ АДМИНА
    """Add a new admin to the database (password will be hashed)."""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Проверяем, не существует ли уже администратор с таким логином
        cursor.execute('SELECT id FROM admins WHERE login = %s', (login,))
        if cursor.fetchone():
            raise ValueError(f"Admin with login '{login}' already exists.")

        hashed_password = pwd_context.hash(password)
        cursor.execute(
            'INSERT INTO admins (login, password) VALUES (%s, %s) RETURNING id',
            (login, hashed_password)
        )
        admin_id = cursor.fetchone()[0]
        conn.commit()
        return admin_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Admin CRUD operations
def verify_admin(login: str, password: str):
    """Verify admin credentials"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT id, password FROM "admins" WHERE login = %s',
            (login,)
        )
        admin = cursor.fetchone()

        if not admin:
            return None

        admin_id, hashed_password = admin
        if pwd_context.verify(password, hashed_password):
            return admin_id
        return None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


# Ingredient CRUD operations
def create_ingredient(name: str):
    """Create a new ingredient (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO "ingredients" (name) VALUES (%s) RETURNING id',
            (name,)
        )
        ingredient_id = cursor.fetchone()[0]
        conn.commit()
        return ingredient_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_all_ingredients():
    """Get all ingredients"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM "ingredients"')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def delete_ingredient(ingredient_id: int):
    """Delete an ingredient (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "ingredients" WHERE id = %s',
            (ingredient_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# UserIngredient CRUD operations
def add_user_ingredient(user_id: int, ingredient_id: int):
    """Add ingredient to user's collection"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Check if ingredient exists
        cursor.execute('SELECT 1 FROM "ingredients" WHERE id = %s', (ingredient_id,))
        if not cursor.fetchone():
            raise ValueError("Ingredient not found")

        cursor.execute(
            'INSERT INTO "user_ingredients" (user_id, ingredient_id) VALUES (%s, %s) RETURNING id',
            (user_id, ingredient_id)
        )
        user_ingredient_id = cursor.fetchone()[0]
        conn.commit()
        return user_ingredient_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_user_ingredients(user_id: int):
    """Get all ingredients for a specific user"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.id, i.name 
            FROM "user_ingredients" ui
            JOIN "ingredients" i ON ui.ingredient_id = i.id
            WHERE ui.user_id = %s
        """, (user_id,))

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def delete_user_ingredient(user_id: int, ingredient_id: int):
    """Remove ingredient from user's collection"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "user_ingredients" WHERE user_id = %s AND ingredient_id = %s',
            (user_id, ingredient_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Category CRUD operations
def create_category(name: str):
    """Create a new category (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO "categories" (name) VALUES (%s) RETURNING id',
            (name,)
        )
        category_id = cursor.fetchone()[0]
        conn.commit()
        return category_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_all_categories():
    """Get all categories"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM "categories"')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def get_category(category_id: int):
    """Get specific category by ID"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM "categories" WHERE id = %s', (category_id,))
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def delete_category(category_id: int):
    """Delete a category (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "categories" WHERE id = %s',
            (category_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Cocktail CRUD operations
def create_cocktail(name: str, category_id: int, instructions: str):
    """Create a new cocktail (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Check if category exists
        cursor.execute('SELECT 1 FROM "categories" WHERE id = %s', (category_id,))
        if not cursor.fetchone():
            raise ValueError("Category not found")

        cursor.execute(
            'INSERT INTO "cocktails" (name, category_id, instructions) VALUES (%s, %s, %s) RETURNING id',
            (name, category_id, instructions)
        )
        cocktail_id = cursor.fetchone()[0]
        conn.commit()
        return cocktail_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_all_cocktails():
    """Get all cocktails"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.name, c.instructions, cat.name as category_name
            FROM "cocktails" c
            JOIN "categories" cat ON c.category_id = cat.id
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def get_cocktail(cocktail_id: int):
    """Get specific cocktail by ID"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.name, c.instructions, cat.name as category_name
            FROM "cocktails" c
            JOIN "categories" cat ON c.category_id = cat.id
            WHERE c.id = %s
        """, (cocktail_id,))

        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def delete_cocktail(cocktail_id: int):
    """Delete a cocktail (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "cocktails" WHERE id = %s',
            (cocktail_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_cocktails_by_user_ingredients(user_id: int):
    """Get cocktails that can be made with user's ingredients"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.name, c.instructions, cat.name as category_name
            FROM "cocktails" c
            JOIN "categories" cat ON c.category_id = cat.id
            WHERE NOT EXISTS (
                SELECT ci.ingredient_id
                FROM "cocktail_ingredients" ci
                WHERE ci.cocktail_id = c.id
                AND ci.ingredient_id NOT IN (
                    SELECT ui.ingredient_id
                    FROM "user_ingredients" ui
                    WHERE ui.user_id = %s
                )
            )
        """, (user_id,))

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def get_cocktails_missing_ingredients(user_id: int):
    """Get cocktails with missing ingredients for a user"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                c.id as cocktail_id, 
                c.name as cocktail_name,
                i.id as missing_ingredient_id,
                i.name as missing_ingredient_name
            FROM "cocktails" c
            JOIN "cocktail_ingredients" ci ON c.id = ci.cocktail_id
            JOIN "ingredients" i ON ci.ingredient_id = i.id
            WHERE ci.ingredient_id NOT IN (
                SELECT ui.ingredient_id
                FROM "user_ingredients" ui
                WHERE ui.user_id = %s
            )
            ORDER BY c.id
        """, (user_id,))

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


# CocktailIngredient CRUD operations
def add_cocktail_ingredient(cocktail_id: int, ingredient_id: int):
    """Add ingredient to cocktail (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Check if cocktail and ingredient exist
        cursor.execute('SELECT 1 FROM "cocktails" WHERE id = %s', (cocktail_id,))
        if not cursor.fetchone():
            raise ValueError("Cocktail not found")

        cursor.execute('SELECT 1 FROM "ingredients" WHERE id = %s', (ingredient_id,))
        if not cursor.fetchone():
            raise ValueError("Ingredient not found")

        cursor.execute(
            'INSERT INTO "cocktail_ingredients" (cocktail_id, ingredient_id) VALUES (%s, %s) RETURNING id',
            (cocktail_id, ingredient_id)
        )
        ci_id = cursor.fetchone()[0]
        conn.commit()
        return ci_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_cocktail_ingredients(cocktail_id: int):
    """Get all ingredients for a specific cocktail"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.id, i.name
            FROM "cocktail_ingredients" ci
            JOIN "ingredients" i ON ci.ingredient_id = i.id
            WHERE ci.cocktail_id = %s
        """, (cocktail_id,))

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def delete_cocktail_ingredient(cocktail_id: int, ingredient_id: int):
    """Remove ingredient from cocktail (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "cocktail_ingredients" WHERE cocktail_id = %s AND ingredient_id = %s',
            (cocktail_id, ingredient_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_ingredient_by_id(ingredient_id: int):
    """Get specific ingredient by ID"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM "ingredients" WHERE id = %s', (ingredient_id,))
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

# Add this function to the Cocktail CRUD operations section
def get_cocktails_by_ingredient(ingredient_id: int):
    """Get all cocktails that contain a specific ingredient"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.name, c.instructions, cat.name as category_name
            FROM "cocktails" c
            JOIN "categories" cat ON c.category_id = cat.id
            WHERE c.id IN (
                SELECT cocktail_id 
                FROM "cocktail_ingredients" 
                WHERE ingredient_id = %s
            )
        """, (ingredient_id,))

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_all_users():
    """Get all users (admin only)"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute('SELECT id, login FROM "users"')
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_cocktails_by_category(category_id: int):
    """Get all cocktails in a specific category"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.name, c.instructions, cat.name as category_name
            FROM "cocktails" c
            JOIN "categories" cat ON c.category_id = cat.id
            WHERE c.category_id = %s
        """, (category_id,))

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()