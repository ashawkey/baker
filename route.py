import time
from flask import Blueprint, request, jsonify
from mysql import *

bp = Blueprint('route', __name__, url_prefix='/api')

#@bp.route('/')
#def hello():
#    return "Hello!"

@bp.route('/get_blogs_meta')
def get_blogs_meta():
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_getMeta)
    meta = cur.fetchall()
    return jsonify(meta)

@bp.route('/get_blogs_content')
def get_blogs_content():
    name = request.args.get('name')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_getPost, (name,))
    text = cur.fetchone()
    return jsonify(text)

@bp.route('/search_blogs_content')
def search_blogs_content():
    keyword = request.args.get('keyword')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_searchPost, (keyword,))
    res = cur.fetchall()
    return jsonify(res)
    
@bp.route('/get_blogs_comments')
def get_blogs_comments():
    name = request.args.get('name')
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_getComments, (name,))
    text = cur.fetchall()
    return jsonify(text)

@bp.route('/post_comment', methods=('POST',))
def post_comment():
    ctime = time.time()
    title = request.form['title']
    name = request.form['name']
    body = request.form['body']
    db = mysql.get_db()
    cur = db.cursor()
    cur.execute(stmt_insertComments, (ctime, title, name, body))
    db.commit()
    return jsonify({
        'success': True,
        "status_code": 200,
        })