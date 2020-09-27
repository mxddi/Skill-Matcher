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
    uid = g.user['id']
    team_objects = db.execute(
        'SELECT teamname FROM team WHERE leader_id = ?',
        (uid,)
    ).fetchall()
    team_names = []
    for team in team_objects:
        team_names.append(team['teamname'])

    return render_template("teams/teams.html", teamnames=team_names)

@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
    if request.method == "POST":
        teamname = request.form['teamname']
        members = request.form['members']
        skillreqs = request.form['skills']
        emails = request.form['emails']
        db = get_db()
        error = None

        if not teamname:
            error = "Teamname is required."
        else:
            teamkey = teamname + str(random.randrange(1000))
            leader_id = g.user['id']
            members = g.user['username'] + "," + members
            emails = g.user['email'] + "," + emails
            db.execute(
                'INSERT INTO team (teamkey, teamname, leader_id, members, memberemails, skillreqs) VALUES (?, ?, ?, ?, ?, ?)',
                (teamkey, teamname, leader_id, members, emails, skillreqs)
            )
            db.commit()
            return redirect(url_for('teams.index'))
        flash(error)
        
    return render_template("teams/create.html")

@bp.route("/view/<teamname>", methods=('GET', 'POST'))
@login_required
def view(teamname):
    db = get_db()
    if request.method == "POST":
        newteamname = request.form['teamname']
        members = request.form['members']
        emails = request.form['emails']
        skillreqs = request.form['skills']
        error = None

        if not newteamname:
            error = "Teamname is required."
        else:
            leader_id = g.user['id']
            db.execute(
                'UPDATE team SET teamname = ?, members = ?, skillreqs = ? WHERE teamname = ? AND leader_id = ?',
                (newteamname, members, skillreqs, teamname, leader_id)
            )
            db.commit()
            return redirect(url_for('teams.index'))
        flash(error)

    team = db.execute(
        'SELECT * FROM team t WHERE t.leader_id = ? AND t.teamname = ?',
        (g.user['id'], teamname)
    ).fetchone()

    teamname, members, emails, skills = "", "", "", ""

    if team:
        teamname = team['teamname']
        members = team['members']
        emails = team['memberemails']
        skills = team['skillreqs']
    
    return render_template('teams/view.html', teamname=teamname, members=members, emails=emails, skills=skills)


@bp.route("/join/<teamname>", methods=('GET', 'POST'))
@login_required
def join(teamname):
    db = get_db()
    team = db.execute(
        'SELECT * FROM team WHERE teamname = ?',
        (teamname,)
    ).fetchone()

    if request.method == 'POST':
        username = g.user['username']
        email = request.form['email']
        error = None

        if not email:
            error = "Email is required."
        else:
            members = team['members'] + "," + username
            emails = team['memberemails'] + "," + email
            db.execute(
                'UPDATE team SET members = ?, memberemails = ? WHERE teamkey = ?',
                (members, emails, team['teamkey'])
            )
            db.commit()
            return redirect(url_for('teams.index'))
        flash(error)

    teamname, members, skills, canjoin = "", "", "", False

    if team:
        teamname = team['teamname']
        members = team['members']
        skills = team['skillreqs']
        canjoin = team['leader_id'] != g.user['id']

    return render_template("teams/join.html", teamname=teamname, members=members, skills=skills, canjoin=canjoin)