from flask import redirect, render_template, url_for
from database import get_db, close_db

def all_users_func():
    '''
    function    - display table of all users
    :param      - 
    :return     - table of all registered usernames
    '''
    db = get_db()
    users = db.execute("SELECT user_id FROM users WHERE user_id != 'Admin';").fetchall()
    close_db()
    return render_template("admin_pages/all_users.html", users=users, title="All Users")

def reset_func():
    '''
    function    - reset all user data
    :param      - 
    :return     -  redirect to admin page
    '''
    db = get_db()
    users = db.execute("SELECT user_id FROM users WHERE user_id != 'Admin';").fetchall()
    for user in users:
            user_id = user[0]
            db.execute("DROP TABLE IF EXISTS "+user_id+"_favourites;")
            db.execute("DELETE FROM users WHERE user_id = ?;", (user_id,))
    db.commit()
    close_db()
    return redirect(url_for("admin"))