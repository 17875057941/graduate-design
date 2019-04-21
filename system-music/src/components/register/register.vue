<template>
  <div class="register">
    <div class="register" v-show="false">
      <x-header>注册</x-header>
      <group>
        <x-input type="text" title="用户名：" v-model="username" placeholder="请输入用户名"></x-input>
        <x-input type="password" title="密码：" v-model="password" placeholder="请输入密码"></x-input>
        <x-input type="password" title="确认密码：" v-model="repassword" placeholder="请确认密码"></x-input>
      </group>
      <x-button @click.native="register" type="primary">立即注册</x-button>
      <div>{{message}}</div>
    </div>

    <div class="page-container">
      <h1>注册</h1>
      <div>
        <input type="text" title="用户名：" v-model="username" placeholder="请输入用户名">
        <input type="password" title="密码：" v-model="password" placeholder="请输入密码">
        <input type="password" title="确认密码：" v-model="repassword" placeholder="请确认密码">
        <button @click="register" type="primary">立即注册</button>
        <div class="error"><span>+</span></div>
      </div>
      <div class="connect">
        <p style="width: 100%;"><router-link class="facebook" to="/login">去登陆</router-link></p>
      </div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import { Group, XInput, XButton, XHeader } from 'vux'
  import {fetch} from 'common/js/fetch'
  export default {
    components: {
      Group,
      XInput,
      XButton,
      XHeader
    },
    data() {
      return {
        username: '',
        password: '',
        repassword: '',
        message: ''
      }
    },
    methods: {
      register() {
        fetch('post', 'register', this.$data).then(res => {
          if (res.data.code === 0) {
            this.$data.message = '密码不一致'
          } else if (res.data.code === 1) {
            this.$data.message = ''
            this.$router.push({path: '/hobby'})
          } else if (res.data.code === 2) {
            this.$data.message = '用户已经存在'
          } else if (res.data.code === 5) {
            this.$data.message = '用户名或密码不能为空'
          }
          this.$vux.toast.show({
            text: this.$data.message,
            type: 'text'
          })
        })
      }
    }
  }
</script>

<style lang="stylus" scoped>
  @import url("~common/css/reset.css")
  body {
    background: #f8f8f8;
    font-family: 'PT Sans', Helvetica, Arial, sans-serif;
    text-align: center;
    color: #fff;
  }

  .register {
    width: 100%;
    position: fixed;
    top: -15px;
    bottom: 0;
    left: 0;
    right: 0;
    background: url("../../common/image/1.jpg") no-repeat;
    background-size: cover;
  }
  .page-container {
      margin: 120px auto 0 auto;
  }

  h1 {
    font-size: 30px;
    font-weight: 700;
    text-shadow: 0 1px 4px rgba(0,0,0,.2);
    text-align: center
  }

  div {
    position: relative;
    width: 305px;
    margin: 15px auto 0 auto;
    text-align: center;
  }

  input {
    width: 270px;
    height: 42px;
    margin-top: 25px;
    padding: 0 15px;
    background: #2d2d2d;
    background: rgba(45,45,45,.15);
    -moz-border-radius: 6px;
    -webkit-border-radius: 6px;
    border-radius: 6px;
    border: 1px solid #3d3d3d;
    border: 1px solid rgba(255,255,255,.15);
    -moz-box-shadow: 0 2px 3px 0 rgba(0,0,0,.1) inset;
    -webkit-box-shadow: 0 2px 3px 0 rgba(0,0,0,.1) inset;
    box-shadow: 0 2px 3px 0 rgba(0,0,0,.1) inset;
    font-family: 'PT Sans', Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: #fff;
    text-shadow: 0 1px 2px rgba(0,0,0,.1);
    -o-transition: all .2s;
    -moz-transition: all .2s;
    -webkit-transition: all .2s;
    -ms-transition: all .2s;
  }

  input:-moz-placeholder { color: #fff; }
  input:-ms-input-placeholder { color: #fff; }
  input::-webkit-input-placeholder { color: #fff; }

  input:focus {
    outline: none;
    -moz-box-shadow:
        0 2px 3px 0 rgba(0,0,0,.1) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    -webkit-box-shadow:
        0 2px 3px 0 rgba(0,0,0,.1) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    box-shadow:
        0 2px 3px 0 rgba(0,0,0,.1) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
  }

  button {
    cursor: pointer;
    width: 300px;
    height: 44px;
    margin-top: 25px;
    padding: 0;
    background: #ef4300;
    -moz-border-radius: 6px;
    -webkit-border-radius: 6px;
    border-radius: 6px;
    border: 1px solid #ff730e;
    -moz-box-shadow:
        0 15px 30px 0 rgba(255,255,255,.25) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    -webkit-box-shadow:
        0 15px 30px 0 rgba(255,255,255,.25) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    box-shadow:
        0 15px 30px 0 rgba(255,255,255,.25) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    font-family: 'PT Sans', Helvetica, Arial, sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 1px 2px rgba(0,0,0,.1);
    -o-transition: all .2s;
    -moz-transition: all .2s;
    -webkit-transition: all .2s;
    -ms-transition: all .2s;
  }

  button:hover {
    -moz-box-shadow:
        0 15px 30px 0 rgba(255,255,255,.15) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    -webkit-box-shadow:
        0 15px 30px 0 rgba(255,255,255,.15) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    box-shadow:
        0 15px 30px 0 rgba(255,255,255,.15) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
  }

  button:active {
    -moz-box-shadow:
        0 15px 30px 0 rgba(255,255,255,.15) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    -webkit-box-shadow:
        0 15px 30px 0 rgba(255,255,255,.15) inset,
        0 2px 7px 0 rgba(0,0,0,.2);
    box-shadow:        
        0 5px 8px 0 rgba(0,0,0,.1) inset,
        0 1px 4px 0 rgba(0,0,0,.1);

    border: 0px solid #ef4300;
  }

  .error {
    display: none;
    position: absolute;
    top: 27px;
    right: -55px;
    width: 40px;
    height: 40px;
    background: #2d2d2d;
    background: rgba(45,45,45,.25);
    -moz-border-radius: 8px;
    -webkit-border-radius: 8px;
    border-radius: 8px;
  }

  .error span {
    display: inline-block;
    margin-left: 2px;
    font-size: 40px;
    font-weight: 700;
    line-height: 40px;
    text-shadow: 0 1px 2px rgba(0,0,0,.1);
    -o-transform: rotate(45deg);
    -moz-transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
  }

  .connect {
    width: 305px;
    margin: 35px auto 0 auto;
    font-size: 18px;
    font-weight: 700;
    text-shadow: 0 1px 3px rgba(0,0,0,.2);
  }

  .connect a {
    display: inline-block;
    // width: 32px;
    height: 35px;
    margin-top: 15px;
    font-size: 16px;
    -o-transition: all .2s;
    -moz-transition: all .2s;
    -webkit-transition: all .2s;
    -ms-transition: all .2s;
  }

// .connect a.facebook { background: url(../img/facebook.png) center center no-repeat; }
// .connect a.twitter { background: url(../img/twitter.png) center center no-repeat; }

// .connect a:hover { background-position: center bottom; }
</style>
