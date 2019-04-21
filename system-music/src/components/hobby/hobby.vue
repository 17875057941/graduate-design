<template>
  <div class="hobby">
    <div class="header">
      <h1>选择你的兴趣</h1>
      <p>为你推荐更多精彩内容</p>
    </div>
    <div class="btn-group">
      <button
        mini
        :class="item.isClicked ? 'btn-clicked': 'btn'"
        v-for="(item, index) in btnValue"
        :value="item.key"
        :key="index"
        @click="handleOnClick(item.isClicked,index)"
      >{{item.value}}</button>
    </div>
    <div class="submit">
      <button @click="gotoIndex">选好了</button>
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
        fetch('post', '/fixColdStart', {love: params}).then(res => {
        })
        this.$router.push({
          path: '/singer'
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
    background: url("../../common/image/white-bg1.jpg") no-repeat;
    background-size: cover;
    padding: 0 1rem;

    .header {
      margin-top: 3rem;
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
      margin-top: 30px;
      .btn {
        width: 100px;
        height: 100px;
        margin-right: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        border: none;
      }
      .btn-clicked {
        width: 100px;
        height: 100px;
        margin-right: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        border: none;
        background: gray;
        opacity: 0.5;
      }
    }
    .submit {
      text-align: center;
      margin-top: 40px;
      button {
        width: 200px;
        height: 50px;
        border: none;
        background: darkgray;
        border-radius: 25px;
      }
    }
  }
</style>
