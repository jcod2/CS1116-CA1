# Wed Development 2, CA1

from flask import Flask, redirect, render_template, url_for, session, request, g
from forms import *
from database import get_db, close_db
from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from functools import wraps
from my_functions import *
from poke_functions import *
from admin_functions import *
from user_functions import *
# import requests

# adminsitartor user account
# user_id: admin
# password: admin
# can manually add or delete users if they visit /admin, can also reset user data (delete all users and their favourites)

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.teardown_appcontext(close_db)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

@app.before_request
def check_team():
    if "mode" not in session:
        session["mode"] = "dark"
    g.mode = session["mode"]

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            login_Error = "You must be logged in to do that."
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        elif session["user_id"] != "Admin":
            return redirect(url_for("index"))
        return view(**kwargs)
    return wrapped_view

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(418)
def page_not_found(e):
    return render_template("errors/418.html"), 418

@app.route("/theme")
def theme():
    '''
    function    - set site stylesheet
    :param      - 
    :return     - correct stylesheet
    '''
    if  session["mode"] == "light":
         session["mode"] = "dark"
    else:
        session["mode"] = "light"
    return redirect(request.referrer)

@app.route("/")
def index():
    '''
    function    - redirect to homepage
    :param      - 
    :return     -  
    '''
    return render_template("index.html", title="Homepage")

@app.route("/disclaimer")
def disclaimer():
    '''
    function    - redirect to copyright disclaimer
    :param      - 
    :return     -  
    '''
    return render_template("disclaimer.html", title="Disclaimer")

