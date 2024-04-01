<template>
  <div>
    <el-container>
      <el-main style="padding: 0 10px">
        <el-tabs type="card" id="main_card">
          <el-tab-pane label="详细信息" class="detail_info">
            <el-card id="api_detail" style="float: right; width:calc(100% - 405px)">
              <div>
                <div v-if="apiSet">
                  <div style="margin-bottom: 5px">
                    <el-button-group>
                      <el-button type="primary" size="mini" @click="copyApi">复制</el-button>
                    </el-button-group>
                  </div>
                  <el-form label-width="100px" label-position="left" :model="caseData.api_data[apiIndex]">
                    <el-form-item label="接口名称" prop="label">
                      <el-input placeholder="请输入" v-model="caseData.api_data[apiIndex].label"
                                style="width: 100%"></el-input>
                    </el-form-item>
                    <el-row>
                      <el-col :span="4">
                        <el-form-item label="登录接口" style="margin-right: 100px">
                          <el-switch v-model="caseData.api_data[apiIndex].is_login" active-color="#13ce66"></el-switch>
                        </el-form-item>
                      </el-col>
                      <el-col :span="5">
                        <el-form-item label="登录cookie">
                          <el-input placeholder="请输入cookie参数名称" style="width: 90%"
                                    v-model="caseData.api_data[apiIndex].session_name"></el-input>
                        </el-form-item>
                      </el-col>
                      <el-col :span="15">
                        <el-form-item label="第三方接口">
                          <el-switch v-model="caseData.api_data[apiIndex].is_other_port"
                                     active-color="#13ce66"></el-switch>
                        </el-form-item>
                      </el-col>
                    </el-row>
                    <el-form-item label="host">
                      <el-select style="width: 10%" v-model="caseData.api_data[apiIndex].web_method" clearable>
                        <el-option label="http" value="http"></el-option>
                        <el-option label="https" value="https"></el-option>
                      </el-select>
                      <el-input placeholder="请输入地址端口" style="width: 90%"
                                v-model="caseData.api_data[apiIndex].host"></el-input>
                    </el-form-item>
                    <el-form-item label="路径">
                      <el-select style="width: 10%" v-model="caseData.api_data[apiIndex].method"
                                 default-first-option>
                        <el-option label="get" value="get"></el-option>
                        <el-option label="post" value="post"></el-option>
                        <el-option label="put" value="put"></el-option>
                        <el-option label="delete" value="delete"></el-option>
                        <el-option label="options" value="options"></el-option>
                      </el-select>
                      <el-input placeholder="请输入" style="width: 90%"
                                v-model="caseData.api_data[apiIndex].path"></el-input>
                    </el-form-item>
                  </el-form>
                  <el-tabs v-model="caseData.api_data[apiIndex].activeParams" type="border-card" id="active_params"
                           @tab-click="clickActiveParam">
                    <el-tab-pane label="Params" name="Params">
                      <el-table :data="caseData.api_data[apiIndex].params" border size="mini"
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
                                       @click.native.prevent="addRow(caseData.api_data[apiIndex].params)">新增
                            </el-button>
                          </template>
                          <template slot-scope="scope">
                            <el-button size="mini" type="text"
                                       @click="insertRow(scope.$index, caseData.api_data[apiIndex].params)">插入
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveUp(scope.$index, caseData.api_data[apiIndex].params)">上移
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveDown(scope.$index, caseData.api_data[apiIndex].params)">下移
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click.native.prevent="deleteRow(scope.$index, caseData.api_data[apiIndex].params)">
                              删除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="Headers" name="Headers">
                      <el-table :data="caseData.api_data[apiIndex].headers" border size="mini"
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
                                       @click.native.prevent="addRow(caseData.api_data[apiIndex].headers)">新增
                            </el-button>
                          </template>
                          <template slot-scope="scope">
                            <el-button size="mini" type="text"
                                       @click="insertRow(scope.$index, caseData.api_data[apiIndex].headers)">插入
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveUp(scope.$index, caseData.api_data[apiIndex].headers)">上移
                            </el-button>
                            <el-button size="mini" type="text"
                                       @click="moveDown(scope.$index, caseData.api_data[apiIndex].headers)">下移
                            </el-button>
                            <el-button size="small" type="text"
                                       @click.native.prevent="deleteRow(scope.$index, caseData.api_data[apiIndex].headers)">
                              删除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="Body" name="Body">
                      <el-tabs v-model="caseData.api_data[apiIndex].payload_method" @tab-click="clickBody"
                               id="body_data">
                        <el-tab-pane label="none" name="none">
                          <el-input type="textarea" rows="20" :disabled="true" placeholder="无需参数"
                                    class="textarea_disabled"
                                    style="text-align: center"></el-input>
                        </el-tab-pane>
                        <el-tab-pane label="form-data" name="form-data">
                          <el-table :data="caseData.api_data[apiIndex].payload_fd" border size="mini"
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
                            <el-table-column label="文件" width="200">
                              <template slot-scope="scope">
                                <el-upload
                                    class="upload-demo"
                                    ref="form-data-file"
                                    :http-request="uploadFormDataFile"
                                    action="#"
                                    :on-exceed="uploadLimit"
                                    :show-file-list="false"
                                    :limit="1"
                                >
                                  <el-button type="text" size="mini" @click="setFdIndex(scope.$index)">上传
                                  </el-button>
                                </el-upload>
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
                                           @click.native.prevent="addPayloadFdRow(caseData.api_data[apiIndex].payload_fd)">
                                  新增
                                </el-button>
                              </template>
                              <template slot-scope="scope">
                                <el-button size="mini" type="text"
                                           @click="insertFormData(scope.$index, caseData.api_data[apiIndex].payload_fd)">
                                  插入
                                </el-button>
                                <el-button size="mini" type="text"
                                           @click="moveUp(scope.$index, caseData.api_data[apiIndex].payload_fd)">上移
                                </el-button>
                                <el-button size="mini" type="text"
                                           @click="moveDown(scope.$index, caseData.api_data[apiIndex].payload_fd)">下移
                                </el-button>
                                <el-button size="mini" type="text"
                                           @click.native.prevent="deleteFormDataFile(scope.$index, caseData.api_data[apiIndex].payload_fd)">
                                  删除文件
                                </el-button>
                                <el-button size="mini" type="text"
                                           @click.native.prevent="deleteFormData(scope.$index)">
                                  删除
                                </el-button>
                              </template>
                            </el-table-column>
                          </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="x-www-form-urlencoded" name="x-www-form-urlencoded">
                          <el-table :data="caseData.api_data[apiIndex].payload_xwfu" border size="mini"
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
                                           @click.native.prevent="addRow(caseData.api_data[apiIndex].payload_xwfu)">
                                  新增
                                </el-button>
                              </template>
                              <template slot-scope="scope">
                                <el-button size="mini" type="text"
                                           @click="insertRow(scope.$index, caseData.api_data[apiIndex].payload_xwfu)">插入
                                </el-button>
                                <el-button size="mini" type="text"
                                           @click="moveUp(scope.$index, caseData.api_data[apiIndex].payload_xwfu)">上移
                                </el-button>
                                <el-button size="mini" type="text"
                                           @click="moveDown(scope.$index, caseData.api_data[apiIndex].payload_xwfu)">下移
                                </el-button>
                                <el-button size="small" type="text"
                                           @click.native.prevent="deleteRow(scope.$index, caseData.api_data[apiIndex].payload_xwfu)">
                                  删除
                                </el-button>
                              </template>
                            </el-table-column>
                          </el-table>
                        </el-tab-pane>
                        <el-tab-pane label="raw" name="raw">
                          <el-select v-model="caseData.api_data[apiIndex].raw_method" size="mini"
                                     style="width: 100px">
                            <el-option label="Text" value="Text"></el-option>
                            <el-option label="JavaScript" value="JavaScript"></el-option>
                            <el-option label="JSON" value="JSON"></el-option>
                            <el-option label="HTML" value="HTML"></el-option>
                            <el-option label="XML" value="XML"></el-option>
                          </el-select>
                          <b-code-editor v-if="caseData.api_data[apiIndex].raw_method==='JSON'"
                                         v-model="caseData.api_data[apiIndex].raw_data" ref="json_editor"
                                         :gutter="false"
                                         class="code_edit"></b-code-editor>
                          <el-input v-else type="textarea" rows="18"
                                    v-model="caseData.api_data[apiIndex].raw_data"></el-input>
                        </el-tab-pane>
                        <el-tab-pane label="binary" name="binary">
                          <el-upload
                              class="upload-demo"
                              ref="uploadBinary"
                              drag
                              :http-request="uploadBinaryFile"
                              action="#"
                              :on-success="binaryUpload"
                              :on-preview="handlePreview"
                              :on-remove="removeBinary"
                              :on-exceed="uploadLimit"
                              :file-list="payloadBinaryFile"
                              :limit="1"
                          >
                            <i class="el-icon-upload"></i>
                            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                            <div class="el-upload__tip" slot="tip"></div>
                          </el-upload>
                        </el-tab-pane>
                      </el-tabs>
                    </el-tab-pane>
                  </el-tabs>
                </div>
                <div v-else-if="confSet">
                  <div>
                    <el-form label-width="100px" label-position="left">
                      <el-form-item label="配置类型">
                        <el-input placeholder="请输入配置名称" style="width: 500px" disabled
                                  v-model="caseData.api_data[apiIndex].children[confIndex].run_time"></el-input>
                      </el-form-item>
                      <el-form-item label="配置名称">
                        <el-input placeholder="请输入配置名称" style="width: 500px"
                                  v-model="caseData.api_data[apiIndex].children[confIndex].label"></el-input>
                      </el-form-item>
                      <el-form-item label="配置脚本">
                        <el-row>
                          <el-col :span="17">
                            <el-input type="textarea" style="width: 100%" rows="25" placeholder="请输入脚本"
                                      resize="none"
                                      v-model="caseData.api_data[apiIndex].children[confIndex].do_action"></el-input>
                          </el-col>
                          <el-col :span="7">
                            <el-tree
                                v-if="showExec"
                                style="background-color: rgb(248, 248, 248); height: 462px"
                                highlight-current
                                @node-click="clickAddExec"
                                :data="showExecData">
                              <span slot-scope="{ node }">
                                <span style="font-size: 12px">{{ node.label }}</span>
                              </span>
                            </el-tree>
                          </el-col>
                        </el-row>
                      </el-form-item>
                      <el-form-item>
                        <el-button size="mini" type="primary" @click="showMock=true">mock变量</el-button>
                      </el-form-item>
                    </el-form>
                  </div>
                </div>
                <div v-else>请点击左侧节点</div>
              </div>
            </el-card>
            <el-card style="font-size: 14px; width: 400px" class="tree-card" id="api_tree">
              <el-button-group>
                <el-button type="primary" size="mini" style="margin-bottom: 5px" @click="addApi()">新增接口</el-button>
                <el-button type="primary" size="mini" @click="ApiListVisible=true">引入接口</el-button>
                <el-button type="primary" size="mini" @click="saveCase">保存</el-button>
                <el-button type="primary" size="mini" @click="runApis">运行</el-button>
                <router-link :to="'/debug_report?case_id='+this.case_id" target="_blank"
                             style="text-decoration-line: none;color: #FFF">
                  <el-button type="success" size="mini">报告</el-button>
                </router-link>
              </el-button-group>
              <el-tree
                  node-key="tree_id"
                  :data="caseData.api_data"
                  ref="api_tree"
                  draggable
                  @node-drop="handleDrop"
                  @node-expand="nodeExpand"
                  @node-collapse="nodeCollapse"
                  :expand-on-click-node="false"
                  :highlight-current="true"
                  :render-content="renderContent"
                  :allow-drop="allowDrop"
                  :default-expanded-keys="caseData.dek">
              </el-tree>
            </el-card>
          </el-tab-pane>
          <el-tab-pane label="基本信息">
            <el-form label-width="100px" style="padding: 10px"
                     label-position="left">
              <el-form-item label="用例名称">
                <el-input v-model="caseData.name" placeholder="请输入用例名称" style="width: 600px"></el-input>
              </el-form-item>
              <el-form-item label="所属模块">
                <el-select
                    style="width: 600px"
                    filterable
                    placeholder="请选择模块"
                    v-model="caseData.module_id">
                  <el-option
                      v-for="item in module_options"
                      :label="item.module_path"
                      :value="item.id"
                      :key="item.id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="责任人">
                <el-select
                    style="width: 600px"
                    filterable
                    placeholder="请选择责任人"
                    v-model="caseData.user_id">
                  <el-option
                      v-for="item in user_options"
                      :label="item.name"
                      :value="item.user"
                      :key="item.user">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="执行优先级" v-if="caseData.case_type===2">
                <el-input v-model="caseData.priority" style="width: 600px"></el-input>
              </el-form-item>
              <el-form-item label="host">
                <el-select style="width: 120px" v-model="caseData.web_method">
                  <el-option label="http" value="http"></el-option>
                  <el-option label="https" value="https"></el-option>
                </el-select>
                <el-input placeholder="请输入地址端口" v-model="caseData.host" style="width: 480px"></el-input>
              </el-form-item>
              <el-form-item label="用例描述">
                <el-input v-model="caseData.des" placeholder="请输入用例描述" style="width: 600px"></el-input>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="前置步骤">
            <el-card>
              <div slot="header">
                <span>已选用例（可选择多个）</span>
                <el-button size="mini" type="primary" @click="CaseListVisible=true">选择前置步骤</el-button>
              </div>
              <el-table border size="mini" :data="dependCase">
                <el-table-column label="用例名称" prop="name" width="300"></el-table-column>
                <el-table-column label="所属模块" prop="module" width="150"></el-table-column>
                <el-table-column label="用例描述" prop="des"></el-table-column>
                <el-table-column label="责任人" prop="user" width="150" align="center"></el-table-column>
                <el-table-column label="操作" align="center" width="150">
                  <template slot-scope="scope">
                    <router-link :to="'/case_detail?project_id='+project_id+'&case_id='+scope.row.case_id"
                                 target="_blank"
                                 style="margin-right: 10px">
                      <el-button type="text" size="mini">编辑</el-button>
                    </router-link>
                    <el-button type="text" size="mini" @click="deleteDependCase(scope.row.id)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
    <el-dialog title="选择配置类型" :visible.sync="activeConfAdd">
      <el-form v-model="addConfDefaultData">
        <el-form-item label="配置类型">
          <el-select style="width: 150px" v-model="addConfDefaultData.run_time" default-first-option>
            <el-option v-for="item in confType" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="activeConfAdd = false">取 消</el-button>
        <el-button type="primary" @click="addConf(addConfDefaultData)">确 定</el-button>
      </div>
    </el-dialog>
    <el-drawer
        :visible.sync="showMock"
        size="60%"
        :direction="'ltr'">
      <template slot="title">
        <span style="font-weight: bolder; color: #303133">内置环境变量</span>
      </template>
      <el-card>
        <div v-for="i in showMockData">
          <span style="font-size: 14px; font-weight: bolder">{{ i.type_name }}</span>
          <el-table :data="i.data" border size="mini">
            <el-table-column label="变量" prop="func_name" width="200">
              <template slot-scope="scope">
                <div>
                  <i>{{ scope.row.func_name }}</i>
                  <el-button type="text" size="mini" @click="clickCopy(scope.row.func_name)" style="float: right">
                    <span>复制</span>
                  </el-button>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="说明" prop="func_des"></el-table-column>
          </el-table>
          <br>
        </div>
      </el-card>
    </el-drawer>
    <el-dialog
        :visible.sync="ApiListVisible"
    >
      <ApiListView :showApiList="ApiListVisible" @toParent="clickImportApi"></ApiListView>
    </el-dialog>
    <el-dialog
        width="80%"
        :visible.sync="CaseListVisible">
      <ProjectCaseImportList :project_id="caseData.project_id" @toParent="clickImportCase"
                             :version_id="caseData.version_id"
                             :showCaseVisible="CaseListVisible" :case_type="caseData.case_type"></ProjectCaseImportList>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import ApiListView from "@/components/ApiListView.vue";
