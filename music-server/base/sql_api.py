#coding=utf-8
import pymysql
from flask import Flask, flash, request, session
from flask_cors import *
import json
import requests
import gensim
import os
from datetime import timedelta
# from common.log import *
connection = pymysql.connect(host='localhost',port=3306,user='root',passwd='123456',db='musicsystem')

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

#获取歌词
# http://music.163.com/api/song/lyric?os=pc&id='+id+'&lv=-1&kv=-1&tv=-1
@app.route('/lyric/<songId>', methods=['GET'])
def get_lyric(songId):
    url = 'http://music.163.com/api/song/lyric?os=pc&id='+songId+'&lv=-1&kv=-1&tv=-1'
    r = requests.get(url)
    json_obj = r.text
    j = json.loads(json_obj)
    return json.dumps({'lyric': j['lrc']['lyric']})

#产生推荐
@app.route('/recommend', methods=['POST'])
def create_recommend():
    song_id_list = json.loads(request.get_data())
    print(song_id_list, 'p')
    if len(song_id_list) != 0 and 'username' in session:
        model_str = 'songVec.model'
        model = gensim.models.Word2Vec.load(model_str)
        result_song_list = []
        for song_id in song_id_list:
            result_song_list += model.wv.most_similar(positive=[str(song_id)]) # 转为字符串

        for item in result_song_list:
            # songId => item[0]
            with connection.cursor() as cur:
                cur.execute('INSERT IGNORE INTO `USERRECOMMEND`(`songId`,`username`) values (%s,%s)',(item[0],session['username']))
                connection.commit()

    if 'username' in session:
        recommend_songid_list = get_songId(session['username']) #获取推荐过的所有id列表
        songList = []
        if not len(recommend_songid_list):
            with connection.cursor() as cursor:
                sql = "select love from users where username = %s"
                cursor.execute(sql, (session['username']))
                love = cursor.fetchone()
                loveList = love[0].split(',') #['classical', 'dew', 'pop']
                print(loveList, 'love')
                sql_love = "select * from singlesong where style in (%s) limit 20"%",".join(['%s'] * len(loveList))
                print(sql_love, 'p')
                cursor.execute(sql_love,(loveList))
                songData = cursor.fetchall()
                for song in songData:
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
            pass
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
        cursor.execute('SELECT password from users where username = %s',(userInfo['username']))
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
    if 'username' in session:
        session.pop('username')
        return '退出登录成功'
    else:
        return '退出登录失败'
@app.route('/get_session', methods=['GET'])
def get_session():
    user = session.get('username')
    return str(user)

@app.route('/search', methods=['post'])
def search():
    value = json.loads(request.get_data())
    with connection.cursor() as cursor:
        sql = "SELECT * FROM singleSong where songName = %s OR singerName = %s LIMIT 10"
        cursor.execute(sql, (value['params'], value['params']))
        songListData = cursor.fetchall()
        songList = []
        for song in songListData:
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

        result = {
            'data':
                {'song':
                     {
                         'list': songList
                     }
                },
            'code': 0
        }
        return json.dumps(result)
    pass
@app.route('/fixColdStart', methods=['post']) #解决冷启动问题，先给根据喜好给新用户推荐音乐
def fixColdStart():
    data = json.loads(request.get_data())
    username = session.get('username')
    if 'username' in session:
        sql = "update USERS set love = %s where username = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (data['love'],username))
            connection.commit()
        connection.close()
        return json.dumps({'data': {'code': 0}})
@app.route('/getRankList', methods=['post']) #获取排行榜歌单
def getHotRankLst():
    data = json.loads(request.get_data())
    sql = "SELECT * FROM SINGLESONG WHERE listName = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, (data['listName']))
        songListData = cursor.fetchall()
        songList = []
        for song in songListData:
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
        result = {
            'song': {
                'list': songList
            },
            'code': 0
        }
        return json.dumps(result)

@app.route('/getAllRankList', methods=['post'])
def getAllRankList():
    rankList = [
        {'name': 'biaosheng', 'picUrl': 'http://p2.music.126.net/DrRIg6CrgDfVLEph9SNh7w==/18696095720518497.jpg?param=150y150'},
        {'name': 'Billboard', 'picUrl': 'http://p2.music.126.net/EBRqPmY8k8qyVHyF8AyjdQ==/18641120139148117.jpg?param=150y150' },
        {'name': 'dianyin', 'picUrl': 'http://p2.music.126.net/5tgOCD4jiPKBGt7znJl-2g==/18822539557941307.jpg?param=150y150'},
        {'name': 'douying', 'picUrl': 'http://p1.music.126.net/bZvjH5KTuvAT0YXlVa-RtQ==/109951163326845001.jpg?param=150y150'},
        {'name': 'gudian',  'picUrl': 'http://p1.music.126.net/BzSxoj6O1LQPlFceDn-LKw==/18681802069355169.jpg?param=150y150'},
        {'name': 'hotSong', 'picUrl': 'http://p1.music.126.net/GhhuF6Ep5Tq9IEvLsyCN7w==/18708190348409091.jpg?param=150y150' },
        {'name': 'newSong', 'picUrl': 'http://p2.music.126.net/N2HO5xfYEqyQ8q6oxCw8IQ==/18713687906568048.jpg?param=150y150'}]
    allData = []
    for item in rankList:
        single = {}
        with connection.cursor() as cursor:
            sql = "select * from singleSong where listName = %s limit 3"
            cursor.execute(sql,(item['name']))
            songleListData = cursor.fetchall()
            songleList = []
            for song in songleListData:
                re = {}
                re['songid'] = song[0]
                re['songname'] = song[1]
                re['songmid'] = song[2]
                re['singername'] = song[3]
                re['picUrl'] = song[4]
                re['albumname'] = song[5]
                re['duration'] = song[6]
                singerInfo = {'id': song[2], 'mid': song[2], 'name': song[3]}
                re['singer'] = [singerInfo]
                # it = {'musicData': re}
                single['listName'] = song[8]
                songleList.append(re)
        single['picUrl'] = item['picUrl']
        single['songList'] = songleList
        allData.append(single)
        result = {'data': allData}
    return json.dumps(allData)
    pass
if __name__ == '__main__':
    # logger.info('This is info')
    # logger.warning('This is warning')
    # logger.error('This is error')
    app.run(host='localhost',debug=True)
