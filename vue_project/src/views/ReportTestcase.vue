<template>
  <div>
    <el-container style="height:100%">
      <el-header style="height: 205px;padding: 0 5px 0 5px">
        <el-card style="height: 200px">
          <el-row>
            <el-col :span="5">
              <div style="margin-top: 30px">
                <el-statistic :title="'用例总数'" :value="caseTotal"></el-statistic>
              </div>
            </el-col>

            <el-col :span="7">
              <div id="static_case" style="height: 200px;line-height: 100px"></div>
            </el-col>
            <el-col :span="12">
              <div id="static_user" style="height: 200px;line-height: 100px"></div>
            </el-col>

          </el-row>
        </el-card>
      </el-header>
      <el-main style="padding: 0 5px 0 5px">
        <el-card style="padding: 5px 0 20px 20px" id="test">
          <el-form :data="queryFields" style="width: 100%">
            <el-row>
              <el-col :span="6">
                <el-form-item label="用例名称">
                  <el-input v-model="queryFields.caseName" style="width: 70%"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="责任人">
                  <el-select
                      style="width: 300px"
                      filterable
                      placeholder="请选择责任人"
                      v-model="queryFields.user">
                    <el-option
                        v-for="item in user_options"
                        :label="item.name"
                        :value="item.user"
                        :key="item.user">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="用例状态">
                  <el-select v-model="queryFields.caseStatus" style="width: 70%">
                    <el-option :value="''" :label="'请选择'"></el-option>
                    <el-option :value="'失败'" :label="'失败'"></el-option>
                    <el-option :value="'成功'" :label="'成功'"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <div style="float: right">
                <el-button @click="resetQuery">重置</el-button>
                <el-button type="primary" @click="ReportTestcaseList">查询</el-button>
              </div>
            </el-row>
          </el-form>
          <el-table :data="ReportList" border style="width: 100%" :highlight-current-row="true" height="550px">
            <el-table-column type="index" label="序号" width="100"></el-table-column>
            <el-table-column label="用例名称" prop="case_name"></el-table-column>
            <el-table-column label="所属模块" prop="module" width="200"></el-table-column>
            <el-table-column label="责任人" prop="username" width="150"></el-table-column>
            <el-table-column label="用例状态" prop="result" width="150">
              <template slot-scope="scope">
                <div v-if="scope.row.result" style="color: #67C23A">成功</div>
                <div v-else style="color: #F56C6C">失败</div>
              </template>
            </el-table-column>
            <el-table-column label="执行时间" prop="create_time" width="300"></el-table-column>
            <el-table-column width="100" align="center" label="操作">
              <template slot-scope="scope">
                <el-button type="text" @click="ViewTestcase(scope.row.id)">查看</el-button>
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
              :total="queryCaseTotal">
          </el-pagination>
        </el-card>
      </el-main>
    </el-container>
    <el-dialog :visible.sync="dialogTableVisible" fullscreen :title="'测试用例：'+ caseName" center>
      <ReportCaseView :reportData="TestcaseDetail"></ReportCaseView>
      <span slot="footer">
        <el-button type="primary" @click="dialogTableVisible=false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from 'echarts'
import ReportCaseView from "@/components/ReportCaseView.vue";


export default {
  name: "ReportTestcase",
  components: {ReportCaseView},
  data() {
    return {
      user_options:[],
      report_id: '',
      option: {
        title: {
          text: '0%',
          left: 'center',
          top: 'center',
        },
        tooltip: {
          formatter: '{c} {b} ({d}%)',
          textStyle: {
            fontSize: 10,
          }
        },
        series: [
          {
            type: 'pie',
            radius: ['40%', '70%'],
            data: [
              {value: 0, name: '成功用例'},
              {value: 0, name: '失败用例'},
            ],
            color: ['#67C23A', '#F56C6C'],
            labelLine: {
              show: false,
              fontSize: 5,
              positions: 'center'
            },
            label: {
              show: false
            },
          },
        ]

      },
      userOption: {
        title: {
          text: '用例人员分布图',
          left: 'center',
        },
        xAxis: {
          data: []
        },
        yAxis: {},
        dataZoom: {
          type: 'inside',
          start: 0,
          show: true
        },
        series: [
          {
            name: '成功',
            type: 'bar',
            data: [],
            barWidth: '30%',
            color: ['#67C23A'],
          },
          {
            name: '失败',
            type: 'bar',
            data: [],
            barWidth: '30%',
            color: ['#F56C6C'],
          },
        ],
        tooltip: {
          formatter: '{a}:{c}',
          textStyle: {
            fontSize: 10,
          }
        },

      },
      caseTotal: 0,
      queryCaseTotal: 0,
      queryFields: {caseName: '', user: '', caseStatus: '', page: 1, pageSize: 15,},
      dialogTableVisible: false,
      caseName: '',
      TestcaseDetail: {},
      ReportList: [{case_name: 'test'}],
    }
  },
  mounted() {
    this.userList()
    this.report_id = this.$route.query.report_id
    this.ReportTestcaseList()
  },
  methods: {
    staticCaseData() {
      axios({
        method: 'get',
        url: 'report_testcase_static',
        params: {report_id: this.report_id}
      }).then(res => {
        this.option.series[0].data = res.data.data.static_num
        this.option.title.text = res.data.data.pass_percent
        this.userOption.xAxis.data = res.data.data.usernames
        this.userOption.series[0].data = res.data.data.pass_num
        this.userOption.series[1].data = res.data.data.fail_num
        this.caseTotal = res.data.data.case_count
        this.staticCaseEcharts()
        this.staticUser()
      })
    },
    staticCaseEcharts() {
      const chartDom = document.getElementById('static_case');
      const myChart = echarts.init(chartDom);
      myChart.setOption(this.option)
    },
    staticUser() {
      const chartDom = document.getElementById('static_user');
      const myChart = echarts.init(chartDom);
      myChart.setOption(this.userOption)
    },
    handleCurrentChange(page) {
      this.queryFields.page = page
      this.ReportTestcaseList()
    },
    resetQuery() {
      this.queryFields.caseName = ''
      this.queryFields.user = ''
      this.queryFields.caseStatus = ''
    },
    statusColor(status) {
      return status ? '#67C23A' : '#F56C6C'
    },
    userList() {
      axios({
        url: '/base_user',
        method: 'get',
      }).then(res => {
        this.user_options = res.data
      })
    },
    ReportTestcaseList() {
      axios({
        url: '/report_testcase',
        params: {
          report_id: this.$route.query.report_id,
          caseName: this.queryFields.caseName,
          caseStatus: this.queryFields.caseStatus,
          user: this.queryFields.user,
          page: this.queryFields.page,
          pagesize: this.queryFields.pageSize,
        },
        method: 'get'
      }).then(res => {
        this.ReportList = res.data.data
        this.queryCaseTotal = res.data.total
      })
      this.staticCaseData()
    },
    ViewTestcase(id) {
      axios({
        method: "get",
        url: '/report_detail',
        params: {id: id}
      }).then(res => {
        this.TestcaseDetail = res.data.data;
        this.caseName = res.data.case_name;
        this.dialogTableVisible = true
      })
    },
  }
}
</script>

<style scoped>
.el-header .el-main {
  text-align: center;
  line-height: 100px;
}

.el-main {
  padding: 0 0;
}

.el-table /deep/ * {
  font-size: 14px !important;
}

.el-card /deep/ .el-card__body {
  padding: 5px 0 0 0 !important;
}
</style>