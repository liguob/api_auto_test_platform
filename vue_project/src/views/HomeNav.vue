<template>
  <div>
    <el-container style="height: 100%">
      <el-header>
        <div style="float: right">
          <span style="margin-right: 30px">欢迎您，{{ username }}</span>
          <el-button type="text" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-container style="margin-top: 5px">
        <el-aside style="width: 200px">
          <Menu></Menu>
        </el-aside>
        <el-container style="border-left: 1px black">
          <el-main>
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>

</template>

<script>
import Menu from "@/components/Menu.vue";
import axios from "axios";

export default {
  name: "HomeNav",
  components: {Menu},
  data(){
    return{
      username:'用户'
    }
  },
  methods:{
    logout(){
      axios({
        method:'post',
        url:'/logout'
      }).then(res=>{
        this.$router.push('/login')
      })
    }
  },
  mounted() {
    axios({
      method:'get',
      url:'/user_detail',
    }).then(res=>{
      this.username = res.data.first_name
    })
  }
}
</script>

<style scoped>
.el-menu {
  border-right-width: 0;
}

.el-header {
  background-color: #545c64;
  color: white;
  line-height: 60px;
}

.el-aside {
  background-color: #545c64;
  text-align: left;
}

.el-aside .el-header {
  background-color: #545c64;
}

.el-main {
  height: 840px;
  padding: 5px;
}
.el-table {
  font-size: 14px !important;
}
</style>