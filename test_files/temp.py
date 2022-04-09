@app.route("/national_dex/<string:region>")
def contents(region):
    db = get_db()
    pokemon = db.execute("""SELECT * FROM pokemon 
                         WHERE region_of_origin = ?
                         ORDER BY pokedex_number ASC;""", (region, )).fetchall()
    close_db()
    return render_template("poke_pages/contents.html", 
        pokemon=pokemon, title=region + "'s Regional Pokémon")