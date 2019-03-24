# graduate-design
音乐推荐系统

数据库表：
singerdetail: 歌手信息
singerId,singerName,img1vUrl,Findex(歌手id，歌手名，歌手封面，歌手索引)
singleSong：单首歌曲
songId，songName，singerId，singerName，picUrl，albumname，duration（歌曲id，歌曲名，歌手id，歌手名，歌曲图片，专辑名，歌曲时长）
userrecommend：给用户推荐的歌曲。
songId，username（歌曲名，用户名）这两个组成主键
users：用户。
usernamename，password，love（用户名，密码，用户喜好）
