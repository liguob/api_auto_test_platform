<template>
  <div>
    <div style="line-height: 50px;float: right">
      <el-form @submit.native.prevent>
        <el-input placeholder="请输入接口名称或路径" v-model="queryFields.search_key" style="width: 300px">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-button type="primary" @click="Search_api" native-type="submit">查询</el-button>
        <el-button type="primary" @click="Open_new_api">新增接口</el-button>
      </el-form>
    </div>
    <el-table :data="api_list" border style="width: 100%" :highlight-current-row="true" height="750">
      <el-table-column label="序号" type="index" align="center" width="70"></el-table-column>
      <el-table-column label="接口名称" prop="label" width="200"></el-table-column>
      <el-table-column label="请求方法" prop="method" width="100">
        <template slot-scope="scope">
          <el-tag>{{ scope.row.method }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="路径" prop="path" width="400"></el-table-column>
      <el-table-column label="描述" prop="des"></el-table-column>
      <el-table-column label="操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="Open_edit_api(scope.row.id)">编辑</el-button>
          <el-button type="text" @click="clickDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15]"
        :page-size="this.queryFields.PageSize"
        layout="total, prev, pager, next, jumper, sizes"
        @current-change="handleCurrentChange"
        :total="apiCount">
    </el-pagination>
    <el-dialog
        title="提示"
        :visible.sync="dialogConfirmVisible"
        width="30%"
        :before-close="handleClose">
      <span>是否删除接口？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogConfirmVisible = false">取 消</el-button>
        <el-button type="primary" @click="Delete_api">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import HeadName from "@/components/HeadName.vue";
import axios from "axios";

export default {
  name: "ApiManage",
  components: {
    HeadName,
    Menu
  },
  data() {
    return {
      apiCount: 0,
      queryFields: {search_key: '', Page: 1, PageSize: 15},
      deleteId: '',
      api_list: [],
      dialogConfirmVisible: false,
      api_detail: {
        name: '',
        host: '',
        path: '',
        method: '',
        headers: '',
        params: '',
        payload: '',
        des: '',
      },
      method_options: [{
        value: 'get',
        label: 'get',
      }, {
        value: 'post',
        label: 'post',
      }, {
        value: 'delete',
        label: 'delete',
      }, {
        value: 'put',
        label: 'put',
      }],
      formLabelWidth: '120px',
    };
  },
  methods: {
    handleCurrentChange() {
    },
    handleClose(id) {
      this.dialogConfirmVisible = true;
      this.delete_case_id = id;
    },
    Open_new_api() {
      let routeData = this.$router.resolve({name: 'api_edit'})
      window.open(routeData.href, '_blank')
    },
    Open_edit_api(id) {
      let routeData = this.$router.resolve({name: 'api_edit', query: {id: id}})
      window.open(routeData.href, '_blank')
    },
    Search_api() {
      axios.get('/api_list',
          {params: this.queryFields}
      ).then(res => {
        this.api_list = res.data.data
        this.apiCount = res.data.count
      })
    },
    clickDelete(id) {
      this.dialogConfirmVisible = true
      this.deleteId = id
    },
    Delete_api() {
      axios('/api_delete', {params: {id: this.deleteId}}).then(res => {
        this.api_list = res.data.data
        this.$message({message: res.data.message, type: res.data.type})
        this.dialogConfirmVisible = false
        this.Search_api()
      })
    },
  },
  mounted() {
    this.Search_api();
  }
}
</script>

<style scoped>
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

.el-button + .el-button {
  margin-left: 5px;
}

.el-table * {
  font-size: 14px !important;
}
</style>