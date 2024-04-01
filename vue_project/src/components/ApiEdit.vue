<template>
  <div>
    <div>
      <el-container style="background-color: #f4f4f4">
        <div style="width: 1200px; margin: auto">
          <el-card>
            <el-header style="text-align: center">
              <span>接口信息</span>
            </el-header>
            <el-main>
              <el-form label-width="100px" label-position="left">
                <el-form-item label="接口名称">
                  <el-input placeholder="请输入" v-model="apiData.label"
                            style="width: 100%"></el-input>
                </el-form-item>
                <el-row>
                  <el-col :span="5">
                    <el-form-item label="登录接口" style="margin-right: 100px">
                      <el-switch v-model="apiData.is_login" active-color="#13ce66"></el-switch>
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item label="第三方接口">
                      <el-switch v-model="apiData.is_other_port"
                                 active-color="#13ce66"></el-switch>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item label="host">
                  <el-select style="width: 10%" v-model="apiData.web_method" clearable>
                    <el-option label="http" value="http"></el-option>
                    <el-option label="https" value="https"></el-option>
                  </el-select>
                  <el-input placeholder="请输入地址端口" style="width: 90%"
                            v-model="apiData.host"></el-input>
                </el-form-item>
                <el-form-item label="路径">
                  <el-select style="width: 10%" v-model="apiData.method"
                             default-first-option>
                    <el-option label="get" value="get"></el-option>
                    <el-option label="post" value="post"></el-option>
                    <el-option label="put" value="put"></el-option>
                    <el-option label="delete" value="delete"></el-option>
                    <el-option label="options" value="options"></el-option>
                  </el-select>
                  <el-input placeholder="请输入" style="width: 90%"
                            v-model="apiData.path"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                  <el-input placeholder="请输入" v-model="apiData.des"
                            style="width: 100%"></el-input>
                </el-form-item>
              </el-form>
              <el-tabs v-model="apiData.activeParams" type="border-card">
                <el-tab-pane label="Params" name="Params">
                  <el-table :data="apiData.params" border size="mini"
                            style="overflow-y: auto"
                            height="460">
                    <el-table-column label="参数名" prop="key">
                      <template slot-scope="scope">
                        <el-input size="small" v-model="scope.row.key"
                                  @change="EditValue(scope.$index, scope.row)"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="参数值" prop="value">
                      <template slot-scope="scope">
                        <el-input size="small" v-model="scope.row.value"
                                  @change="EditValue(scope.$index, scope.row)"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="描述" prop="des">
                      <template slot-scope="scope">
                        <el-input size="small" v-model="scope.row.des"
                                  @change="EditValue(scope.$index, scope.row)"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column align="center" width="250">
                      <template slot="header">
                        <el-button type="text" size="mini"
                                   @click.native.prevent="addRow(apiData.params)">新增
                        </el-button>
                      </template>
                      <template slot-scope="scope">
                        <el-button size="mini" type="text"
                                   @click="insertRow(scope.$index, apiData.params)">插入
                        </el-button>
                        <el-button size="mini" type="text"
                                   @click="moveUp(scope.$index, apiData.params)">上移
                        </el-button>
                        <el-button size="mini" type="text"
                                   @click="moveDown(scope.$index, apiData.params)">下移
                        </el-button>
                        <el-button size="mini" type="text"
                                   @click.native.prevent="deleteRow(scope.$index, apiData.params)">
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-tab-pane>
                <el-tab-pane label="Headers" name="Headers">
                  <el-table :data="apiData.headers" border size="mini"
                            style="overflow-y: auto"
                            height="460">
                    <el-table-column label="参数名" prop="key">
                      <template slot-scope="scope">
                        <el-input size="small" v-model="scope.row.key"
                                  @change="EditValue(scope.$index, scope.row)"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="参数值" prop="value">
                      <template slot-scope="scope">
                        <el-input size="small" v-model="scope.row.value"
                                  @change="EditValue(scope.$index, scope.row)"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="描述" prop="des">
                      <template slot-scope="scope">
                        <el-input size="small" v-model="scope.row.des"
                                  @change="EditValue(scope.$index, scope.row)"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column align="center" width="250">
                      <template slot="header">
                        <el-button size="small" type="text"
                                   @click.native.prevent="addRow(apiData.headers)">新增
                        </el-button>
                      </template>
                      <template slot-scope="scope">
                        <el-button size="mini" type="text"
                                   @click="insertRow(scope.$index, apiData.headers)">插入
                        </el-button>
                        <el-button size="mini" type="text"
                                   @click="moveUp(scope.$index, apiData.headers)">上移
                        </el-button>
                        <el-button size="mini" type="text"
                                   @click="moveDown(scope.$index, apiData.headers)">下移
                        </el-button>
                        <el-button size="small" type="text"
                                   @click.native.prevent="deleteRow(scope.$index, apiData.headers)">
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-tab-pane>
                <el-tab-pane label="Body" name="Body">
                  <el-tabs v-model="apiData.payload_method">
                    <el-tab-pane label="none" name="none">
                      <el-input type="textarea" rows="22" :disabled="true" placeholder="无需参数"
                                class="textarea_disabled"
                                style="text-align: center"></el-input>
                    </el-tab-pane>
                    <el-tab-pane label="form-data" name="form-data">
                      <el-table :data="apiData.payload_fd" border size="mini"
                                style="overflow-y: auto" height="406">
                        <el-table-column label="参数名" prop="key">
                          <template slot-scope="scope">
                            <el-input size="small" v-model="scope.row.key"
                                      @change="EditValue(scope.$index, scope.row)"></el-input>
                          </template>
                        </el-table-column>

                        <el-table-column label="参数值" prop="value">
                          <template slot-scope="scope">
                            <el-input v-if="scope.row.isFile" size="small" v-model="scope.row.value"
                                      @change="EditValue(scope.$index, scope.row)" disabled></el-input>
                            <el-input v-else size="small" v-model="scope.row.value"
                                      @change="EditValue(scope.$index, scope.row)"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column label="描述" prop="des">
                          <template slot-scope="scope">
                            <el-input size="small" v-model="scope.row.des"
                                      @change="EditValue(scope.$index, scope.row)"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column width="300" align="center">
                          <template slot="header">
                            <el-button size="small" type="text"
                                       @click.native.prevent="addPayloadFdRow(apiData.payload_fd)">
                              新增
                            </el-button>
                          </template>
                          <template slot-scope="scope">
                            <el-button size="mini" type="text"
                                       @click="insertFormData(scope.$index, apiData.payload_fd)">
                              插入
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveUp(scope.$index, apiData.payload_fd)">上移
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveDown(scope.$index, apiData.payload_fd)">下移
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click.native.prevent="deleteRow(scope.$index)">
                              删除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="x-www-form-urlencoded" name="x-www-form-urlencoded">
                      <el-table :data="apiData.payload_xwfu" border size="mini"
                                style="overflow-y: auto" height="406">
                        <el-table-column label="参数名" prop="key">
                          <template slot-scope="scope">
                            <el-input size="small" v-model="scope.row.key"
                                      @change="EditValue(scope.$index, scope.row)"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column label="参数值" prop="value">
                          <template slot-scope="scope">
                            <el-input size="small" v-model="scope.row.value"
                                      @change="EditValue(scope.$index, scope.row)"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column label="描述" prop="des">
                          <template slot-scope="scope">
                            <el-input size="small" v-model="scope.row.des"
                                      @change="EditValue(scope.$index, scope.row)"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column align="center" width="250">
                          <template slot="header">
                            <el-button size="small" type="text"
                                       @click.native.prevent="addRow(apiData.payload_xwfu)">
                              新增
                            </el-button>
                          </template>
                          <template slot-scope="scope">
                            <el-button size="mini" type="text"
                                       @click="insertRow(scope.$index, apiData.payload_xwfu)">插入
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveUp(scope.$index, apiData.payload_xwfu)">上移
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveDown(scope.$index,apiData.payload_xwfu)">下移
                            </el-button>
                            <el-button size="small" type="text"
                                       @click.native.prevent="deleteRow(scope.$index, apiData.payload_xwfu)">
                              删除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="raw" name="raw">
                      <el-select v-model="apiData.raw_method" size="mini"
                                 style="width: 100px">
                        <el-option label="Text" value="Text"></el-option>
                        <el-option label="JavaScript" value="JavaScript"></el-option>
                        <el-option label="JSON" value="JSON"></el-option>
                        <el-option label="HTML" value="HTML"></el-option>
                        <el-option label="XML" value="XML"></el-option>
                      </el-select>
                      <el-input type="textarea" rows="21"
                                v-model="apiData.raw_data"></el-input>
                    </el-tab-pane>
                    <el-tab-pane label="binary" name="binary">
                      <div style="height: 406px"></div>
                    </el-tab-pane>
                  </el-tabs>
                </el-tab-pane>
              </el-tabs>
            </el-main>
            <div style="text-align: center;margin-top: 5px">
              <el-button type="primary" @click="saveApi" size="mini">保存</el-button>
              <el-button plain @click="closeWindow" size="mini">关闭</el-button>
            </div>
          </el-card>
        </div>
      </el-container>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ApiEdit",
  data() {
    return {
      id: '',
      apiData: {
        label: '',
        des: '',
        is_login: false,
        is_other_port:
            false,
        path: '',
        method: 'get',
        params: [],
        headers: [],
        activeParams: 'Params',
        payload_method: 'none',
        payload_fd: [],
        payload_xwfu: [],
        raw_method: 'Text',
        raw_data: ''
      }
    }
  },
  mounted() {
    this.id = this.$route.query.id
    if (this.id) {
      this.apiDetail()
    }
  },
  methods: {
    apiDetail() {
      axios({
        method: 'get',
        url: '/api_detail',
        params: {id: this.id},
      }).then(res => {
        this.apiData = res.data.data
      })
    },
    saveApi() {
      let saveData;
      if (this.id) {
        saveData = {
          method: 'post',
          url: '/api_edit',
          params: {id: this.id},
          data: this.apiData
        }
      } else {
        saveData = {
          method: 'post',
          url: '/api_edit',
          data: this.apiData
        }
      }
      axios(saveData).then(res => {
        setTimeout(function() {
          window.close()
        },2000)
        this.$message({message: res.data.message, type: res.data.type, duration: 2000})
      })
    },
    closeWindow() {
      window.close();
    },
    addPayloadFdRow(rows) {
      rows.push({key: '', value: '', isFile: false, abspath: '', file_name: '', des: ''})
    },
    insertFormData(index, row) {
      row.splice(index, 0, {key: '', value: '', isFile: false, abspath: '', file_name: '', des: ''})
    },
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
    addRow(rows) {
      rows.push({key: '', value: '', des: '',})
    },
    insertRow(index, rows) {
      rows.splice(index, 0, {key: '', value: '', des: '',})
    },
    moveUp(index, rows) {
      if (index > 0) {
        const up = rows[index]
        rows.splice(index, 1)
        rows.splice(index - 1, 0, up)
      }
    },
    moveDown(index, rows) {
      if (index < rows.length - 1) {
        const up = rows[index]
        rows.splice(index, 1)
        rows.splice(index + 1, 0, up)
      }
    },
    EditValue(index, row) {
    },
  }
}
</script>

<style scoped>
.el-header {
  height: 30px !important;
  padding: 8px;
  font-weight: bold;
  line-height: 20px;
  text-align: center;
  font-size: 18px;
}
.el-main{
  padding: 10px 10px;
}

.el-footer {
  text-align: center;
  line-height: 50px;
  height: 50px !important;
}

.el-form-item {
  margin-bottom: 10px;
}

</style>