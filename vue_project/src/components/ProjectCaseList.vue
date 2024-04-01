<template>
  <div>
    <el-card style="float: right;width: 84%" id="case_list">
      <el-form :data="queryFields" style="width: 100%" @submit.prevent.native>
        <el-row>
          <el-col :span="6">
            <el-form-item label="用例名称">
              <el-input style="width: 200px" v-model="queryFields.caseName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="责任人">
              <el-select
                  style="width: 150px"
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
              <el-select v-model="queryFields.status">
                <el-option
                    v-for="item in statusOptions"
                    :label="item.name"
                    :value="item.value"
                    :key="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <div style="float: right">
            <el-button type="primary" @click="openNewCase" size="mini">新增</el-button>
            <el-button type="primary" @click="getCases" size="mini" native-type="submit">查询</el-button>
          </div>
        </el-row>
      </el-form>
      <el-table :data="caseList" type="index" border :highlight-current-row="true" :height="650" size="mini"
                style="margin-bottom: 10px">
        <template slot-scope="scope">
          <el-table-column label="序号" type="index" width="80" align="center"></el-table-column>
          <el-table-column label="用例名称" prop="name" width="300"></el-table-column>
          <el-table-column label="所属模块" prop="module" width="150"></el-table-column>
          <el-table-column label="用例描述" prop="des"></el-table-column>
          <el-table-column label="是否启用" width="100" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.is_active ? '是' : '否' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="执行优先级" v-if="case_type === 2" prop="priority" width="120"
                           align="center"></el-table-column>
          <el-table-column label="责任人" prop="user" width="150" align="center"></el-table-column>
          <el-table-column label="操作" align="center" width="150">
            <template slot-scope="scope">
              <router-link :to="'/case_detail?project_id='+project_id+'&case_id='+scope.row.id" target="_blank"
                           style="margin-right: 10px">
                <el-button type="text" size="mini">编辑</el-button>
              </router-link>
              <el-button type="text" size="mini" @click="changeCaseStatus(scope.row.id)">{{ scope.row.is_active? '禁用' : '启用' }}</el-button>
              <el-button type="text" size="mini" @click="handleClose(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </template>
      </el-table>
      <el-pagination
          style="float: right"
          background
          :page-sizes="[15,30,50]"
          :page-size="this.queryFields.PageSize"
          layout="total, prev, pager, next, jumper, sizes"
          @size-change="changeSize"
          @current-change="handleCurrentChange"
          :total="caseTotal">
      </el-pagination>
      <el-dialog title="用例信息" :visible.sync="dialogCaseForm" :destroy-on-close="true">
        <el-form :model="caseData" label-width="100px">
          <el-form-item label="用例名称">
            <el-input v-model="caseData.name"></el-input>
          </el-form-item>
          <el-form-item label="所属模块">
            <el-select
                style="width: 100%"
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
          <el-form-item label="用例描述">
            <el-input v-model="caseData.des"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogCaseForm = false">取 消</el-button>
          <el-button type="primary" @click="addCase()">确 定</el-button>
        </div>
      </el-dialog>
      <el-dialog
          title="提示"
          :visible.sync="dialogConfirmVisible"
          width="30%">
        <span>是否删除用例？</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="dialogConfirmVisible = false">取 消</el-button>
        <el-button type="primary" @click="removeCase">确 定</el-button>
      </span>
      </el-dialog>
    </el-card>
    <el-card style="width: 15%; height: 778px;overflow: auto" id="module_tree">
      <el-button style="width: 100%" type="primary" @click="clickModuleEdit">模块管理</el-button>
      <el-tree :data="module_data" :props="defaultProps" :render-content="renderContent"
               :expand-on-click-node="false" highlight-current></el-tree>
    </el-card>
    <el-dialog id="module_edit" title="项目模块" :visible.sync="activeEditModule" :modal-append-to-body="true"
               @close="moduleTree">
      <ModuleEdit :module_data="module_data" :project_id="project_id"></ModuleEdit>
      <span slot="footer" class="dialog-footer">
        <el-button @click="activeEditModule = false">取 消</el-button>
        <el-button type="primary" @click="clickConfirm">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import ModuleEdit from "@/components/ModuleEdit.vue";

