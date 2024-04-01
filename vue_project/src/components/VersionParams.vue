<template>
  <div>
    <el-form @submit.native.prevent>
      <el-row>
        <el-col :span="6">
          <el-form-item label="运行环境">
            <el-input style="width: 70%" placeholder="请输入环境地址，127.0.0.1:8080"
                      v-model="queryFields.host"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="变量名">
            <el-input style="width: 70%" placeholder="请输入变量名" v-model="queryFields.key"></el-input>
          </el-form-item>
        </el-col>
        <div style="float: right">
          <el-button type="primary" @click="clickAdd">新增</el-button>
          <el-button type="primary" @click="paramsList" native-type="submit">查询</el-button>
        </div>
      </el-row>
    </el-form>
    <el-table :data="paramsDataList" border :highlight-current-row="true" style="margin-top: 10px" height="740"
              size="mini">
      <el-table-column label="序号" type="index" align="center" width="80"></el-table-column>
      <el-table-column label="变量名" prop="key"></el-table-column>
      <el-table-column label="变量值" prop="value"></el-table-column>
      <el-table-column label="参数说明" prop="des"></el-table-column>
      <el-table-column label="运行环境" prop="run_env" width="250"></el-table-column>
      <el-table-column label="常数变量" prop="is_share" width="100" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.is_share">是</span>
          <span v-else>否</span>
        </template>
      </el-table-column>
      <el-table-column label="绑定用例">
        <template slot-scope="scope">
          <router-link :to="'/case_detail?project_id='+$route.query.project_id+'&case_id='+ scope.row.bind_case_id"
                       target="_blank" style="color: #409EFF;text-decoration-line: none">{{ scope.row.case_name }}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="120">
        <template slot-scope="scope">
          <el-button @click="clickEdit(scope.row.id)" type="text">编辑</el-button>
          <el-button @click="deleteParams(scope.row.id)" type="text">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15,30,50]"
        :page-size="this.queryFields.PageSize"
        layout="total, prev, pager, next, jumper, sizes"
        @current-change="changePage"
        @size-change="changeSize"
        :total="count">
    </el-pagination>
    <el-dialog title="参数信息" :visible.sync="dialogParamsForm" :destroy-on-close="true">
      <el-form :model="paramsData" label-width="100px">
        <el-form-item label="所属项目">
          <el-select
              disabled
              style="width: 100%"
              filterable
              v-model="paramsData.project_id">
            <el-option
                v-for="item in projectOptions"
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
              v-model="paramsData.version_id">
            <el-option
                v-for="item in versionOptions"
                :label="item.version_name"
                :value="item.id"
                :key="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="参数名">
          <el-input v-model="paramsData.key" placeholder="请输入参数名（字母、数字、下划线组成）"></el-input>
        </el-form-item>
        <el-form-item label="参数值">
          <el-input v-model="paramsData.value" placeholder="请输入参数值"></el-input>
        </el-form-item>
        <el-form-item label="是否常数">
          <el-switch active-color="#13ce66" v-model="paramsData.is_share"></el-switch>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="paramsData.des" type="textarea" rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogParamsForm = false">取 消</el-button>
        <el-button type="primary" @click="editParams">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProjectParams",
  data() {
    return {
      dialogParamsForm: false,
      paramsData: {
        version_id: null,
        project_id: null,
        is_share: true,
      },
      paramsDataList: [],
      queryFields: {
        Page: 1,
        PageSize: 15,
        key: '',
        host: '',
        version_id: null,
        project_id: null,
      },
      count: 0,
      projectOptions: [],
      versionOptions: [],
    }
  },
  methods: {
    changePage(val){
      this.queryFields.Page = val
      this.paramsList()
    },
    changeSize(val){
      this.queryFields.PageSize = val
      this.paramsList()
    },
    clickAdd() {
      this.paramsData = this.$options.data().paramsData
      this.paramsData.project_id = Number(this.$route.query.project_id)
      this.paramsData.version_id = Number(this.$route.query.version_id)
      this.dialogParamsForm = true
    },
    paramsList() {
      this.queryFields.version_id = this.$route.query.version_id
      this.queryFields.project_id = this.$route.query.project_id
      axios({
        method: 'get',
        params: this.queryFields,
        url: '/params_list',
      }).then(res => {
        this.paramsDataList = res.data.data
        this.count = res.data.count
      })
    },
    editParams() {
      axios({
        method: 'post',
        url: '/params_edit',
        data: this.paramsData,
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.paramsList()
        this.dialogParamsForm = false
      })
    },
    deleteParams(id) {
      axios({
        method: 'get',
        url: '/params_delete',
        params: {id: id}
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.paramsList()
      })
    },
    clickEdit(id) {
      axios({
        method: 'get',
        params: {id: id},
        url: '/params_detail'
      }).then(res => {
        this.paramsData = res.data.data
        this.dialogParamsForm = true
      })
    }
  },
  mounted() {
    this.paramsList()
    axios({
      url: '/project_option',
      method: "get"
    }).then(res => {
      this.projectOptions = res.data.data;
    })
    axios({
      method: 'get',
      url: '/version_options',
      params: {project_id: this.$route.query.project_id}
    }).then(res => {
      this.versionOptions = res.data.data
    })
  }
}
</script>

<style scoped>
.el-form .el-form-item {
  margin-bottom: 5px !important;
}

.el-table /deep/ * {
  font-size: 14px !important;
}

</style>