@app.route("/register", methods=["GET", "POST"])
def register():
    '''
    function    - registration form
    :param      - 
    :return     -  redirect to login
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data.title()
        password = form.password.data
        if not user_id.isalnum():
            form.user_id.errors.append("Username must be alphanumeric. (Only letters and numbers allowed)")
            return render_template("user_pages/register.html", 
                form=form, title="Register")
        db = get_db()
        try:
            db.execute("""INSERT INTO users (user_id, password)
                        VALUES (?, ?)""", (user_id, generate_password_hash(password)))
            db.execute("DROP TABLE IF EXISTS "+user_id+";")
            db.execute("CREATE TABLE "+user_id+"_favourites""""
                        (pokemon_id INTEGER PRIMARY KEY,
                        pokedex_number INTEGER NOT NULL,
                        pokemon_name TEXT NOT NULL,
                        alternate_form_name TEXT);""")
            db.commit()
            close_db()
            return redirect(url_for('login'))
        except IntegrityError:
            form.user_id.errors.append("User id is already taken.")
    return render_template("user_pages/register.html", 
        form=form, title="Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    function    - login form
    :param      - 
    :return     -  redirect to favourites
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data.title()
        password = form.password.data

        db = get_db()
        user_exists = db.execute("""SELECT * FROM users
                                WHERE user_id = ?;""", (user_id,)).fetchone()
        close_db()
        if not user_exists:
            form.user_id.errors.append("Unknown user id!")
        elif not check_password_hash(user_exists["password"], password):
            form.password.errors.append("Incorrect password!")
        elif user_id in session:
             form.user_id.errors.append("Already logged in as "+user_id)
        else:
            session.pop("user_id", None)
            session["user_id"] = user_id
            if user_id == "Admin":
                return redirect(url_for("admin"))
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("favourites")
            return redirect(next_page)
    return render_template("user_pages/login.html", 
        form=form, title="Login")

@app.route("/logout")
def logout():
    '''
    function    - logout the user currently in session
    :param      - 
    :return     -  redirect to login
    '''
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    '''
    function    - admin form
    :param      - 
    :return     -  redirect to correct page based on form data
    '''
    form = AdminForm()
    if form.validate_on_submit():
        options = form.options.data

        if options == "Add user":
            return redirect(url_for("adminAdd"))
        elif options == "Delete user":
            return redirect(url_for("adminDel"))
        elif options == "Reset users":
            return render_template("admin_pages/admin_reset.html")
        elif options == "Show all users":
            return redirect(url_for("all_users"))
    return render_template("admin_pages/admin.html", 
        form=form, title="Admin")

@app.route("/admin/add", methods=["GET", "POST"])
@admin_required
def adminAdd():
    '''
    function    - add a specific user account
    :param      - 
    :return     -  redirect to admin page
    '''
    form = AdminAddForm()
    if form.validate_on_submit():
        user_id = form.user_id.data.title()
        password = form.password.data
        if not user_id.isalnum():
            form.user_id.errors.append("Username must be alphanumeric.")
            return render_template("admin_pages/admin_form.html", 
                form=form, title="Add User", message="Add User")
        db = get_db()
        try:
            db.execute("""INSERT INTO users (user_id, password)
                        VALUES (?, ?)""", (user_id, generate_password_hash(password)))
            db.execute("DROP TABLE IF EXISTS "+user_id+";")
            db.execute("CREATE TABLE "+user_id+"_favourites""""
                        (pokemon_id INTEGER PRIMARY KEY,
                        pokedex_number INTEGER NOT NULL,
                        pokemon_name TEXT NOT NULL,
                        alternate_form_name TEXT);""")
            db.commit()
            close_db()
            return redirect(url_for('admin'))
        except IntegrityError:
            form.user_id.errors.append("User id is already taken.")
    return render_template("admin_pages/admin_form.html", 
        form=form, title="Add User", message="Add User")

@app.route("/admin/delete", methods=["GET", "POST"])
@admin_required
def adminDel():
    '''
    function    - delete a specific user account
    :param      - 
    :return     -  redirect to admin page
    '''
    form = AdminDelForm()
    if form.validate_on_submit():
        user_id = form.user_id.data.title()

        db = get_db()
        db.execute("DELETE FROM users WHERE user_id = ?;", (user_id,))
        db.execute("DROP TABLE IF EXISTS "+user_id+"_favourites;")
        db.commit()
        close_db()
        return redirect(url_for('admin'))
    return render_template("admin_pages/admin_form.html", 
        form=form, title="Delete User", caption="Delete User")

@app.route("/admin/reset")
@admin_required
def reset():
    return reset_func()

@app.route("/all_users")
def all_users():
    return all_users_func()

@app.route("/confirm_reset")
def confirm_reset():
    '''
    function    - redirect to confirmation page for re-setting user data
    :param      - 
    :return     - 
    '''
    return render_template("admin_pages/confirm_reset.html")

@app.route("/national_dex")
def national_dex_home():
    '''
    function    - redirect to home page of nation dex search
    :param      - 
    :return     - 
    '''
    return render_template("poke_pages/national_dex.html", title="Search Pokémon by Region")

@app.route("/national_dex/<string:region>")
def dex_by_region(region):
    return dex_by_region_func(region)

@app.route("/nation_dex")
def redirect_dead():
    '''
    function    - redirect dead route to national dex home
    :param      - 
    :return     - 
    '''
    return redirect(url_for("national_dex_home"))

@app.route("/pokemon/<int:pokemon_id>")
def pokemon(pokemon_id):
    return pokemon_func(pokemon_id)

'''
@app.route("/pokemon/<int:jump>")
def jumpTo(jump):
    db = get_db()
    pokemon = db.execute("SELECT * FROM pokemon WHERE pokemon_id = ?;", (jump,)).fetchone()
    close_db()
    return render_template("poke_pages/pokemon.html", 
        pokemon=pokemon, title=pokemon["pokemon_name"], pokemon_id=pokemon_id)
'''

@app.route("/pokemon/<int:pokemon_id>/<string:direction>")
def poke_nav(pokemon_id, direction):
    return poke_nav_func(pokemon_id, direction)

@app.route("/random_team")
def random_team():
    return random_team_func()

@app.route("/random_team_by_region/<string:region>/<int:start>/<int:end>")
def random_team_by_region(region, start, end):
    return random_team_by_region_func(region, start, end)

@app.route("/random_team_new_tab")
def random_team_new_tab():
    return random_team_new_tab_func()

''' was going to implement the saving of random teams, but decided to remove it before i put more time into it
would have been a lot of bloat in the db, adding tables for each saved team, did get it working using just the session
it was acting more or less like a cart, but that was kinda useless since it was user specific
@app.route("/random_team_save")
def random_team_save():
    pokemon_ids = session["team"]
    db = get_db()
    team = []
    for id in pokemon_ids:
        pokemon = db.execute("""SELECT * FROM pokemon
                            WHERE pokemon_id = ?;""", (id,)).fetchone()
        team.append(pokemon)
    return render_template("user_pages/saved_team.html", 
        team=team, title="Your current saved team")
