import json

# Include Flask packages
from flask import Flask, render_template, request
import copy

import MyBO

app = Flask(__name__)

@app.route('/api/similarity/<song_id>',methods = ['GET'])
def get_recommendation(song_id):
    result = MyBO.find_by_template('similarity',dict(song_id=song_id),['song_id'+str(i) for i in range(1,10)])

    rgb = []
    titles = []
    for k,v in result[0].items():
        r = MyBO.find_by_template('similarity',dict(song_id=v),['r','g','b'])
        r = MyBO.int_to_rgb(r[0])
        rgb.append(r)
        r = MyBO.find_by_template('song_info',dict(song_id=v),['title'])
        titles.append(r[0]['title'])

    return render_template("similarity.html",titles=titles,color=rgb)

@app.route('/',methods = ['GET'])
def log_in():
    return render_template("index.html")

@app.route('/api/login',methods = ['POST'])
def main_web():
    info1 = []
    result = MyBO.get_top_hot()
    for r in result:
        info1.append(MyBO.get_song_info(r))

    uid = request.form['user_id']
    info2 = []
    result = MyBO.find_by_template('recommendation',dict(user_id=uid),['song_id'+str(i) for i in range(1,7)])
    for k,v in result[0].items():
        info2.append(MyBO.get_song_info(v))

    return render_template("login.html",data1=info1,data2=info2)


if __name__ == '__main__':
    app.run(host=MyBO.public_ip(), port=80)
