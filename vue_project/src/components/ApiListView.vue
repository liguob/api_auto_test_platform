<template>
  <div>
    <div style="float: right;margin-bottom: 5px">
      <el-form @submit.native.prevent>
        <el-input placeholder="请输入接口名称或路径" v-model="queryFields.search_key" style="width: 300px">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-button type="primary" @click="Search_api" native-type="submit">查询</el-button>
      </el-form>
    </div>
    <el-table
        :data="ApisListData"
        border style="width: 100%"
        :highlight-current-row="true"
        height="600"
        size="mini">
      <el-table-column type="index" label="序号" width="80"></el-table-column>
      <el-table-column label="接口名称" prop="label" width="200"></el-table-column>
      <el-table-column label="请求方法" prop="method" width="80">
        <template slot-scope="scope">
          <el-tag>{{ scope.row.method }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="路径" prop="path" width="200"></el-table-column>
      <el-table-column label="描述" prop="des"></el-table-column>
      <el-table-column label="操作" width="120" align="center">
        <template slot-scope="scope">
          <el-button type="text" @click="useApi(scope.row)">引用</el-button>
          <el-button type="text" @click="openEditApi(scope.row.id)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        style="float: right"
        background
        :page-sizes="[15]"
        :page-size="queryFields.PageSize"
        layout="total, prev, pager, next, jumper, sizes"
        :total="apiCount">
    </el-pagination>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ApiListView",
  props: ['showApiList'],
  data() {
    return {
      selectId: '',
      ApisListData: [],
      queryFields: {search_key: '', Page: 1, PageSize: 15},
      apiCount: 0,
      checkedGh: '',
    }
  },
  watch: {
    showApiList: {
      handler(newValue, oldValue) {
        if (newValue === true) {
          this.Search_api()
        }
      },
      immediate: true
    },
  },
  methods: {
    openEditApi(id) {
      const routeData = this.$router.resolve({name: 'api_edit', query: {id: id}})
      window.open(routeData.href, '_blank')
    },
    useApi(data) {
      delete data.id
      delete data.des
      this.$emit('toParent', data)
    },
    Search_api() {
      axios.get('/api_list',
          {params: this.queryFields}
      ).then(res => {
        this.ApisListData = res.data.data
        this.apiCount = res.data.count
      })
    },
  },
}
</script>

<style scoped>
.el-table /deep/ * {
  font-size: 14px !important;
}
</style>