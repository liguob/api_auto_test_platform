<template>
  <div>
    <el-collapse class="collapse" v-if="reportData.data.length>0" style="width: 100%">
      <el-collapse-item v-for="item in reportData.data" style="width: 100%">
        <template slot="title">
          <div :style="item.result?'color: #67C23A':'color: #F56C6C'">
            <span style="width: 80px;float: left;text-align: left">状态码：{{ item.status_code }}</span>
            <span style="width: 100px;float: left;margin-left: 20px">耗时：{{ item.request_time }}ms</span>
            <span style="margin-left: 20px">{{ item.name }}</span>
          </div>
        </template>
        <div style="margin-left: 10px">
          <h5>URL</h5>
          <el-input disabled type="textarea" v-model="item.url" rows="1" class="area"
                    :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
          <el-collapse class="collapse">
            <el-collapse-item>
              <template slot="title"><h5>请求headers</h5></template>
              <el-input disabled type="textarea" v-model="item.Request_headers" class="area"
                        :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
            </el-collapse-item>
            <el-collapse-item>
              <template slot="title"><h5>请求body</h5></template>
              <el-input disabled type="textarea" v-model="item.Request_body" class="area"
                        :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
            </el-collapse-item>
            <el-collapse-item>
              <template slot="title"><h5>响应headers</h5></template>
              <el-input disabled type="textarea" v-model="item.Response_headers" class="area"
                        :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
            </el-collapse-item>
            <el-collapse-item>
              <template slot="title"><h5>响应body</h5></template>
              <el-input disabled type="textarea" v-model="item.Response_body" class="area"
                        :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
            </el-collapse-item>
            <el-collapse-item v-if="item.setConfig.length>0">
              <template slot="title"><h5>配置结果</h5></template>
              <el-collapse style="margin-left: 10px" class="collapse">
                <el-collapse-item v-for="i in item.setConfig">
                  <template slot="title">
                    <h5 :style="i.result?'color: #67C23A':'color: #F56C6C'">{{ i.name }}</h5>
                  </template>
                  <el-input disabled type="textarea" v-model="i.info" class="area"
                            :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
                </el-collapse-item>
              </el-collapse>
            </el-collapse-item>
          </el-collapse>
        </div>
      </el-collapse-item>
      <el-collapse-item v-if="reportData.params">
        <template slot="title">
          <h3 style="color: #409EFF">用例参数</h3>
        </template>
        <el-input disabled type="textarea" v-model="reportData.params" class="area"
                  :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
      </el-collapse-item>
    </el-collapse>
    <el-empty v-else description="无报告数据，请确认运行接口是否存在或禁用"></el-empty>
    <el-collapse class="collapse" v-if="reportData.error_info !== ''">
      <el-collapse-item>
        <template slot="title">
          <h3 style="color: #F56C6C">错误信息</h3>
        </template>
        <div>
          <el-input disabled type="textarea" v-model="reportData.error_info" rows="1" class="area"
                    :autosize="{ minRows: 1, maxRows: 100}" resize="none"></el-input>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
export default {
  name: "ReportCaseView",
  props: ['reportData'],
}
</script>

<style scoped>

h5 {
  margin: 0 5px 5px 0;
}

.area /deep/ .el-textarea__inner {
  font-size: 10px;
  color: #606266 !important;
  cursor: auto !important;
}

.collapse /deep/ .el-collapse-item__content {
  padding-bottom: 0 !important;
}


</style>