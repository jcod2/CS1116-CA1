from flask import render_template, session
from database import get_db, close_db
from random import randint

def dex_by_region_func(region):
    '''
    function    - generate table of pokemon from region
    :param      - String -> region
    :return     - table of all pokemon from that region
    '''
    db = get_db()
    pokemon = db.execute("""SELECT pokemon_id, pokedex_number, pokemon_name, alternate_form_name, 
                            primary_type, secondary_type FROM pokemon
                         WHERE region_of_origin = ?
                         ORDER BY pokedex_number ASC;""", (region, )).fetchall()
    close_db()
    return render_template("poke_pages/national_dex.html", 
        pokemon=pokemon, title=region + "'s Regional Pokémon")

def pokemon_func(pokemon_id):
    '''
    function    - dex entry page
    :param      - Int -> pokemon_id
    :return     - dex entry page of the pokemon with that id
    '''
    db = get_db()
    pokemon = db.execute("SELECT * FROM pokemon WHERE pokemon_id = ?;", (pokemon_id,)).fetchone()
    close_db()
    ''' get imgs from API instead of 'local' files
    dex_num = db.execute("""SELECT pokedex_number FROM pokemon
                            WHERE pokemon_id = ?;""", (pokemon_id,)).fetchone()
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(dex_num[0]))
    data = response.json()

    sprite = data["sprites"]["front_default"]
    ,sprite=sprite)'''
    return render_template("poke_pages/pokemon.html", 
        pokemon=pokemon, title=pokemon["pokemon_name"], pokemon_id=pokemon_id)

def poke_nav_func(pokemon_id, direction):
    '''
    function    - next or previous dex entry page
    :param      - Int -> pokemon_id
    :return     - next or previous dex entry page
    '''
    '''
    there are gaps in the ids in table, e.g. no ids between 744 and 828, so to avoid 404's
    i wrote this route, i could have just re-done the ids in the db table
    but this way its more full proof i feel could also instead have used
    use dex number instead of id and for each page do a for loop to display
    each pokemon with that dex number sinces dex number is not unique, but i wanted 
    each entry to have its own page and when i did try the for loop, pages with 3+entries 
    were too long and annoying to scroll through
    '''
    db = get_db()
    query = "SELECT * FROM pokemon WHERE pokemon_id = ?;"
    if direction == "prev":
        pokemon_id = pokemon_id - 1
        pokemon = db.execute(query, (pokemon_id,)).fetchone()
        while not pokemon:
            pokemon = db.execute(query, (pokemon_id,)).fetchone()
            pokemon_id -= 1
    if direction == "next":
        pokemon = db.execute(query, (pokemon_id,)).fetchone()
        while not pokemon:
            pokemon = db.execute(query, (pokemon_id,)).fetchone()
            pokemon_id += 1
    close_db()
    return render_template("poke_pages/pokemon.html", 
        pokemon=pokemon, title=pokemon["pokemon_name"], pokemon_id=pokemon_id)

def random_team_func():
    '''
    function    - generate random team of 6 pokemon
    :param      - 
    :return     - random team of 6 pokemon with unique primary types 
    '''
    # start ran_team and clear on each page reload
    if "ran_team" not in session:
        session["ran_team"] = []
    else:
        session["ran_team"] = []

    db = get_db()
    random_team = []
    temp_types = []
    while len(random_team) < 6:
        pokemon = db.execute("""SELECT pokemon_id, pokedex_number, pokemon_name, alternate_form_name, 
                            primary_type, secondary_type FROM pokemon
                            WHERE pokedex_number = ?;""", (randint(1, 898),)).fetchone()
        if pokemon["primary_type"]:
            if pokemon["primary_type"] not in temp_types:
                temp_types.append(pokemon["primary_type"])
                random_team.append(pokemon)
                session["ran_team"].append(pokemon["pokemon_id"])
    close_db()

    return render_template("poke_pages/random_team.html", 
        title="Random Team Generator", random_team=random_team)

def random_team_by_region_func(region, start, end):
    '''
    function    - generate random team of 6 pokemon in a specific region
    :param      - String -> region, Int -> start, Int -> end
    :return     - random team from that region of 6 pokemon with unique primary types
    '''
    # start ran_team and clear on each page reload
    if "ran_team" not in session:
        session["ran_team"] = []
    else:
        session["ran_team"] = []

    db = get_db()
    message = "Team consisiting only of " + region + "'s Regional Pokémon."
    random_team = []
    temp_types = []
    while len(random_team) < 6:
        pokemon = db.execute("""SELECT DISTINCT pokemon_id, pokedex_number, pokemon_name, alternate_form_name, 
                            primary_type, secondary_type FROM pokemon
                            WHERE pokedex_number = ?;""", (randint(start, end),)).fetchone()
        if pokemon["primary_type"]:
            if pokemon["primary_type"] not in temp_types:
                temp_types.append(pokemon["primary_type"])
                random_team.append(pokemon)
                session["ran_team"].append(pokemon["pokemon_id"])
    close_db()
    return render_template("poke_pages/random_team.html", 
        title="Random Team Generator", random_team=random_team, message=message)

def random_team_new_tab_func():
    '''
    function    - take the randomly generated team and dispay it in a new tab
    :param      - 
    :return     - list of the team with ids taken from previous page
    '''
    db = get_db()
    random_team = []
    for id in session["ran_team"]:
        pokemon = db.execute("""SELECT pokemon_id, pokedex_number, pokemon_name, alternate_form_name, 
                    primary_type, secondary_type FROM pokemon
                    WHERE pokemon_id = ?;""", (id, )).fetchone()
        random_team.append(pokemon)
    close_db()
    return render_template("poke_pages/random_team_new_tab.html", 
        title="Random Team Generator", random_team=random_team)