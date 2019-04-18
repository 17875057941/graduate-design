<template>
  <music-list :songs="songs"></music-list>
</template>

<script type="text/ecmascript-6">
  import {loadPlay} from 'common/js/cache'
  import {fetch} from 'common/js/fetch'
  import MusicList from 'components/music-list/music-list'
  import {createSong} from 'common/js/song'
  export default {
    data() {
      return {
        playHistoryIdList: [],
        songs: []
      }
    },
    created() {
      let historyList = loadPlay()
      historyList.forEach(item => {
        this.playHistoryIdList.push(item.id)
      })
    },
    mounted() {
      this.getRecommendMusic()
    },
    methods: {
      getRecommendMusic() {
        fetch('post', 'http://localhost:5000/recommend', this.playHistoryIdList).then(res => {
          this.songs = this._normalizeSongs(res.data.list)
          console.log(res.data.list)
        })
      },
      _normalizeSongs(list) {
        let ret = []
        list.forEach((item) => {
          let {musicData} = item
          if (musicData.songid && musicData.albumname) {
            console.log(9)
            ret.push(createSong(musicData))
          }
        })
        return ret
      }
    },
    components: {
      MusicList
    }
  }
</script>

<style scoped lang="stylus" rel="stylesheet/stylus">
  @import "~common/stylus/variable"

  .recommend
    position: fixed
    width: 100%
    top: 88px
    bottom: 0
    .recommend-content
      height: 100%
      overflow: hidden
      .slider-wrapper
        position: relative
        width: 100%
        overflow: hidden
      .recommend-list
        .list-title
          height: 65px
          line-height: 65px
          text-align: center
          font-size: $font-size-medium
          color: $color-theme
        .item
          display: flex
          box-sizing: border-box
          align-items: center
          padding: 0 20px 20px 20px
          .icon
            flex: 0 0 60px
            width: 60px
            padding-right: 20px
          .text
            display: flex
            flex-direction: column
            justify-content: center
            flex: 1
            line-height: 20px
            overflow: hidden
            font-size: $font-size-medium
            .name
              margin-bottom: 10px
              color: $color-text
            .desc
              color: $color-text-d
      .loading-container
        position: absolute
        width: 100%
        top: 50%
        transform: translateY(-50%)
</style>
