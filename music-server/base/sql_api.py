import pymysql
from flask import Flask, request
from flask_cors import *
import json
import requests
import gensim

connection = pymysql.connect(host='localhost',port=3306,user='root',db='musicsystem')

app = Flask(__name__)
CORS(app, supports_credentials=True)

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
def get_singerdetail(singerId):
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
def create_recommend():
    pass
    song_id_list = json.loads(request.get_data())
    if len(song_id_list) != 0:
        model_str = 'songVec.model'
        model = gensim.models.Word2Vec.load(model_str)
        result_song_list = []
        for song_id in song_id_list:
            result_song_list += model.most_similar(song_id)
            print(len(result_song_list))
        songList = []
        for item in result_song_list:
            # songId => item[0]
            sql = "SELECT * FROM singlesong where songId = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, item[0])
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

if __name__ == '__main__':
    app.run(host='localhost',debug=True)