DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS teams;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE team (
    teamname TEXT PRIMARY KEY,
    leader INTEGER NOT NULL,
    --members list is string of ids separated by slash ex: 1/23/243
    members TEXT NOT NULL,
    --skillreq list is string separated by slash ex: c/java/positivity
    skillreqs TEXT NOT NULL,
    FOREIGN KEY (leader) REFERENCES user (id)
);