<template>
  <div>
    <el-form @submit.native.prevent>
      <el-form-item>
        <div style="float: right">
          <el-input style="width: 300px; margin-right: 5px" v-model="queryFields.caseName"
                    placeholder="请输入用例名称"></el-input>
          <el-button type="primary" @click="getCases" native-type="submit">查询</el-button>
        </div>
      </el-form-item>
    </el-form>
    <el-table :data="caseList" type="index" border :highlight-current-row="true" :height="500" size="mini"
              style="margin-bottom: 10px">
      <template slot-scope="scope">
        <el-table-column label="序号" type="index" width="80" align="center"></el-table-column>
        <el-table-column label="用例名称" prop="name" width="300"></el-table-column>
        <el-table-column label="所属模块" prop="module" width="150"></el-table-column>
        <el-table-column label="用例描述" prop="des"></el-table-column>
        <el-table-column label="责任人" prop="user" width="150" align="center"></el-table-column>
        <el-table-column label="操作" align="center" width="150">
          <template slot-scope="scope">
            <el-button type="text" size="mini" @click="importCase(scope.row.id)" style="margin-right: 10px">引用
            </el-button>
            <router-link :to="'/case_detail?project_id='+project_id+'&case_id='+scope.row.id" target="_blank"
                         style="margin-right: 10px">
              <el-button type="text" size="mini">编辑</el-button>
            </router-link>
          </template>
        </el-table-column>
      </template>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15]"
        :page-size="this.queryFields.PageSize"
        layout="total, prev, pager, next, jumper, sizes"
        @current-change="handleCurrentChange"
        :total="caseTotal">
    </el-pagination>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CaseImportList",
  watch: {
    showCaseVisible: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal === true) {
          this.getCases()
        }
      },
    },
  },
  methods: {
    handleCurrentChange(page){
      this.queryFields.Page = page
      this.getCases()
    },
    getCases() {
      axios({
        method: 'get',
        url: '/testcase_list',
        params: {
          project_id: this.project_id,
          caseName: this.queryFields.caseName,
          case_type: 1,
          Page: this.queryFields.Page,
          PageSize: this.queryFields.PageSize,
          version_id:this.version_id
        }
      }).then(res => {
        this.caseList = res.data.data
        this.caseTotal = res.data.total
      })
    },
    importCase(id) {
      this.$emit('toParent', id)
    },
  },
  data() {
    return {
      queryFields: {user: '', caseName: '', moduleId: '', project_id: this.project_id, Page: 1, PageSize: 15},
      caseList: [],
      caseTotal: 0
    }
  },
  props: ['project_id', 'showCaseVisible','case_type', 'version_id']
}
</script>

<style scoped>
.el-table /deep/ *{
  font-size: 14px !important;
}

</style>