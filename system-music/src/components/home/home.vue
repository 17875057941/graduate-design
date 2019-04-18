<template>
 <div class="home">
   <div class="btn-group">
     <x-button @click.native="login" type="primary">登陆</x-button>
     <x-button @click.native="register">注册</x-button>
   </div>
 </div>
</template>

<script>
  import { XButton } from 'vux'
  export default {
    components: {
      XButton
    },
    methods: {
      login() {
        this.$router.push('/login')
      },
      register() {
        this.$router.push('/register')
      }
    }
  }
</script>

<style scoped>
  .home {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: url("../../common/image/cover.jpg") no-repeat;
    background-size: cover;
  }
  .btn-group {
    width: 300px;
    margin: 0 auto;
    position: relative;
    top: 300px;
  }
</style>
