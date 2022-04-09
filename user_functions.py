from flask import redirect, render_template, url_for, session
from database import get_db, close_db
from sqlite3 import IntegrityError

def favourites_func():
    '''
    function    - go to user favourites
    :param      - 
    :return     - table of user favourites
    '''
    db = get_db()
    pokemon = db.execute("SELECT * FROM "+session["user_id"]+"_favourites ORDER BY pokedex_number;").fetchall()
    close_db()
    return render_template("user_pages/favourites.html", 
        pokemon=pokemon, title="Your favourites")

def add_to_favourites_func(pokemon_id):
    '''
    function    - add pokemon to user favourites
    :param      - Int -> pokemon_id
    :return     - table consisting of favourites
    '''
    db = get_db()
    try:
        db.execute("INSERT INTO "+session["user_id"]+"_favourites"""" (pokemon_id, pokedex_number, pokemon_name, alternate_form_name)
                SELECT pokemon_id, pokedex_number, pokemon_name, alternate_form_name FROM pokemon
                WHERE pokemon_id = ?;""", (pokemon_id,))
        db.commit()
        close_db()
    except IntegrityError:
        return redirect(url_for("favourites"))
    return redirect(url_for("favourites"))

def remove_from_favourites_func(pokemon_id):
    '''
    function    - remove pokemon from user favourites
    :param      - Int -> pokemon_id
    :return     - favourites without the parameter pokemon
    '''
    db = get_db()
    db.execute("DELETE FROM "+session["user_id"]+"_favourites WHERE pokemon_id = ?;", (pokemon_id,))
    db.commit()
    close_db()
    return redirect(url_for("favourites"))