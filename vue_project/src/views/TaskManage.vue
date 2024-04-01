<template>
  <div>
    <div style="line-height: 50px; float: right">
      <el-form @submit.native.prevent>
        <el-input placeholder="请输入任务名称" style="width: 300px" v-model="queryFields.name">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-button type="primary" @click="taskList" native-type="submit">查询</el-button>
        <el-button type="primary" @click="clickAddTask">新增任务</el-button>
      </el-form>
    </div>
    <el-table :data="TaskData" border style="width: 100%" :highlight-current-row="true" height="750">
      <el-table-column label="序号" type='index' prop="index" align="center" width="70"></el-table-column>
      <el-table-column label="任务名称" prop="name" width="300"></el-table-column>
      <el-table-column label="所属项目" prop="project_name" width="300"></el-table-column>
      <el-table-column label="协议类型" prop="web_type" width="100"></el-table-column>
      <el-table-column label="环境地址" prop="host" width="180"></el-table-column>
      <el-table-column label="计划运行时间" prop="next_time" width="160" align="center"></el-table-column>
      <el-table-column label="说明" prop="des"></el-table-column>
      <el-table-column label="运行状态" prop="is_running" width="100">
        <template slot-scope="scope">
          <span :style="{color: statusColor(scope.row.status)}">{{ scope.row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="启用状态" width="100" align="center">
        <template slot-scope="scope">
          <el-switch active-color="#13ce66" v-model="scope.row.task_status"
                     @change="changeTaskStatus(scope.row.id, scope.row.task_status)"></el-switch>
        </template>
      </el-table-column>
      <el-table-column width="200" align="center">
        <template slot-scope="scope">
          <el-button type="text" size="mini" @click="goEditTask(scope.row.id)">编辑</el-button>
          <el-button v-if="scope.row.task_status" size="mini" type="text" @click="runTask(scope.row.id)">运行
          </el-button>
          <el-button size="mini" type="text" @click="deleteTask(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15]"
        :page-size="this.queryFields.PageSize"
        layout="total, prev, pager, next, jumper, sizes"
        @current-change="taskList"
        :total="count">
    </el-pagination>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "TaskManage",
  data() {
    return {
      count: 0,
      queryFields: {
        name: '',
        Page: 1,
        PageSize: 15,
        version_id: this.$route.query.version_id,
        project_id: this.$route.query.project_id
      },
      TaskData: [],
      task_id: '',
    }
  },
  mounted() {
    this.taskList();
  },
  methods: {
    deleteTask(id) {
      axios({
        url: '/task_delete',
        params: {id: id}
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type, duration: 2000})
        this.taskList()
      })
    },
    changeTaskStatus(id, status) {
      axios({
        method: 'post',
        url: '/save_task',
        data: {id: id, task_status: status}
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type, duration: 2000})
        this.taskList()
      })
    },
    goEditTask(id) {
      let routeUrl = this.$router.resolve({
        path: '/task_form',
        query: {version_id: this.$route.query.version_id, project_id: this.$route.query.project_id, task_id: id}
      })
      window.open(routeUrl.href, '_blank')
    },
    clickAddTask() {
      let routeUrl = this.$router.resolve({
        path: '/task_form',
        query: {version_id: this.$route.query.version_id, project_id: this.$route.query.project_id}
      })
      window.open(routeUrl.href, '_blank')
    },
    runTask(task_id) {
      axios({
        url: '/run_task',
        method: 'get',
        params: {id: task_id}
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.taskList()
      })
    },
    statusColor(text) {
      if (text === '运行') {
        return '#F56C6C'
      } else {
        return '#67C23A'
      }
    },
    taskList() {
      axios({
        url: '/task_list',
        method: 'get',
        params: this.queryFields
      }).then(res => {
        this.TaskData = res.data.data
        this.count = res.data.count
      })
    },
  }
}
</script>

<style scoped>
.el-table * {
  font-size: 14px !important;
}

</style>