import ProjectCaseImportList from "@/components/ProjectCaseImportList.vue";

export default {
  name: "ProjectCase",
  components: {ProjectCaseImportList, ApiListView},
  computed: {},
  mounted() {
    this.case_id = parseInt(this.$route.query.case_id)
    this.project_id = parseInt(this.$route.query.project_id)
    this.caseDetail()
    this.userList()
    this.moduleOptions()
    this.funcOptions()
    this.getExecData()
    this.getCaseDepend()
    document.getElementById('api_detail').style.minHeight = (document.documentElement.clientHeight - 65).toString() + 'px';
    document.getElementById('api_detail').style.minHeight = (document.documentElement.clientHeight - 65).toString() + 'px';
    document.getElementById('api_tree').style.height = (document.documentElement.clientHeight - 65).toString() + 'px';
    document.getElementById('api_tree').style.maxHeight = (document.documentElement.clientHeight - 65).toString() + 'px';
  },
  data() {
    return {
      refVal: this.$refs,
      dependCase: [],
      CaseListVisible: false,
      queryCaseFields: {caseName: '', Page: 1, PageSize: 15},
      caseList: [{name: '用例名称', 'user': '责任人', status: '', disabled: ''}],
      ApiListVisible: false,
      ApisListData: [],
      allExecData: [],
      showExecData: [],
      showExec: false,
      showMock: false,
      showMockData: [],
      module_options: [],
      user_options: [],
      case_id: '',
      project_id: '',
      loading: false, // 加载状态
      fdIndex: '', // 上传fd时的索引
      addConfApiId: 0,
      progressPercent: 0,
      payloadBinaryFile: [{'name': '', 'url': ''}],
      confType: [{value: '前置处理器'}, {value: '后置处理器'}],
      addConfDefaultData: {run_time: '前置处理器', action_type: '定义变量'},
      activeConfAdd: false,
      apiTreeId: 0,
      confTreeId: 0,
      apiIndex: 0,
      addConfApiIndex: 0,
      confIndex: 0,
      apiSet: false,
      confSet: false,
      actionTreeId: 0,
      actionTreeData: {},
      activeRule: false,
      fileList: [],
      confTypeIsBefore: true,
      confTypeIsAfter: false,
      window_height: '',
      caseData: {
        case_id: '',  // 用例id
        name: '', // 用例名称
        des: '', // 用例描述
        dek: [], // 默认展开节点
        web_method: 'http',
        is_import: false,
        host: '',
        case_type: '',
        api_data: [],
      },
    }
  },
  methods: {
    clickBody(tab) {
      if (tab.index === "3") {
        this.refreshJson()
      }
    },
    clickActiveParam(tab) {
      if (tab.index === "2") {
        this.refreshJson()
      }
    },
    refreshJson() {
      let rawMethod
      let activeParams
      let payloadMethod
      rawMethod = this.caseData.api_data[this.apiIndex].raw_method
      activeParams = this.caseData.api_data[this.apiIndex].activeParams
      payloadMethod = this.caseData.api_data[this.apiIndex].payload_method
      if (activeParams === "Body" && payloadMethod === "raw" && rawMethod === "JSON") {
        this.$nextTick(() => {
          this.$refs['json_editor'].refresh()
        })
      }
    },
    deleteDependCase(id) {
      axios({
        method: 'get',
        url: '/delete_depend_case',
        params: {id: id}
      }).then(res => {
        this.$message({message: res.data.message, type: "success"})
        this.getCaseDepend()
      })
    },
    getCaseDepend() {
      axios({
        method: 'get',
        url: '/case_depend',
        params: {case_id: this.case_id}
      }).then(res => {
        this.dependCase = res.data.data
      })
    },
    clickImportApi(info) {
      this.addApi(info)
    },
    clickAddExec(data) {
      if (this.caseData.api_data[this.apiIndex].children[this.confIndex].do_action) {
        this.caseData.api_data[this.apiIndex].children[this.confIndex].do_action += '\n' + data.exec_value
      } else {
        this.caseData.api_data[this.apiIndex].children[this.confIndex].do_action += data.exec_value
      }
    },
    renderContent(h, {node, data, store}) {
      // 接口操作
      if (data.type === "api") {
        return (
            <span
                class="custom-tree-node"
                style="font-size: 14px;display: flex;flex: 1;justify-content: space-between;align-items: center">
            <span
                onClick={() => this.clickNode(data, node)}
                style={data.disabled ? 'color: darkgray;' : 'color: black;' + 'text-overflow:ellipsis;width: 200px;overflow: hidden'}>{node.label === '' ? '默认http请求' : node.label}</span>
            <span>
              <el-button size="mini" type="text"
                         on-click={() => this.doDisable(data)}>{data.disabled ? "启用" : "禁用"}</el-button>
              <el-button size="mini" type="text" on-click={() => this.clickAddConf(node, data)}>新增</el-button>
              <el-button size="mini" type="text" on-click={() => this.removeApi(node, data)}>删除</el-button>
            </span>
          </span>
        );
      }
      // 配置操作
      else {
        return (
            <span
                class="custom-tree-node"
                style="font-size: 14px;display: flex;flex: 1;justify-content: space-between;align-items: center">
            <span
                onClick={() => this.clickNode(data, node)}
                style={data.disabled ? 'color: darkgray;' : 'color: black;' + 'text-overflow:ellipsis;width: 180px;overflow: hidden'}>{node.label === '' ? '处理器名称' : node.label}</span>
            <span>
              <el-button size="mini" type="text"
                         on-click={() => this.doDisable(data)}>{data.disabled ? "启用" : "禁用"}</el-button>
              <el-button size="mini" type="text" on-click={() => this.removeConf(node, data)}>删除</el-button>
            </span>
          </span>
        );
      }
    },
    clickCopy(value) {
      let oInput = document.createElement('input')
      oInput.value = value
      document.body.appendChild(oInput)
      oInput.select();
      document.execCommand('Copy')
      this.$message({message: '复制成功', type: 'success', duration: 1000})
      oInput.remove()
    },
    getExecData() {
      axios({
        method: "get",
        url: 'get_exec'
      }).then(res => {
        this.allExecData = res.data.data
      })
    },
    funcOptions() {
      axios({
        method: 'get',
        url: 'get_func',
      }).then(res => {
        this.showMockData = res.data.data
      })
    },
    moduleOptions() {
      axios({
        method: 'get',
        url: 'module_options',
        params: {
          project_id: this.project_id
        }
      }).then(res => {
        this.module_options = res.data.data
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
    copyApi() {
      this.openFullScreen()
      axios({
        url: 'save_case',
        params: {
          project_id: this.project_id,
          case_id: this.case_id
        },
        method: 'post',
        data: {
          case_id: this.case_id,
          data: this.caseData
        },
      }).then(res => {
        axios({
          url: 'copy_case_api',
          params: {id: this.caseData.api_data[this.apiIndex].tree_id}
        }).then(res => {
          this.$message({message: res.data.message, type: res.data.type});
          this.caseData.api_data.push(res.data.data);
          this.closeFullScreen()
          this.$message({"message": res.data.message, "type": res.data.type});
        })
      })
    },
    addApi(initData = '') {
      let addApiData = {case_id: this.case_id, project_id: this.project_id,}
      if (initData !== '') {
        addApiData = Object.assign(addApiData, initData)
      }
      axios({
        url: '/add_case_api/',
        method: 'post',
        data: addApiData,
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type});
        this.caseData.api_data.push(res.data.data);
      })
    },
    clickAddConf(node, data) {
      // 点击新增配置时，获取api节点的索引
      const parent = node.parent;
      const children = parent.data;
      this.addConfApiId = data.tree_id;
      this.addConfApiIndex = children.findIndex(d => d.tree_id === data.tree_id);
      this.activeConfAdd = true;
    },
    addConf(data) {
      // 添加接口配置
      const conf = {
        tree_id: this.addConfApiId.toString() + '_' + this.caseData.api_data[this.addConfApiIndex].children.length.toString(),
        label: data.run_time,
        type: "config",
        api_id: this.addConfApiId,
        project_id: this.project_id,
        run_time: data.run_time,
        disabled: false,
        // action_type: data.action_type,
      };
      axios({
        method: 'post',
        url: '/add_case_conf/',
        data: conf
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type});
        this.caseData.api_data[this.addConfApiIndex].children.push(res.data.data);
        this.activeConfAdd = false;
      })
    },
    removeApi(node, data) {
      // 删除接口
      const parent = node.parent;
      const children = parent.data;
      const index = children.findIndex(d => d.tree_id === data.tree_id);
      if (data.tree_id === this.apiTreeId) {
        // 删除节点是当前显示节点或包含当前显示节点，则不显示
        this.apiSet = false;
        this.confSet = false;
        this.confIndex = 0;
        this.apiIndex = 0;
      }
      // 当前节点是展开api节点，则删除展示节点列表
      const id_index = this.caseData.dek.indexOf(data.tree_id);
      if (id_index >= 0) {
        this.caseData.dek.splice(id_index, 1);
      }
      axios({
        url: '/del_case_api',
        params: {
          case_id: this.case_id,
          tree_id: data.tree_id,
        },
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
      })
      // 删除节点
      children.splice(index, 1);
      this.getActionTreeIndex();
    },
    removeConf(node, data) {
      // 删除配置
      const parent = node.parent;
      const children = parent.data.children
      const index = children.findIndex(d => d.tree_id === data.tree_id);
      if (data.tree_id === this.confTreeId) {
        // 删除节点是当前显示节点，则不显示
        this.apiSet = false;
        this.confSet = false;
        this.confIndex = 0;
        this.apiIndex = 0;
      }
      // 删除节点
      axios({
        url: '/del_case_conf/',
        method: 'get',
        params: {conf_id: data.conf_id},
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type});
        children.splice(index, 1);
        this.getActionTreeIndex();
      })
    },
    doDisable(data) {
      data.disabled = !data.disabled;
    },
    clickNode(data, node) {
      this.actionTreeId = data.tree_id;
      if (data.type === 'api') {
        this.payloadBinaryFile = []
        this.showMock = false;
        this.apiSet = true;
        this.confSet = false;
        this.apiTreeId = data.tree_id
        this.getActionTreeIndex()
        this.refreshJson()
        if (this.caseData.api_data[this.apiIndex].payload_binary_original_name) {
          const addFile =
              {
                name: this.caseData.api_data[this.apiIndex].payload_binary_original_name,
              }
          this.payloadBinaryFile.push(addFile)
        }
      } else {
        if (data.run_time === '前置处理器') {
          this.showExecData = this.allExecData['all']
        } else if (data.run_time === '后置处理器') {
          this.showExecData = this.allExecData['after'].concat(this.allExecData['all'])
        }
        this.showExec = true
        this.apiSet = false;
        this.confSet = true;
        this.apiTreeId = node.parent.data.tree_id
        this.confTreeId = data.tree_id
        this.getActionTreeIndex()
      }
    },
    nodeExpand(data) {
      this.caseData.dek.push(data.tree_id)
    },
    nodeCollapse(data) {
      const node_index = this.caseData.dek.findIndex(d => d === data.tree)
      this.caseData.dek.splice(node_index, 1)
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
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
    addRow(rows) {
      rows.push({key: '', value: '', des: '',})
    },
    allowDrop(draggingNode, dropNode, type) {
      // 只允许同一个父节点下拖拽
      if (draggingNode.data.type === dropNode.data.type) {
        return type !== 'inner'
      }
    },
    handleDrop(draggingNode, dropNode, dropType, ev) {
      // 拖拽时刷新索引
      this.getActionTreeIndex();
    },
    saveCase() {
      this.openFullScreen()
      axios({
        url: 'save_case',
        params: {
          project_id: this.project_id,
          case_id: this.case_id
        },
        method: 'post',
        data: {
          case_id: this.case_id,
          data: this.caseData
        },
      }).then(res => {
        this.caseData = res.data.caseData
        this.$message({"message": res.data.message, "type": res.data.type})
        this.closeFullScreen()
      })
    },
    clickImportCase(case_id) {
      axios({
        url: '/add_depend_case',
        params: {
          id: this.case_id,
          depend_id: case_id
        },
        method: 'get',
      }).then(res => {
        this.$message({"message": res.data.message, "type": res.data.type})
        this.getCaseDepend()
      })
    },
    getActionTreeIndex() {
      // 刷新当前树节点数据的索引
      let apis = this.caseData.api_data
      this.apiIndex = apis.findIndex(d => d.tree_id === this.apiTreeId)
      if (this.confSet) {
        let confs = apis[this.apiIndex]['children']
        this.confIndex = confs.findIndex(d => d.tree_id === this.confTreeId)
      }
    },
    openFullScreen() {
      this.loading = this.$loading({
        lock: true,
      })
    },
    closeFullScreen() {
      this.loading.close()
    },
    runApi() {
      // 判断当前接口是否禁用
      if (this.caseData.api_data[this.apiIndex].disabled) {
        this.$message.warning(this.caseData.api_data[this.apiIndex].label + '：接口已禁用')
      } else {
        this.openFullScreen()
        axios({
          url: '/run_api/',
          params: {
            project_id: this.project_id,
            case_id: this.case_id,
            api_id: this.actionTreeId,
          },
          method: 'post',
          data: {
            case_id: this.case_id,
            data: this.caseData,
          },
        }).then(res => {
          this.caseData = res.data.caseData;
          this.$message({"message": '执行成功，报告已生成', "type": "success"});
          this.closeFullScreen()
        })
      }
    },
    runApis() {
      this.openFullScreen()
      axios({
        url: '/run_apis/',
        params: {
          project_id: this.project_id,
          case_id: this.case_id,
        },
        method: 'post',
        data: {
          case_id: this.case_id,
          data: this.caseData,
        },
      }).then(res => {
        this.caseData = res.data.caseData;
        this.$message({"message": '执行成功，报告已生成', "type": "success"});
        this.closeFullScreen()
      })
    },
    caseDetail() {
      axios.get('/case_detail/', {
            params: {
              case_id: this.case_id
            }
          }
      ).then(res => {
        this.caseData = res.data.caseData;
      })
    },
    EditValue(index, row) {
    },
    uploadBinaryFile(params) {
      this.progressPercent = 0
      const
          formData = new FormData();
      formData.append('file', params.file)
      axios({
        method: 'post',
        url: '/upload_binary_file/',
        params: {case_id: this.case_id, tree_id: this.caseData.api_data[this.apiIndex].tree_id},
        data: formData,
        onUploadProgress: progressEvent => {
          const complete = (progressEvent.loaded / progressEvent.total * 100 | 0)
          params.onProgress({percent: complete})
        }
      }).then(res => {
            params.onSuccess(res)
            this.$message({message: res.data.message, type: res.data.type})
          }
      )
    },
    setFdIndex(index) {
      this.fdIndex = index
    },
    uploadFormDataFile(params) {
      if (this.caseData.api_data[this.apiIndex].payload_fd[this.fdIndex].isFile) {
        this.$message.warning('重新上传请先删除已传文件')
      } else {
        this.progressPercent = 0
        const formData = new FormData();
        formData.append('file', params.file)
        axios({
          method: 'post',
          url: '/upload_form_data_file/',
          params: {
            case_id: this.case_id,
            tree_id: this.caseData.api_data[this.apiIndex].tree_id,
            row: this.fdIndex
          },
          data: formData,
          onUploadProgress: progressEvent => {
            const complete = (progressEvent.loaded / progressEvent.total * 100 | 0)
            params.onProgress({percent: complete})
          }
        }).then(res => {
              // 回填对应行的fd数据
              this.caseData.api_data[this.apiIndex].payload_fd[this.fdIndex].isFile = true;
              this.caseData.api_data[this.apiIndex].payload_fd[this.fdIndex].value = res.data.value;
              this.caseData.api_data[this.apiIndex].payload_fd[this.fdIndex].file_name = res.data.file_name;
              // 保存上传信息
              this.saveApiFormData("upload");
            }
        )
      }
    },
    saveApiFormData(action) {
      axios({
        url: '/save_form_data/',
        method: 'post',
        params: {
          case_id: this.case_id,
          tree_id: this.caseData.api_data[this.apiIndex].tree_id,
          row: this.fdIndex,
          action: action,
        },
        data: this.caseData.api_data[this.apiIndex].payload_fd
      }).then(res => {
        this.caseData.api_data[this.apiIndex].payload_fd = res.data.form_data
        this.$message({message: res.data.message, type: res.data.type}
        )
      })
    },
    addPayloadFdRow(rows) {
      rows.push({key: '', value: '', isFile: false, file_name: '', des: ''})
    },
    insertFormData(index, row) {
      row.splice(index, 0, {key: '', value: '', isFile: false, file_name: '', des: ''})
    },
    deleteFormData(index, rows) {
      this.setFdIndex(index)
      this.saveApiFormData('remove')
    },
    deleteFormDataFile(index, raws) {
      if (raws[index].isFile) {
        this.setFdIndex(index)
        this.saveApiFormData('removeFile')
        this.$refs["form-data-file"].clearFiles()
      } else {
        this.$message.warning('未上传文件')
      }
    },
    binaryUpload(res, file, fileList) {
      // 回填前端数据
      this.caseData.api_data[this.apiIndex].payload_binary_original_name = res.data.payload_binary_original_name
      this.caseData.api_data[this.apiIndex].payload_binary_name = res.data.payload_binary_name
    },
    removeBinary(file, fileList) {
      axios({
        method: 'get',
        url: '/remove_binary_file/',
        params: {case_id: this.case_id, tree_id: this.caseData.api_data[this.apiIndex].tree_id},
      }).then(res => {
        this.payloadBinaryFile.pop();
        this.caseData.api_data[this.apiIndex].payload_binary_name = '';
        this.caseData.api_data[this.apiIndex].payload_binary_original_name = '';
        this.$message({message: res.data.message, type: res.data.type})
      })
    },
    handlePreview(file) {
      // 上传文件
    },
    uploadLimit() {
      this.$message.warning('重新上传请先删除已传文件')
    },
  },
}
</script>