'''

@app.route("/favourites")
@login_required
def favourites():
    return favourites_func()

@app.route("/add_to_favourites/<int:pokemon_id>")
@login_required
def add_to_favourites(pokemon_id):
    return add_to_favourites_func(pokemon_id)

@app.route("/remove_from_favourites/<int:pokemon_id>")
def remove_from_favourites(pokemon_id):
    return remove_from_favourites_func(pokemon_id)

@app.route("/pokedex", methods=["GET", "POST"])
def pokedex():
    '''
    function    - search database table
    :param      - 
    :return     - tables based on the form fields filled
    '''
    form = PokedexForm()
    db = get_db()
    pokemon = alt_form = classification = leg_type = hidden_ab = stats = evs = region = temp_query = None
    message = ""

    form.prim_type.choices = pop_choices(list(db.execute("SELECT DISTINCT primary_type FROM pokemon ORDER BY primary_type;").fetchall()))
    form.sec_type.choices = form.prim_type.choices
    form.classification.choices = pop_choices(list(db.execute("SELECT DISTINCT classification FROM pokemon ORDER BY classification;").fetchall()))
    form.hidden_ab.choices = pop_choices(list(db.execute("SELECT DISTINCT hidden_ability FROM pokemon ORDER BY hidden_ability;").fetchall()))
    form.alt_form.choices = pop_choices(list(db.execute("SELECT DISTINCT alternate_form_name FROM pokemon ORDER BY alternate_form_name;").fetchall()))
    form.leg_type.choices = pop_choices(list(db.execute("SELECT DISTINCT legendary_type FROM pokemon;").fetchall()))
    form.region.choices = pop_choices(list(db.execute("SELECT DISTINCT region_of_origin FROM pokemon ORDER BY region_of_origin;").fetchall()))

    if form.validate_on_submit():
        name = form.name.data.title().strip()
        nat_dex = form.nat_dex.data
        prim_type = form.prim_type.data
        sec_type = form.sec_type.data
        classification = form.classification.data
        hidden_ab = form.hidden_ab.data
        alt_form = form.alt_form.data
        leg_type = form.leg_type.data
        region = form.region.data
        stats = form.stats.data
        evs = form.evs.data

        query = "SELECT * FROM pokemon"
        temp_query = []
        order = " ORDER BY pokedex_number ASC;"
        if name:
            temp_query.append("pokemon_name = '" + name +"'")
        if nat_dex:
            # did this manually instead of using wtforms validators, as wtforms validators makes the field required and i didnt want that
            if int(nat_dex) < 1 or int(nat_dex) > 898:
                form.nat_dex.errors.append("Number must be between 1 and 898.")
            else:
                form.nat_dex.errors.append("Must be a number.")
            temp_query.append("pokedex_number = '" + nat_dex +"'")
        if prim_type:
            temp_query.append("primary_type = '" + prim_type +"'")
        if sec_type:
            temp_query.append("secondary_type = '" + sec_type +"'")
        if classification:
            temp_query.append("classification = '" + classification +"'")
        if hidden_ab:
            temp_query.append("hidden_ability = '" + hidden_ab +"'")
        if alt_form:
            temp_query.append("alternate_form_name = '" + alt_form +"'")
        if leg_type:
            temp_query.append("legendary_type = '" + leg_type +"'")
        if region:
            temp_query.append("region_of_origin = '" + region +"'")
        if temp_query:
            message = "Below are the results from the form."
            query = query + " WHERE " + " AND ".join(temp_query)
            pokemon = db.execute(query + order).fetchall()
        elif not temp_query:
            message = "All fields left empty, below is a table containing all Pokémon."
            pokemon = db.execute(query + order).fetchall()
        if not pokemon:
            message = "No such pokemon exists."
        close_db()
    return render_template("poke_pages/pokedex_form.html", 
        form=form, title="Pokédex Search", caption="Search Results", pokemon=pokemon, classification=classification, 
        hidden_ab=hidden_ab, alt_form=alt_form, leg_type=leg_type, region=region, stats=stats, evs=evs, 
        message=message)