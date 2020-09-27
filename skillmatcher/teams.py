import functools

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
    teamstring = db.execute(
        'SELECT teamname FROM team t JOIN user u ON t.leader_id = u.id'
    ).fetchall()
    return render_template("teams/teams.html", teamnames=teamstring)
    # teamnames = teamstring.split("/")
    # return render_template("teams/teams.html")