export default {
  name: "ProjectCaseList",
  components: {ModuleEdit},
  props: ['project_id', 'case_type', 'version_id'],
  data() {
    return {
      user_options: [],
      statusOptions:[{value:'',name:'请选择'},{value:1,name:'启用'},{value:0,name:'禁用'}],
      project_id: this.project_id,
      version_id: this.version_id,
      module_options: [],
      caseTotal: 0,
      queryFields: {
        user: '',
        caseName: '',
        moduleId: '',
        case_type: this.case_type,
        project_id: this.project_id,
        version_id: this.version_id,
        status: '',
        Page: 1,
        PageSize: 15
      },
      activeEditModule: false,
      defaultProps: {
        children: 'children',
        label: 'module_name'
      },
      table_height: '',
      module_data: [],
      delete_case_id: '',
      dialogConfirmVisible: false,
      dialogCaseForm: false,
      caseData: {
        name: '',
        des: '',
        module_id: '',
      },
      caseList: []
    }
  },
  methods: {
    changeCaseStatus(id) {
      axios({
        url: 'change_case_status',
        params: {id: id}
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.getCases()
      })
    },
    changeSize(val) {
      this.queryFields.PageSize = val
      this.getCases()
    },
    renderContent(h, {node, data, store}) {
      return (
          <span class="custom-tree-node" style="font-size: 14px">
            <span onClick={() => this.clickModule(data, node)}>{node.label}</span>
          </span>);
    },
    handleCurrentChange(page) {
      this.queryFields.Page = page
      this.getCases()
    },
    userList() {
      axios({
        url: '/base_user',
        method: 'get',
      }).then(res => {
        this.user_options = res.data
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
    clickModule(data, node) {
      this.queryFields.moduleId = data.id
      this.getCases()
    },
    clickModuleEdit() {
      this.activeEditModule = true
      this.moduleTree()
    },
    clickConfirm() {
      this.activeEditModule = false
      this.moduleTree()
    },
    openNewCase() {
      this.caseData = this.$options.data().caseData;
      this.dialogCaseForm = true;
    },
    moduleTree() {
      axios({
        url: '/module_detail',
        method: "get",
        params: {
          project_id: this.project_id
        }
      }).then(res => {
        this.module_data = res.data.data
      })
    },
    addCase() {
      axios({
        method: 'post',
        url: '/add_case/',
        data: {
          project_id: this.project_id,
          module_id: this.caseData.module_id,
          version_id: this.version_id,
          case_type: this.case_type,
          name: this.caseData.name,
          des: this.caseData.des,
        }
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type});
        this.dialogCaseForm = false;
        this.caseList = res.data;
        this.getCases();
      })
    },
    removeCase() {
      axios({
        url: '/remove_case/',
        method: 'get',
        params: {
          id: this.delete_case_id,
          project_id: this.project_id,
        }
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type});
        this.dialogConfirmVisible = false;
        this.getCases();
      })
    },
    getCases() {
      axios({
        method: 'get',
        url: '/testcase_list',
        params: this.queryFields
      }).then(res => {
        this.caseList = res.data.data
        this.caseTotal = res.data.total
      })
    },
    handleClose(id) {
      this.dialogConfirmVisible = true;
      this.delete_case_id = id;
    }
  },

  mounted() {
    this.userList();
    this.getCases();
    this.moduleTree();
    this.moduleOptions();
    this.table_height = document.getElementById("case_list").style.height
    const tree = document.getElementById('module_tree').style
    tree.maxHeight = tree.minHeight = this.table_height.toString() + 'px'
  }
}
</script>

<style scoped>

#module_tree /deep/ span {
  font-size: 14px !important;
}

#module_edit /deep/ .el-dialog {
  height: 600px;
  overflow: auto;
}

.el-table /deep/ * {
  font-size: 14px !important;
}
</style>