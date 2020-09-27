DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS team;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamkeys TEXT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE team (
    teamkey TEXT PRIMARY KEY,
    teamname TEXT NOT NULL,
    leader_id INTEGER NOT NULL,
    --members list is string of ids separated by slash ex: 1/23/243
    members TEXT NOT NULL,
    --skillreq list is string separated by slash ex: c/java/positivity
    skillreqs TEXT,
    FOREIGN KEY (leader_id) REFERENCES user (id)
);