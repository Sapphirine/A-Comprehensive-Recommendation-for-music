import pymysql
import json
import os, socket

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='similarity',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

def public_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def int_to_rgb(i):
    r = str(hex(int(i['r'])))[2:].upper()
    if len(r) < 2:
        r+="0"
    g = str(hex(int(i['g'])))[2:].upper()
    if len(g) < 2:
        g+="0"
    b = str(hex(int(i['b'])))[2:].upper()
    if len(b) < 2:
        b+="0"

    rgb = "#"+r+g+b
    return rgb

def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""
    if t is None:
        return s
    for (key,value) in t.items():
        if s != "":
            s += "AND "
        if type(value) == list:
            s += key + '="' + value[0] + '"'
        else:
            s += key + '="' + value + '"'

    if s != "":
        s = "WHERE " + s;

    return s

def find_by_template(table,t,fields=None,limit=None,offset=None):
    WC = template_to_where_clause(t)


    if fields is not None:
        q = "select " + ",".join(fields) + " from "+table + " " +WC
    else:
        q = "select * from "+table + " " +WC
    result = run_q(q, None, True)
    return result

def get_top_hot():
    q = "select * from hottest"
    result = run_q(q,None, True)
    id = []
    for r in result:
        id.append(r['song'])
    return id

def get_song_info(id):
    info = {}
    r = find_by_template('song_info',dict(song_id=id),['title'])
    info['title'] = r[0]['title']
    r = find_by_template('similarity',dict(song_id=id),['r','g','b'])
    info['color'] = int_to_rgb(r[0])
    ip = public_ip()
    info['link'] = "/api/similarity/"+id

    return info
