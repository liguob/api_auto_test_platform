<template>
  <div>
    <el-container>
      <el-aside style="height: 100%;width: 210px">
        <Menu></Menu>
      </el-aside>
      <el-container style="border-left: 1px black">
        <el-main>
          <template>
            <el-tabs v-model="activeName" @tab-click="handleClick">
              <el-tab-pane name="用户管理">
                <span slot="label" style="font-size: 20px">用户管理</span>
                <el-table :data="user_list" type="index" border :highlight-current-row="true">
                  <template slot-scope="scope">
                    <el-table-column label="序号" type="index" width="80" align="center"></el-table-column>
                    <el-table-column label="姓名" prop="name" width="150" align="center"></el-table-column>
                    <el-table-column label="用户名" prop="username" width="300" align="center"></el-table-column>
                    <el-table-column label="花名" prop="nickname" align="center"></el-table-column>
                    <el-table-column label="职称" prop="title" width="150" align="center"></el-table-column>
                    <el-table-column width="150" align="center">
                      <template slot="header">
                        <el-button type="primary" @click="openNewUser">新增</el-button>
                      </template>
                      <template slot-scope="scope">
                        <el-button type="danger" @click="deleteUser(scope.row.user)">删除</el-button>
                      </template>
                    </el-table-column>
                  </template>
                </el-table>
              </el-tab-pane>
              <el-tab-pane name="权限管理">
                <span slot="label" style="font-size: 20px">权限管理</span>
                <el-table :data="power_list" type="index" border :highlight-current-row="true">
                  <template slot-scope="scope">
                    <el-table-column label="序号" type="index" width="80" align="center"></el-table-column>
                    <el-table-column label="权限名称" prop="name" width="150" align="center"></el-table-column>
                    <el-table-column label="所属模块" prop="module_name" align="center"></el-table-column>
                    <el-table-column label="路由地址" prop="path" align="center"></el-table-column>
                    <el-table-column width="150" align="center">
                      <template slot="header">
                        <el-button type="primary" @click="openNewPower">新增</el-button>
                      </template>
                      <el-button type="danger">删除</el-button>
                    </el-table-column>
                  </template>
                </el-table>
              </el-tab-pane>
              <el-tab-pane name="角色管理">
                <span slot="label" style="font-size: 20px">角色管理</span>
                <el-table :data="role_list" border :highlight-current-row="true">
                  <template slot-scope="scope">
                    <el-table-column label="序号" type="index" width="80" align="center"></el-table-column>
                    <el-table-column label="角色名称" prop="name" align="center"></el-table-column>
                    <el-table-column label="角色描述" prop="des" align="center"></el-table-column>
                    <el-table-column align="center" width="150">
                      <template slot="header">
                        <el-button type="primary">新增</el-button>
                      </template>
                      <template slot-scope="scope">
                        <el-button type="danger">删除</el-button>
                      </template>
                    </el-table-column>
                  </template>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </template>
        </el-main>
        <el-dialog title="用户信息" :visible.sync="dialogUserForm" :destroy-on-close="true">
          <el-form :model="user_data">
            <el-form-item label="用户名" :label-width="labelFormWidth">
              <el-input v-model="user_data.base_info.username"></el-input>
            </el-form-item>
            <el-form-item label="姓名" :label-width="labelFormWidth">
              <el-input v-model="user_data.user_info.name"></el-input>
            </el-form-item>
            <el-form-item label="花名" :label-width="labelFormWidth">
              <el-input v-model="user_data.user_info.nickname"></el-input>
            </el-form-item>
            <el-form-item label="职称" :label-width="labelFormWidth">
              <el-input v-model="user_data.user_info.title"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogUserForm = false">取 消</el-button>
            <el-button type="primary" @click="addUser()">确 定</el-button>
          </div>
        </el-dialog>
        <el-dialog title="权限信息" :visible.sync="dialogPowerForm" :destroy-on-close="true">
          <el-form :model="power_data">
            <el-form-item label="权限名称" :label-width="labelFormWidth">
              <el-input v-model="power_data.name"></el-input>
            </el-form-item>
            <el-form-item label="路由地址" :label-width="labelFormWidth">
              <el-input v-model="power_data.path"></el-input>
            </el-form-item>
            <el-form-item label="所属模块" :label-width="labelFormWidth">
              <el-input v-model="power_data.module_name"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogPowerForm = false">取 消</el-button>
            <el-button type="primary" @click="addPower()">确 定</el-button>
          </div>
        </el-dialog>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import axios from "axios";

export default {
  name: "UserManage",
  components: {
    Menu
  },
  data() {
    return {
      activeName: '用户管理',
      user_list: [{
        name: '',
        nickname: '',
        title: '',
        username: '',
      }],
      user_data: {
        base_info: {
          username: '',
        },
        user_info: {
          name: '',
          nickname: '',
          title: '',
        },
      },
      power_data: {
        name: '',
        path: '',
        module_name:'',
      },
      role_list: [{
        name: '',
        des: '',
      }],
      power_list: [{
        name: '',
        module_name: '',
        path: '',
      }],
      labelFormWidth: '100px',
      dialogUserForm: false,
      dialogPowerForm: false,
    }
  },
  methods: {
    handleClick(tab, event) {
    },
    userList() {
      axios({
        url: '/base_user',
        method: 'get',
      }).then(res => {
        this.user_list = res.data
      })
    },
    openNewUser() {
      this.user_data = this.$options.data().user_data
      this.dialogUserForm = true;
    },
    openNewPower() {
      this.power_data = this.$options.data().power_data;
      this.dialogPowerForm = true;
    },
    addUser() {
      axios({
        url: '/base_user',
        method: 'post',
        data: this.user_data,
      }).then(res => {
            this.$message({message: '成功', type: "success"})
            this.user_list = res.data;
            this.dialogUserForm = false;
          }
      )
    },
    deleteUser(id) {
      axios({
        url: '/base_user',
        method: 'post',
        data: {
          is_delete: 1,
          id: id,
        }
      }).then(res => {
        this.user_list = res.data;
        this.$message({message: '成功', type: "success"})
      })
    },
    addPower() {
      axios({
        method: 'post',
        url: '/power_list/',
        data: this.power_data
      }).then(res => {
        this.power_list = res.data;
        this.$message({message: '成功', type: "success"})
        this.dialogPowerForm = false;
      })
    },
    powerList() {
      axios({
        method: 'get',
        url: '/power_list/'
      }).then(res => {
        this.power_list = res.data
      })
    },
  },
  mounted() {
    this.userList();
    this.powerList();
  }
}
</script>

<style scoped>

.el-container {
  height: 100%;
}

</style>