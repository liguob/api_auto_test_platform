<template>
  <div>
    <!--    <el-image :src="require('@/assets/login.jpg')" style="height: 100%; width: 100%"></el-image>-->
    <div class="bj_pic">
      <el-card id="login"  shadow="always">
        <div style="line-height: 50px; text-align: center; font-weight: bolder"><span>登录</span></div>
        <el-form @submit.native.prevent>
          <el-form-item>
            <el-input placeholder="请输入用户名" v-model="username">
              <i slot="prefix" class="el-icon-user-solid" style="color: #2e6da4"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-input placeholder="请输入密码" type="password" v-model="password">
              <i slot="prefix" class="el-icon-s-opportunity" style="color: #2e6da4"></i>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" style="width: 100%" @click="loginAuth" native-type="submit">登录</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      loginPic: require('@/assets/login.jpg'),
      username: '',
      password: '',
    }
  },
  methods: {
    loginAuth() {
      const data = new URLSearchParams();
      data.append('username', this.username)
      data.append('password', this.password)
      axios({
        method: 'post',
        url: '/login_auth',
        data: data
      }).then(res => {
        if (res.data.login_auth) {
          this.$router.push('/project_main')
        } else {
          this.$message({message: res.data.message, type: 'error'})
        }
      })
    },
  },
}
</script>

<style scoped>
#login {
  width: 300px;
  top: 50%;
  left: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  border: 0 solid #EBEEF5;
  box-shadow: 0 6px 24px 0 rgba(89, 94, 167, .11) !important;
}

.bj_pic {
  background: url('~@/assets/login.jpg');
  background-size: 100% 100%;
  position: fixed;
  height: 100%;
  width: 100%;
}

</style>