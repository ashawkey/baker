from flask import Blueprint, request, jsonify
from baker.mysql import *

bp = Blueprint('route', __name__)


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
    cur.execute(stmt_search, (keyword,))
    res = cur.fetchall()
    return jsonify(res)
    

