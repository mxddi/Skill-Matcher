import functools, random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from skillmatcher.auth import login_required

from skillmatcher.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')

@bp.route("/")
@login_required
def index():
    db = get_db()
    team_objects = db.execute(
        'SELECT teamname FROM team t JOIN user u ON t.leader_id = u.id'
    ).fetchall()
    team_names = []
    for team in team_objects :
        team_names.append(team['teamname'])
    return render_template("teams/teams.html", teamnames=team_names)
    # teamnames = teamstring.split("/")
    # return render_template("teams/teams.html")

@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
    if request.method == "POST":
        teamname = request.form['teamname']
        members = request.form['members']
        skillreqs = request.form['skills']
        db = get_db()
        error = None

        if not teamname:
            error = "Teamname is required."
        else:
            teamkey = teamname + str(random.randrange(1000))
            leader_id = g.user['id']
            members = g.user['username'] + "," + members
            db.execute(
                'INSERT INTO team (teamkey, teamname, leader_id, members, skillreqs) VALUES (?, ?, ?, ?, ?)',
                (teamkey, teamname, leader_id, members, skillreqs)
            )
            db.commit()
            return redirect(url_for('teams.index'))
        flash(error)
        
    return render_template("teams/create.html")