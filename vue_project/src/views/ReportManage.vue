<template>
  <div>
    <div style="line-height: 50px; float: right">
      <el-form @submit.n.native.prevent>
        <el-input placeholder="请输入任务名称" style="width: 300px" v-model="queryFields.host">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-button type="primary" @click="reportList" style="margin-right: 10px" native-type="submit">查询</el-button>
      </el-form>
    </div>
    <el-table :data="reportListData" border style="width: 100%" :highlight-current-row="true" size="size" stripe
              height="750">
      <el-table-column label="序号" prop="index" type="index" align="center" width="80"></el-table-column>
      <el-table-column label="协议类型" prop="web_type" width="150"></el-table-column>
      <el-table-column label="环境地址" prop="host"></el-table-column>
      <el-table-column label="任务状态" prop="is_running" width="100">
        <template slot-scope="scope">
          <span :style="{color: statusColor(scope.row.status)}">{{ scope.row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="create_time"></el-table-column>
      <el-table-column label="结束时间" prop="edit_time"></el-table-column>
      <el-table-column align="center" label="操作" width="120">
        <template slot-scope="scope">
          <router-link :to="'/report_testcase?report_id='+scope.row.id" target="_blank"
                       style="text-decoration-line: none; color: #409EFF">
            <el-button type="text" size="mini">查看</el-button>
          </router-link>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15,30,50]"
        :page-size="this.queryFields.PageSize"
        layout="total, prev, pager, next, jumper, sizes"
        @size-change="changeSize"
        @current-change="reportList"
        :total="count">
    </el-pagination>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReportManage",
  mounted() {
    this.reportList()
  },
  data() {
    return {
      queryFields: {
        PageSize: 15,
        Page: 1,
        task_name: '',
        project_id: this.$route.query.project_id,
        version_id: this.$route.query.version_id
      },
      count: 0,
      reportListData: []
    }
  },
  methods: {
    statusColor(text) {
      if (text === '成功') {
        return '#67C23A'
      } else {
        return '#F56C6C'
      }
    },
    changeSize(val) {
      this.queryFields.PageSize = val
      this.reportList()
    },
    reportList() {
      axios({
        method: 'get',
        url: '/report_task',
        params: this.queryFields
      }).then(res => {
        this.reportListData = res.data.data
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