import psycopg2
from dotenv import load_dotenv
import os
import db

load_dotenv()
pw = os.getenv("DB")

def create_connection(pw):
    con = psycopg2.connect(dbname="pythondb", password=pw, host="localhost", user="postgres", port=5433)
    return con

def add_user(con):
    username = input("Choose a username: ")
    db.add_user_db(con=con, username=username)

def list_users(con):
    limit = input("How many users do you want to list: ")
    users = db.list_user_db(con=con, limit=limit)
    for user in users:
        print(user)

def list_movies(con):
    limit = input("How many movies do you want to list: ")
    release_date = input("From what date: ")
    movies = db.list_movies_db(con=con, limit=limit, release_date=release_date)
    for movie in movies:
        print(movie)

def update_movie(con):
    title = input("What movie do you want to change?")
    new_movie_title = input("What title should it have?")
    release_date = input("What release date? YYYY-mm-dd")
    genre = input("What genre does the movie have?")
    result = db.update_movie_db(con=con, title=title, new_movie_title=new_movie_title, release_date=release_date, genre=genre)
    if result:
        print("Update succesful")
    else:
        print("Update failed")

def add_movie_genre(con):
    genre = input("What genre do yoy want to add: ")
    try:
        db.add_movie_genre_db(con=con, genre=genre)
    except psycopg2.IntegrityError as e:
        print("Genre already exist, try again")
    except psycopg2.DatabaseError as e:
        print("Something went wrong")
        print(e)


def add_movie(con):
    title = input("What title does the movie have: ")
    genre = input("What genre does the movie has: ")
    release_date = input("What is the release date: ")
    try:
        db.add_movie_db(con=con, title=title, genre=genre, release_date=release_date)
    except psycopg2.DatabaseError:
        print("Something went wrong")
    

menu_text = """
Make a choice:
[0] - Create tables
[1] - Create user
[2] - List users
[3] - Add movie genre
[4] - Add movie
[5] - List movies
[6] - Update movie
[7] - Create rewiev
"""

menu_options = {
    "0": db.create_tables,
    "1": add_user,
    "2": list_users,
    "3": add_movie_genre,
    "4": add_movie,
    "5": list_movies, 
    "6": update_movie
}


def menu(con):
    try:
        choice = input(menu_text)
        menu_options[choice](con)
        input("Press enter to continue")
    except Exception as e:
        print(e)
        print("Not a valid choice")


if __name__ == "__main__":
    try:
        con = create_connection(pw)
        while True:
            menu(con)
    finally:
        con.close()