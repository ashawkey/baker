import os
import glob
import time
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flaskext.mysql import MySQL

SCHEMA = [
    '''
    CREATE TABLE IF NOT EXISTS posts (
        title VARCHAR(256) NOT NULL,
        ctime BIGINT NOT NULL,
        mtime BIGINT NOT NULL,
        body TEXT NOT NULL,
        PRIMARY KEY (title),
        FULLTEXT (title, body) WITH PARSER ngram
    ) ENGINE=INNODB;
    ''',
    '''
    CREATE TABLE IF NOT EXISTS comments (
        pid int NOT NULL auto_increment,
        time BIGINT NOT NULL,
        title VARCHAR(256) NOT NULL,
        nickname VARCHAR(64) NOT NULL,
        comment VARCHAR(1024) NOT NULL,
        PRIMARY KEY (pid),
        FOREIGN KEY (title) 
            REFERENCES posts (title)
            ON DELETE CASCADE
    ) ENGINE=INNODB;
    ''',
]

mysql = MySQL()

stmt_insertPosts = "replace into posts(title, ctime, mtime, body) values(%s, %s, %s, %s)"
stmt_getMeta = "select title, ctime, mtime from posts order by mtime desc"
stmt_getPost = "select body from posts where title = (%s)"
stmt_search = "select title, ctime, mtime from posts where match (title, body) against (%s in boolean mode) order by mtime desc"
stmt_insertComments = "insert into comments(time, title, nickname, comment) values(%s, %s, %s, %s)"
stmt_getComments = "select time, nickname, comment from comments where title = (%s) order by time"

def init_db():
    db = mysql.get_db()
    cur = db.cursor()
    for stmt in SCHEMA:
        cur.execute(stmt)
    db.commit()
    db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def update_db():
    db = mysql.get_db()
    cur = db.cursor()

    blogs = glob.glob("blogs/*.md")
    res = []
    for blog in blogs:
        print(f"[update db] add {blog}")
        
        with open(blog, 'r', encoding='UTF-8') as f:
            body = f.read()
        
        cur.execute(stmt_insertPosts, (os.path.basename(blog), int(os.path.getctime(blog)), int(os.path.getmtime(blog)), body))
    
    db.commit()
    db.close()
    
@click.command('update-db')
@with_appcontext
def update_db_command():
    """always call after init-db."""
    update_db()
    click.echo('Updated the database.')

def init_app(app):
    mysql.init_app(app)
    app.cli.add_command(init_db_command)
    app.cli.add_command(update_db_command)