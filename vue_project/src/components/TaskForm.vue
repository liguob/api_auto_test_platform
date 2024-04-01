<template>
  <div>
    <el-container>
      <el-header>
        <h2>任务信息</h2>
      </el-header>
      <el-main>
        <el-form label-width="100px" :model="data">
          <el-form-item label="任务名称">
            <el-input v-model="data.name"></el-input>
          </el-form-item>
          <el-form-item label="所属项目">
            <el-select
                disabled
                style="width: 100%"
                filterable
                placeholder="请选择项目"
                v-model="data.project_id">
              <el-option
                  v-for="item in project_options"
                  :label="item.project_name"
                  :value="item.project_id"
                  :key="item.project_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属版本">
            <el-select
                disabled
                style="width: 100%"
                filterable
                placeholder="请选择项目版本"
                v-model="data.version_id">
              <el-option
                  v-for="item in version_options"
                  :label="item.version_name"
                  :value="item.id"
                  :key="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="host">
            <el-select style="width: 10%" default-first-option v-model="data.web_type">
              <el-option label="http" value="http"></el-option>
              <el-option label="https" value="https"></el-option>
            </el-select>
            <el-input placeholder="请输入host，例如地址:端口" style="width: 90%" v-model="data.host"></el-input>
          </el-form-item>
          <el-form-item label="运行前置用例">
            <el-switch active-color="#13ce66" v-model="data.is_run_before"></el-switch>
          </el-form-item>
          <el-form-item label="运行基本用例">
            <el-switch active-color="#13ce66" v-model="data.is_run_case"></el-switch>
          </el-form-item>
          <el-form-item label="日程表">
            <el-input type="textarea" rows="5" v-model="data.jenkins_plan" @change="calTime"></el-input>
            <span v-if="message === '成功'" style="color: #67C23A;font-weight: bold">预计下次运行时间：{{
                plan_next_time
              }}</span>
            <span v-else-if=" message === '警告'"
                  style="color: #F56C6C;font-weight: bold">非法输入，请检查语法格式</span>
            <span v-else style="color: #c4a000;font-weight: bold">没有计划任务</span>
          </el-form-item>
          <el-form-item label="任务描述">
            <el-input type="textarea" rows="5" v-model="data.des"></el-input>
          </el-form-item>
        </el-form>
      </el-main>
      <el-footer style="padding: 0 10px">
        <el-button type="primary" @click="saveTask">保存</el-button>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TaskForm",
  data() {
    return {
      plan_next_time: '',
      message: '',
      task_id: '',
      project_options: [],
      version_options: [],
      data: {
        name: '',
        project_id: Number(this.$route.query.project_id),
        version_id: Number(this.$route.query.version_id),
        web_type: 'http',
        host: '',
        jenkins_plan: '',
        is_run_before: false,
        is_run_case: true,
        des: ''
      }
    }
  },
  mounted() {
    axios({
      url: '/project_option',
      method: "get"
    }).then(res => {
      this.project_options = res.data.data;
    })
    axios({
      method: 'get',
      url: '/version_options',
      params: {project_id: this.$route.query.project_id}
    }).then(res => {
      this.version_options = res.data.data
    })
    this.task_id = this.$route.query.task_id
    if (this.task_id) {
      axios({
        url: '/task_detail',
        method: 'get',
        params: {task_id: this.task_id}
      }).then(res => {
        this.data = res.data.data
        if (this.data.jenkins_plan) {
          this.calTime()
        }
      })
    }
  },
  methods: {
    calTime() {
      let post_data = new URLSearchParams();
      post_data.append('jenkins_plan', this.data.jenkins_plan)
      axios({
        method: 'post',
        url: '/get_jenkins_time',
        data: post_data,
      }).then(res => {
        this.message = res.data.message;
        this.plan_next_time = res.data.data;
      })
    },
    saveTask() {
      if (this.data.is_run_case || this.data.is_run_before) {
        axios({
          url: '/save_task',
          method: 'post',
          data: this.data
        }).then(res => {
          if (res.data.message === '成功') {
            this.$message({message: res.data.message, type: res.data.type})
            setTimeout(() => {
              window.close()
            }, 2000)
          } else {
            this.$message({message: res.data.message, type: res.data.type})
          }
        })
      } else {
        this.$message.warning('前置用例，基本用例至少有一个运行')
      }
    }
  }
}
</script>

<style scoped>
.el-header, .el-footer {
  text-align: center;
}

.el-container {
  height: 100%;
}
</style>