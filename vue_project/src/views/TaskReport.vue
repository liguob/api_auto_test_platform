<template>
  <div>
    <el-container>
      <el-container style="border-left: 1px black">
        <el-main style="padding: 5px 10px">
          <div>
            <template>
              <el-table :data="reportData" border style="width: 100%" :highlight-current-row="true" height="800px">
                <el-table-column type="index" label="序号" width="100"></el-table-column>
                <el-table-column label="协议类型" prop="web_type" width="300"></el-table-column>
                <el-table-column label="host" prop="host"></el-table-column>
                <el-table-column label="状态" prop="status" width="250">
                  <template slot-scope="scope">
                    <span :style="{color: statusColor(scope.row.status)}">{{ scope.row.status }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="create_time"></el-table-column>
                <el-table-column width="200" align="center" label="操作">
                  <template slot-scope="scope">
                    <router-link :to="'/report_testcase?report_id='+ scope.row.id" target="_blank"
                                 style="text-decoration-line: none;">
                      <el-button type="text" size="mini">查看</el-button>
                    </router-link>
                  </template>
                </el-table-column>
              </el-table>
              <el-pagination
              style="float: right"
              background
              :page-sizes="[15]"
              :page-size="this.queryFields.pageSize"
              layout="total, prev, pager, next, jumper, sizes"
              @current-change="handleCurrentChange"
              :total="total">
          </el-pagination>
            </template>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "TaskReport",
  mounted() {
    this.reportList()
  },
  data() {
    return {
      reportData: [],
      task_id:'',
      queryFields:{task_id:'',Page:1,PageSize:15},
      total:0,
    }
  },
  methods: {
    handleCurrentChange(page) {
      this.queryFields.Page = page
      this.reportList()
    },
    statusColor(status) {
      return status==='成功' ? '#67C23A' : '#F56C6C'
    },
    reportList() {
      if (this.queryFields.task_id === ''){
        this.queryFields.task_id= this.$route.query.task_id
      }
      axios({
        method: 'get',
        url: '/report_task',
        params: this.queryFields,
      }).then(res => {
        this.reportData = res.data.data
        this.total = res.data.total
      })
    },

  }
}
</script>

<style scoped>
.el-form-item {
  margin-bottom: 5px;
}
</style>