<style scoped>
/*#api_detail /deep/ .el-card__body{*/
/*  padding: 0 0 5px 20px !important;*/
/*}*/
/*#active_params /deep/ .el-tabs__content{*/
/*  padding: 0 0 5px 20px !important;*/
/*}*/
::-webkit-scrollbar {
  width: 0;
  height: 0;
  opacity: 0;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
  background-color: white;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
  background-color: #b3b3b3;
}

.el-textarea__inner {
  font-size: 13px !important;
  line-height: 13px !important;
}

.code_edit /deep/ span {
  line-height: 13px !important;
  font-size: 13px !important;
}

.code_edit {
  height: 335px !important;
}

.el-tree:hover {
  overflow-y: auto;
  overflow-x: inherit;
}

p {
  color: gray;
  font-size: xx-small;
}

.textarea_disabled /deep/ .el-textarea__inner {
  color: #606266 !important;
  cursor: auto !important;
}

.textarea_disabled /deep/ textarea::-webkit-input-placeholder {
  color: #606266 !important;
}

#api_tree /deep/ span {
  font-size: 14px !important;
}

.el-button span {
  font-size: small;
}

.mock_label {
  width: 200px;
  background: #E1F3D8;
}

.el-table /deep/ * {
  font-size: 14px !important;
}
</style>