#coding=utf-8
import pymysql
from flask import Flask, flash, request, session
from flask_cors import *
import json
import requests
import gensim
import os
from datetime import timedelta
connection = pymysql.connect(host='localhost',port=3306,user='root',db='musicsystem')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
CORS(app, supports_credentials=True)

def get_songId(username):#获取当前用户所有推荐歌曲id
    with connection.cursor() as cursor:
        cursor.execute('SELECT songId FROM USERRECOMMEND where username = %s',username)
        result = cursor.fetchall()
        ls = []
        for item in result:
            ls.append(item[0])
        return ls
@app.route('/singer',methods=['GET'])
#query singer
def get_singer():
    sql = "SELECT * FROM singerdetail"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        singerlist = cursor.fetchall()

    dataList = []

    for item in singerlist:
        re = {}
        re['Fsinger_id'] = item[0]
        re['Fsinger_mid'] = item[0]
        re['Fsinger_name'] = item[1]
        re['img1v1Url'] = item[2]
        re['Findex'] = item[3]
        dataList.append(re)
    result = {'list': dataList}
    return json.dumps(result) # tranform to json data

@app.route('/singer/<singerId>',methods=['GET'])
#query singerdetail
def get_singerdetail(singerId):#查询歌手所有歌曲
    sql = "SELECT * FROM singlesong where singerId = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, singerId)
        singerlist = cursor.fetchall()

        dataList = []

        for item in singerlist:
            re = {}
            re['songid'] = item[0]
            re['songname'] = item[1]
            re['songmid'] = item[2]
            re['singer'] = item[3]
            re['picUrl'] = item[4]
            re['albumname'] = item[5]
            re['duration'] = item[6]

            singerInfo = {'id': item[2], 'mid': item[2], 'name': item[3]}
            re['singer'] = [singerInfo]
            it = {'musicData': re}
            dataList.append(it)
        result = {'list': dataList}
    return json.dumps(result)  # tranform to json data

# http://music.163.com/api/song/lyric?os=pc&id='+id+'&lv=-1&kv=-1&tv=-1
@app.route('/lyric/<songId>', methods=['GET'])
def get_lyric(songId):
    url = 'http://music.163.com/api/song/lyric?os=pc&id='+songId+'&lv=-1&kv=-1&tv=-1'
    r = requests.get(url)
    json_obj = r.text
    j = json.loads(json_obj)
    return json.dumps({'lyric': j['lrc']['lyric']})

@app.route('/recommend', methods=['POST'])
def create_recommend():#产生推荐
    song_id_list = json.loads(request.get_data())
    if len(song_id_list) != 0 and 'username' in session:
        model_str = 'songVec.model'
        model = gensim.models.Word2Vec.load(model_str)
        result_song_list = []
        for song_id in song_id_list:
            result_song_list += model.most_similar(song_id)

        for item in result_song_list:
            # songId => item[0]
            with connection.cursor() as cur:
                cur.execute('INSERT IGNORE INTO `USERRECOMMEND`(`songId`,`username`) values (%s,%s)',(item[0],session['username']))
                connection.commit()

    if 'username' in session:
        recommend_songid_list = get_songId(session['username'])
        songList = []
        for item in recommend_songid_list:
            sql = "SELECT * FROM singlesong where songId = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, item)
                song = cursor.fetchone()
                re = {}
                re['songid'] = song[0]
                re['songname'] = song[1]
                re['songmid'] = song[2]
                re['singer'] = song[3]
                re['picUrl'] = song[4]
                re['albumname'] = song[5]
                re['duration'] = song[6]
                singerInfo = {'id': song[2], 'mid': song[2], 'name': song[3]}
                re['singer'] = [singerInfo]
                it = {'musicData': re}
                songList.append(it)
        return json.dumps({'list': songList})
    else:
        return 'Dont have history play'

@app.route('/login',methods=['POST'])
def login():
    userInfo = json.loads(request.get_data())
    if not userInfo['username'] or not userInfo['password']:
        return json.dumps({'code': 5})
    if 'username' in session and session['username'] == userInfo['username']:
        return json.dumps({'code': 6})
    with connection.cursor() as cursor:
        cursor.execute('SELECT password from users where username = %s' ,(userInfo['username']))
        re = cursor.fetchone()
        if not re:
            return json.dumps({'code': 7})
        if userInfo['password'] == re[0] or not userInfo['username']:
            session['username'] = userInfo['username']
            return json.dumps({'code': 1})
        else:
            return json.dumps({'code': 3})
@app.route('/register', methods=['POST'])
def register():
    userInfo = json.loads(request.get_data())
    if not userInfo['username'] or not userInfo['password']:
        return json.dumps({'code': 5})
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users where username = %s"
        cursor.execute(sql, userInfo['username'])
        result = cursor.fetchone()
        if result:#user is already exists
            if 'username' not in session:
                session['username'] = userInfo['username']
            return json.dumps({'code': 2})
        elif userInfo['password'] == userInfo['repassword']:
            # insert into mysql
            sql2 = "INSERT INTO `USERS`(username,password) values (%s,%s)"
            cursor.execute(sql2,(userInfo['username'],userInfo['password']))
            connection.commit()
            if 'username' not in session:
                session['username'] = userInfo['username']
            return json.dumps({'code': 1}) #success
        else:# the first password and second password is different
            return json.dumps({'code': 0})

@app.route('/logout', methods=['POST'])
def logout():
    print('logout', session)
    if 'username' in session:
        session.pop('username')
        return '退出登录成功'
    else:
        return '退出登录失败'
@app.route('/get_session', methods=['GET'])
def get_session():
    user = session.get('username')
    return str(user)
if __name__ == '__main__':
    app.run(host='localhost',debug=True)