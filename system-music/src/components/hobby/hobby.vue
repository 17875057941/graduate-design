<template>
  <div class="hobby">
    <div class="header">
      <h1>选择你的兴趣</h1>
      <p>为你推荐更多精彩内容</p>
    </div>
    <div class="btn-group">
      <x-button
        mini
        :class="item.isClicked ? 'btn-clicked': 'btn'"
        v-for="(item, index) in btnValue"
        :value="item.key"
        @click.native="handleOnClick(item.isClicked,index)"
      >{{item.value}}</x-button>
    </div>
    <div class="submit">
      <x-button mini @click.native="gotoIndex">选好了</x-button>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import { XButton } from 'vux'
  import { fetch } from 'common/js/fetch'

  export default {
    components: {
      XButton
    },
    data () {
      return {
        btnValue: [{
          key: 'classical',
          value: '古典',
          isClicked: false
        }, {
          key: 'dew',
          value: '清新',
          isClicked: false
        }, {
          key: 'pop',
          value: '流行',
          isClicked: false
        }, {
          key: 'rock',
          value: '摇滚',
          isClicked: false
        }, {
          key: 'romatic',
          value: '浪漫',
          isClicked: false
        }, {
          key: 'sad',
          value: '伤感',
          isClicked: false
        }]
      }
    },
    methods: {
      gotoIndex () {
        let hobbyList = []
        this.btnValue.forEach(item => {
          if (item.isClicked) {
            hobbyList.push(item.key)
          }
        })
        let params = hobbyList.join(',')
        fetch('post', 'http://localhost:5000/fixColdStart', {love: params}).then(res => {
        })
      },
      handleOnClick (isClicked, index) {
        this.btnValue[index].isClicked = !isClicked
      }
    }
  }
</script>
<style scoped lang="stylus" rel="stylesheet/stylus">
  .hobby {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: url("../../common/image/white-bg.jpg") no-repeat;
    background-size: cover;
    padding: 0 0.3rem;

    .header {
      margin-top: 1rem;
      h1 {
        font-size: 40px;
        color: #000
        margin-bottom: 0.6rem;
      }
      p {
        color: gray;
      }
    }
    .btn-group {
      .btn {
        border-radius: 50%;
      }
      .btn-clicked {
        background: gray;
        border-radius: 50%;
      }
    }
  }
</style>
