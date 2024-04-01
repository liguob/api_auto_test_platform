<template>
  <div class="project_list" style="height: 100%">
    <div style="line-height: 50px;float: right">
      <el-form @submit.native.prevent>
        <el-input placeholder="请输入项目名称" v-model="queryFields.project_name" style="width: 300px">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-button type="primary" @click="projectList()" native-type="submit">查询</el-button>
        <el-button type="primary" @click="open_new_project()">新增项目</el-button>
      </el-form>
    </div>
    <el-table :data="project_list" border style="width: 100%" :highlight-current-row="true" height="750">
      <el-table-column type="index" label="序号" prop="index" width="70" align="center"></el-table-column>
      <el-table-column prop="project_name" label="项目名称" width="300"></el-table-column>
      <el-table-column prop="create_name" label="责任人" width="150" align="center"></el-table-column>
      <el-table-column prop="description" label="描述"></el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="200" align="center"></el-table-column>
      <el-table-column fixed="right" label="操作" width="100" align="center">
        <template slot-scope="scope">
          <el-button type="text" size="mini" @click="clickEdit(scope.row.project_id)">编辑</el-button>
          <el-button type="text" size="mini" @click="clickDelete(scope.row.project_id)"
                     style="margin-left: 5px">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15]"
        :page-size="15"
        layout="total, prev, pager, next, jumper, sizes"
        @current-change="projectList"
        :total="count">
    </el-pagination>
    <el-dialog title="项目信息" :visible.sync="dialogFormVisible" :destroy-on-close="true">
      <el-form :model="project_data" label-width="80px">
        <el-form-item label="项目名称">
          <el-input v-model="project_data.project_name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="责任人">
          <el-select
              style="width: 100%"
              filterable
              placeholder="请选择责任人"
              v-model="project_data.user_id">
            <el-option
                v-for="item in user_options"
                :label="item.name"
                :value="item.user"
                :key="item.user">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目描述">
          <el-input v-model="project_data.description" type="textarea" :rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="projectEdit();dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
        title="提示"
        :visible.sync="dialogConfirmVisible"
        width="30%">
      <span>是否删除项目？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogConfirmVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteProject">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import axios from "axios";
import HeadName from "@/components/HeadName.vue";

export default {
  name: "Project_main",
  components: {
    Menu,
    HeadName,
  },
  data() {
    return {
      dialogConfirmVisible: false,
      queryFields: {project_name: '', Page: 1, PageSize: 15},
      count: 0,
      user_options: [],
      project_list: [],
      activeName: 'first',
      dialogFormVisible: false,
      deleteProjectId: null,
      project_data: {
        project_name: '',
        user_id: null,
        description: '',
      }
    };
  },
  methods: {
    clickDelete(id) {
      this.deleteProjectId = id
      this.dialogConfirmVisible = true
    },
    deleteProject() {
      axios({
        method: 'post',
        url: '/project_delete',
        data: {
          project_id: this.deleteProjectId,
        }
      }).then(res => {
        this.$message({message: '成功', type: 'success'})
        this.projectList()
        this.dialogConfirmVisible = false
      });
    },
    projectDetail(project_id) {
      axios({
        method: 'get',
        url: '/project_detail',
        params: {
          project_id: project_id
        }
      }).then(res => {
        this.project_data = res.data;
      })
    },
    userList() {
      axios({
        url: '/base_user',
        method: 'get',
      }).then(res => {
        this.user_options = res.data
      })
    },
    projectList() {
      axios.get('/project_list/', {
        params: this.queryFields
      }).then(
          res => {
            this.project_list = res.data.data;
            this.count = res.data.count
          })
    },
    clickEdit(project_id) {
      this.projectDetail(project_id)
      this.dialogFormVisible = true
    },
    projectEdit() {
      axios({
        method: 'post',
        url: '/project_edit/',
        data: this.project_data
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.projectList()
      });
    },
    open_new_project() {
      this.project_data = this.$options.data().project_data;
      this.dialogFormVisible = true;
    },
  },
  mounted() {
    this.projectList();
    this.userList();
  }
}
</script>

<style scoped>
.el-header {
  background-color: white;
  color: #333;
}

.el-aside {
  background-color: white;
  color: #333;
}

.el-main {
  background-color: white;
  color: #333;
}

.project_table el-table-column {
  align-items: center;
}

.search .el-input {
  width: 250px;
  margin-right: 5px;
  margin-bottom: 5px;
}

.el-table * {
  font-size: 14px !important;
}
</style>