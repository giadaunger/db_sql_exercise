def add_user_db(con, username):
    add_user_query = """
    INSERT INTO users(username)
    VALUES(%s)
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(add_user_query, (username,))

def list_user_db(con, limit):
    list_users_query = """
    SELECT * FROM users
    LIMIT %s
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_users_query, (limit,))
            return cursor.fetchall()

def list_movies_db(con, limit, release_date):
    list_movies_query = """
    SELECT * FROM movies
    WHERE release_date >= %s
    LIMIT %s
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(list_movies_query, (release_date, limit))
            return cursor.fetchall()

def update_movie_db(con, new_movie_title, title, release_date, genre):
    uppdatemovie_query = """
    UPDATE movies
    SET title = %s, release_date = %s, genre_id = (SELECT id FROM genres WHERE name = %s)
    WHERE title = %s
    RETURNING id
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(uppdatemovie_query, (new_movie_title, release_date, genre, title))
            return cursor.fetchone()

def add_movie_genre_db(con, genre):
    add_movie_genre_query = """
    INSERT INTO genres(name)
    VALUES(%s)
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(add_movie_genre_query, (genre,))

def add_movie_db(con, title, release_date, genre):
    add_movie_movie_query = """
    INSERT INTO movies(title, release_date, genre_id)
    VALUES(%s, %s, (SELECT id FROM genres WHERE name=%s))
    """
    with con:
        with con.cursor() as cursor:
            cursor.execute(add_movie_movie_query, (title, release_date, genre))

# Example create table func
# def create_tables(con):
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS test(
#         id SERIAL PRIMARY KEY,
#         name VARCHAR(100)
#     )
#     """

#     # Bad / Manual way !!!
#     # cursor = con.cursor()
#     # cursor.execute(create_table_query)
#     # con.commit()
#     # cursor.close()

#     # Using the with-keyword
#     with con:
#         with con.cursor() as cursor:
#             cursor.execute(create_table_query)


def create_tables(con):
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE
    )
    """

    create_genre_table_query = """
    CREATE TABLE IF NOT EXISTS genres(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    )
    """

    create_movies_table_query = """
    CREATE TABLE IF NOT EXISTS movies(
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) UNIQUE,
        release_date DATE,
        genre_id INT REFERENCES genreS(id)
    )
    """

    watchlist = """
    CREATE TABLE IF NOT EXISTS watchlist(
        user_id INT REFERENCES users(id),
        movie_id INT REFERENCES movies(id),
        added_date DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY(user_id, movie_id)
    )
    """

    reviews = """
    CREATE TABLE IF NOT EXISTS reviews(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        movie_id INT REFERENCES movies(id),
        rating INT,
        review_text TEXT,
        review_date DATE DEFAULT CURRENT_DATE
    )
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(create_user_table_query)
            cursor.execute(create_genre_table_query)
            cursor.execute(create_movies_table_query)
            cursor.execute(watchlist)
            cursor.execute(reviews)
