<template>
  <div>
    <el-table :data="reportList" border style="width: 100%" :highlight-current-row="true">
      <el-table-column label="用例名称" prop="case_name"></el-table-column>
      <el-table-column prop="result" label="用例状态">
        <template slot-scope="scope">
          <span v-if="scope.row.result" style="color: #67C23A">成功</span>
          <span v-else style="color: #F56C6C">失败</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="create_time"></el-table-column>
      <el-table-column>
        <template slot="header">
          <el-button type="primary" size="mini" @click="report_list">刷新</el-button>
          <el-button type="danger" size="mini" @click="clearReport">清空报告</el-button>
        </template>
        <template slot-scope="scope">
          <el-button @click="report_detail(scope.row.id)" type="primary" size="mini">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogTableVisible" fullscreen :title="'测试用例：'+caseName" center>
      <ReportCaseView :reportData="reportData"></ReportCaseView>
      <span slot="footer">
        <el-button type="primary" @click="dialogTableVisible=false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import ReportCaseView from "@/components/ReportCaseView.vue";

export default {
  name: "DebugReportCaseList",
  components: {ReportCaseView},
  mounted() {
    this.report_list()
  },
  data() {
    return {
      caseName:'',
      dialogTableVisible:false,
      reportList: [
        {case_name: '1', result: false, create_time: 1}
      ],
      reportData: [],
    }
  },
  methods: {
    clearReport(){
      axios({
        url:'/clear_report',
        method:"get",
        params:{case_id: this.$route.query.case_id}
      }).then(res=>{
        this.reportList = res.data.data
        this.$message.success('成功')
      })
    },
    report_list() {
      axios({
        url: '/debug_report',
        method: "get",
        params: {case_id: this.$route.query.case_id}
      }).then(res => {
        this.reportList = res.data.data
      })
    },
    report_detail(id) {
      axios({
        url: '/debug_report_detail',
        method: "get",
        params: {id: id}
      }).then(res => {
        this.caseName = res.data.case_name
        this.reportData = res.data.data
        this.dialogTableVisible = true
      })
    }
  }
}
</script>

<style scoped>

</style>