<template>
  <div class="home" style="height:100%">
    <el-container style="height:100%">
      <el-aside style="width: 210px;height: 100%;overflow-x: hidden">
        <Menu></Menu>
      </el-aside>
      <el-container>
        <el-header style="padding: 10px 10px">
          <el-row :gutter="5">
            <el-col :span="6">
              <div class="top_data" style="background-color: #249730">
                <div class="top_name">
                  <p>官方接口：{{ real_time_info.api_total_nums }}</p>
                  <el-tag size="mini" style="color: #249730">实时</el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="top_data" style="background-color: #a8994c">
                <div class="top_name">
                  <p>未读消息：{{ real_time_info.no_read_message_nums }}</p>
                  <el-tag size="mini" style="color: #a8994c">实时</el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="top_data" style="background-color: #383ea8">
                <div class="top_name">
                  <p>用例执行次数：{{ real_time_info.run_case_times }}</p>
                  <el-tag size="mini" style="color: #383ea8">实时</el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="top_data" style="background-color: #53a8a4">
                <div class="top_name">
                  <p>导入接口次数：{{ real_time_info.import_api_times }}</p>
                  <el-tag size="mini" style="color: #53a8a4">实时</el-tag>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-header>
        <el-main style="padding: 5px 10px">
          <div>
            <div>
              <el-card class="box-card" style="width: 20%; margin-right: 1px;float: left">
                <div slot="header" class="clearfix">
                  <span>统计信息</span>
                  <el-button style="float: right; padding: 3px 0" type="text">查看详情</el-button>
                </div>
                <div style="margin-bottom: 10%">项目总数: {{ tj_data.project_overflow.project_num }}</div>
                <div style="margin-bottom: 10%">用例总数: {{ tj_data.project_overflow.case_num }}</div>
                <div style="margin-bottom: 6px">接口总数: {{ tj_data.project_overflow.api_num }}</div>
              </el-card>
              <el-card class="box-card" style="width: calc(80% - 5px);float: left">
                <div slot="header" class="clearfix">
                  <span>上次用例执行情况</span>
                  <el-button style="float: right; padding: 3px 0" type="text">查看详情</el-button>
                </div>
                <div>接口通过率</div>
                <el-progress :text-inside="true" :stroke-width="14" :percentage="tj_data.last_run_info.api_pass_percent"
                             status="success" style="margin-bottom: 10px"></el-progress>
                <div>用例成功率</div>
                <el-progress :text-inside="true" :stroke-width="14"
                             :percentage="tj_data.last_run_info.case_pass_percent"
                             status="warning" style="margin-bottom: 10px"></el-progress>
                <div>用例失败率</div>
                <el-progress :text-inside="true" :stroke-width="14"
                             :percentage="tj_data.last_run_info.case_fail_percent"
                             status="exception"></el-progress>
              </el-card>
            </div>
            <div>
              <el-card class="box-card" style="float: left;margin-top: 1px;width: 60%">
                <div slot="header" class="clearfix">
                  <span>个人贡献</span>
                  <el-button style="float: right; padding: 3px 0" type="text">查看详情</el-button>
                </div>
                <table class="table_process">
                  <thead class="header">
                  <tr>
                    <th>项目占比</th>
                    <th>接口占比</th>
                    <th>用例占比</th>
                    <th>监控占比</th>
                  </tr>
                  </thead>
                  <tbody class="table_data">
                  <tr>
                    <td>
                      <el-progress type="circle"
                                   :percentage="tj_data.person_contribution.project_percent"></el-progress>
                    </td>
                    <td>
                      <el-progress type="circle" :percentage="tj_data.person_contribution.api_percent"
                                   status="success"></el-progress>
                    </td>
                    <td>
                      <el-progress type="circle" :percentage="tj_data.person_contribution.case_percent"
                                   status="exception"></el-progress>
                    </td>
                    <td>
                      <el-progress type="circle"
                                   :percentage="tj_data.person_contribution.monitor_percent"></el-progress>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </el-card>
              <el-card class="box-card" style="width: calc(40% - 5px); margin-top: 1px;float: left">
                <div slot="header" class="clearfix">
                  <span>待处理消息</span>
                  <el-button style="float: right; padding: 3px 0" type="text">查看详情</el-button>
                </div>
                <div class="message">
                  <div v-for="o in 5" :key="o" style="text-align: left; margin: 10px">
                    {{ '消息 ' + o }}
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-main>
        <el-footer
            style="height: 150px; background: linear-gradient(to right, white, #B7CAD8, #5E7DB3); padding: 0 10px">
          <el-card class="box-card"
                   style="width: calc(100% - 15px);height: 120px;background: linear-gradient(to right, white, #B7CAD8, #5E7DB3); overflow: auto">
            <div v-for="o in tj_data.notice_info" :key="o" style="text-align: left; margin: 5px">
              {{ '[公告 '+o.create_date+']：' + o.content }}
            </div>
          </el-card>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
// @ is an alias to /src
import Menu from "@/components/Menu.vue";
import axios from "axios";

export default {
  name: 'home',
  components: {
    Menu
  },
  data() {
    return {
      tj_data: {
        project_overflow: {
          project_num: 0,
          case_num: 0,
          api_num: 0
        },
        person_contribution: {
          project_percent: 0,
          api_percent: 0,
          case_percent: 0,
          monitor_percent: 0
        },
        last_run_info: {
          api_pass_percent: 0,
          case_pass_percent: 0,
          case_fail_percent: 0
        },
        notice_info: [{
          content: '',
          create_date: '',
        }]
      },
      real_time_info: {
        api_total_nums: 0,
        no_read_message_nums: 0,
        run_case_times: 0,
        import_api_times: 0
      }
    };
  },
  mounted() {
    axios.get('/static_data').then(
        res => {
          this.tj_data = res.data
        });
    axios.get('/realtime_data/').then(
        res => {
          this.real_time_info = res.data
        });
  },
}
</script>
<style>
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

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both
}

.box-card {
  height: 270px;
}

.el-card div {
  font-size: x-small;
}

.el-card span {
  font-size: large;
}

th, td {
  text-align: center;
  width: 15%;
}

.top_data {
  color: white;
  height: 50px;
  border-radius: 4px;
}

.top_name {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

p {
  font-size: 13px;
  font-weight: bolder;
}
</style>
