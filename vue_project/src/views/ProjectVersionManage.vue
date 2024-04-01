<template>
  <div>
    <div style="line-height: 50px; float: right">
      <el-form @submit.native.prevent>
        <el-input placeholder="请输入版本名称" v-model="queryFields.version_name" style="width: 300px">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-button type="primary" @click="getVersionList" native-type="submit">查询</el-button>
        <el-button type="primary" @click="clickAdd">新增版本</el-button>
      </el-form>
    </div>
    <div>
      <el-table :data="versionList" border style="width: 100%" :highlight-current-row="true" height="750">
        <el-table-column type="index" label="序号" prop="index" width="70" align="center"></el-table-column>
        <el-table-column label="版本名称" prop="version_name"></el-table-column>
        <el-table-column label="版本编号" prop="version_code"></el-table-column>
        <el-table-column prop="project_name" label="所属项目" width="300"></el-table-column>
        <el-table-column prop="create_time" label="创建时间"></el-table-column>
        <el-table-column prop="des" label="描述"></el-table-column>
        <el-table-column fixed="right" label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="mini" @click="clickEdit(scope.row.id)">编辑</el-button>
            <el-button type="text" size="mini"
                       @click="goVersionHome(scope.row.project_id, scope.row.id)">
              进入
            </el-button>
            <el-button type="text" size="mini" @click="clickCopy(scope.row.id)">复制</el-button>
            <el-button type="text" size="mini" style="margin-left: 5px" @click="clickDelete(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          style="float: right"
          background
          :page-sizes="[15]"
          :page-size="this.queryFields.PageSize"
          layout="total, prev, pager, next, jumper, sizes"
          @current-change="getVersionList"
          :total="count">
      </el-pagination>
      <el-dialog title="项目版本" :visible.sync="dialogFormVisible" :destroy-on-close="true">
        <el-form :model="versionData" label-width="80px">
          <el-form-item label="版本名称">
            <el-input style="width: 100%" v-model="versionData.version_name" placeholder="请输入"></el-input>
          </el-form-item>
          <el-form-item label="所属项目">
            <el-select
                style="width: 100%"
                filterable
                placeholder="请选择项目"
                v-model="versionData.project_id">
              <el-option
                  v-for="item in projectOptions"
                  :label="item.project_name"
                  :value="item.project_id"
                  :key="item.project_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="版本编号">
            <el-input v-model="versionData.version_code" placeholder="请输入"></el-input>
          </el-form-item>
          <el-form-item label="版本描述">
            <el-input type="textarea" :rows="3" v-model="versionData.des" placeholder="请输入"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="versionEdit">确 定</el-button>
        </div>
      </el-dialog>
      <el-dialog title="复制版本" :visible.sync="dialogCopyInfoVisible" :destroy-on-close="true">
        <el-form :model="copyVersionData" label-width="80px">
          <el-form-item label="版本名称">
            <el-input style="width: 100%" v-model="copyVersionData.version_name" placeholder="请输入"></el-input>
          </el-form-item>
          <el-form-item label="所属项目">
            <el-select
                disabled
                style="width: 100%"
                filterable
                placeholder="请选择项目"
                v-model="copyVersionData.project_id">
              <el-option
                  v-for="item in projectOptions"
                  :label="item.project_name"
                  :value="item.project_id"
                  :key="item.project_id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="版本编号">
            <el-input v-model="copyVersionData.version_code" placeholder="请输入"></el-input>
          </el-form-item>
          <el-form-item label="版本描述">
            <el-input type="textarea" :rows="3" v-model="copyVersionData.des" placeholder="请输入"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogCopyInfoVisible = false">取 消</el-button>
          <el-button type="primary" @click="copyVersion">确 定</el-button>
        </div>
      </el-dialog>
      <el-dialog
          title="提示"
          :visible.sync="dialogConfirmVisible"
          width="30%">
        <span>是否删除版本？</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="dialogConfirmVisible = false">取 消</el-button>
        <el-button type="primary" @click="deleteVersion">确 定</el-button>
      </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProjectVersionManage",
  watch: {
    dialogFormVisible: {
      handler(newVal) {
        if (newVal) {
          this.getProjectOptions()
        }
      }
    },
    dialogCopyInfoVisible: {
      handler(newVal) {
        if (newVal) {
          this.getProjectOptions()
        }
      }
    },
  },
  data() {
    return {
      versionList: [],
      projectOptions: [],
      versionData: {version_name: '', project_id: null, version_code: '', des: ''},
      copyVersionData: {version_name: '', project_id: null, version_code: '', des: ''},
      queryFields: {version_name: '', Page: 1, PageSize: 15},
      count: 0,
      dialogFormVisible: false,
      dialogCopyInfoVisible: false,
      dialogConfirmVisible: false,
      deleteVersionId: null,
    }
  },
  methods: {
    clickDelete(id) {
      this.deleteVersionId = id
      this.dialogConfirmVisible = true
    },
    deleteVersion() {
      axios({
        method: 'get',
        url: '/version_delete',
        params: {id: this.deleteVersionId}
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.getVersionList()
        this.dialogConfirmVisible = false
      })
    },
    goVersionHome(project_id, version_id, project_name, version_name) {
      let routeUrl = this.$router.resolve({
        path: '/version_case',
        query: {project_id: project_id, version_id: version_id, project_name: project_name, version_name: version_name}
      })
      window.open(routeUrl.href, '_blank')
    },
    clickEdit(id) {
      this.versionDetail(id)
      this.dialogFormVisible = true
    },
    clickCopy(id) {
      axios({
        url: '/version_detail',
        params: {id: id}
      }).then(res => {
        this.copyVersionData = res.data.version_data
        this.copyVersionData.version_name = '复制-' + this.copyVersionData.version_name
      })
      this.dialogCopyInfoVisible = true
    },
    copyVersion() {
      axios({
        url: '/version_copy',
        method: 'post',
        data: this.copyVersionData,
      }).then(res => {
        this.$message({message: res.data.message, type:res.data.type})
        this.getVersionList()
        this.dialogCopyInfoVisible = false
      })
    },
    clickAdd() {
      this.versionData = this.$options.data().versionData
      this.dialogFormVisible = true
    },
    getProjectOptions() {
      axios({
        method: 'get',
        url: '/project_options',
      }).then(res => {
        this.projectOptions = res.data.data
      })
    },
    versionEdit() {
      axios({
        method: 'post',
        url: '/version_edit',
        data: this.versionData
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        this.dialogFormVisible = false
      })
    },
    getVersionList() {
      axios({
        url: 'version_list',
        params: this.queryFields
      }).then(res => {
        this.versionList = res.data.data
      })
    },
    versionDetail(id) {
      axios({
        url: '/version_detail',
        params: {id: id}
      }).then(res => {
        this.versionData = res.data.version_data
      })
    }
  },
  mounted() {
    this.getVersionList()
  }
}
</script>

<style scoped>

</style>