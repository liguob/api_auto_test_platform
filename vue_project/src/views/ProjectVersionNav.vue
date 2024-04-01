<template>
  <div>
    <el-container>
      <el-header>
        <div>
          <span style="margin-right: 50px">项目:{{ project_name }}</span>
          <span>版本:{{ version_name }}</span>
        </div>
      </el-header>
      <el-container style="height: 100%;margin-top: 5px">
        <el-aside style="width: 200px">
          <el-menu
              :default-active="active_menu"
              router
              active-text-color="#ffd04b"
              background-color="#545c64"
              text-color="#fff"
              @select="handleSelect"
          >
            <el-menu-item
                v-for="item in menuItem"
                :index="item.url"
                :route="{path: item.url, query:{project_id: project_id,version_id: version_id}}"
            ><span slot="title">{{ item.name }}</span></el-menu-item>
          </el-menu>
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
import axios from "axios";

export default {
  name: "ProjectVersionMain",
  methods: {
    handleSelect(key) {
      this.active_menu = key
      if (key !== this.active_menu) {
        this.$router.push({path: key})
      }
    },
    versionDetail() {
      axios({
        url: '/version_detail',
        params: {id: this.$route.query.version_id}
      }).then(res => {
        this.project_name = res.data.project_data.project_name
        this.version_name = res.data.version_data.version_name
      })
    }
  },
  data() {
    return {
      active_menu: window.location.href.split('#')[1].split('?')[0],
      project_id: '',
      version_id: '',
      project_name: '',
      version_name: '',
      menuItem: [
        {url: '/version_case', name: '用例管理'},
        {url: '/version_params', name: '参数管理'},
        {url: '/version_task', name: '任务管理'},
        {url: '/version_report', name: '报告查看'},
      ]
    }
  },
  mounted() {
    this.project_id = Number(this.$route.query.project_id)
    this.version_id = Number(this.$route.query.version_id)
    this.versionDetail()
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
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #545c64;
  text-align: left;
  padding: 0 20px;
}

.el-aside .el-header {
  background-color: #545c64;
}

.el-main {
  padding: 5px;
  height: 840px;
}

.el-table /deep/ * {
  font-size: 14px !important;
}

</style>