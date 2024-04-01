<template>
  <div>
    <el-menu
        :default-active="menu_path"
        class="el-menu-vertical-demo"
        :default-openeds="open_menu"
        @open="handleOpen"
        router
        active-text-color="#ffd04b"
        background-color="#545c64"
        text-color="#fff"
        style="overflow: hidden;width: 200px"
        @close="handleClose">
      <!--      <el-menu-item index="/">-->
      <!--        <i class="el-icon-house"></i>-->
      <!--        <span slot="title">首页home</span>-->
      <!--      </el-menu-item>-->
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-star-off"></i>
          <span>功能区</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/project_main">项目管理</el-menu-item>
          <el-menu-item index="/version_manage">项目版本</el-menu-item>
          <!--          <el-menu-item index="/env_manage">环境管理</el-menu-item>-->
          <el-menu-item index="/api_manage">接口库管理</el-menu-item>
          <el-menu-item index="/practice">常用工具</el-menu-item>
          <!--          <el-menu-item index="1-4">线上监控</el-menu-item>-->
          <!--          <el-menu-item index="1-5">接口文档</el-menu-item>-->
          <!--          <el-menu-item index="1-6">Postman</el-menu-item>-->
          <!--          <el-menu-item index="1-7">在线抓包</el-menu-item>-->
        </el-menu-item-group>
      </el-submenu>
      <!--      <el-submenu index="2">-->
      <!--        <template slot="title">-->
      <!--          <i class="el-icon-s-custom"></i>-->
      <!--          <span>用户区</span>-->
      <!--        </template>-->
      <!--        <el-menu-item-group>-->
      <!--          <el-menu-item index="/user_detail">个人资料</el-menu-item>-->
      <!--          <el-menu-item index="2-2">个人贡献</el-menu-item>-->
      <!--          <el-menu-item index="2-3">发送消息</el-menu-item>-->
      <!--          <a href="/logout/">-->
      <!--            <el-menu-item>退出</el-menu-item>-->
      <!--          </a>-->
      <!--        </el-menu-item-group>-->
      <!--      </el-submenu>-->
      <el-submenu index="3" v-if="is_user">
        <template slot="title">
          <i class="el-icon-setting"></i>
          <span>维护区</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/user_manage">用户管理</el-menu-item>
          <!--          <el-menu-item index="3-3">查看日志</el-menu-item>-->
          <el-menu-item index="/public_notice">发布公告</el-menu-item>
          <!--          <el-menu-item index="3-5">权限管理</el-menu-item>-->
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Menu",
  data() {
    return {
      open_menu: ['1', '2'],
      menu_path: window.location.href.split('#')[1].split('?')[0],
      is_user: false,
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      this.open_menu.push(key)
    },
    handleClose(key, keyPath) {
      this.open_menu.splice(this.open_menu.indexOf(key), 1)
    },
  },
  mounted() {
    axios({
      method: 'get',
      url: '/menu_power/',
    }).then(res =>
        this.is_user = res.data.is_user)
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}

.el-aside {
  background-color: #545c64;
}

.el-menu {
  border-right-width: 0;
}

/*::-webkit-scrollbar-track {*/
/*  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);*/
/*  background-color: white;*/
/*  border-radius: 3px;*/
/*}*/

/*::-webkit-scrollbar-thumb {*/
/*  border-radius: 10px;*/
/*  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);*/
/*  background-color: #b3b3b3;*/
/*}*/
</style>
