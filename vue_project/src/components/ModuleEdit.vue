<template>
  <div>
    <el-button type="primary" @click="clickAdd">新增模块</el-button>
    <el-tree :data="module_data" :props="defaultProps" :render-content="renderContent"
             :expand-on-click-node="false"></el-tree>
    <el-dialog title="模块信息" :visible.sync="active" append-to-body>
      <el-divider content-position="left" v-if="parent_module_path !== ''">
        当前节点：{{ parent_module_path.replaceAll('/', '>') }}
      </el-divider>
      <el-divider content-position="left" v-else="parent_module">根节点</el-divider>
      <el-form v-model="module_detail" label-width="100px">
        <el-form-item label="模块名称">
          <el-input placeholder="请输入模块名称" v-model="module_detail.module_name" style="width: 600px"></el-input>
        </el-form-item>
        <el-form-item label="优先级">
          <el-input placeholder="请输入优先级：整数" v-model="module_detail.priority" style="width: 600px"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="active = false">取 消</el-button>
        <el-button type="primary" @click="addModule()">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
        title="提示"
        :visible.sync="activeTip"
        width="30%"
        append-to-body
    >
      <span>是否删除模块？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="activeTip = false">取 消</el-button>
        <el-button type="primary" @click="removeModule">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "moduleEdit",
  props: ["module_data", "project_id"],
  data() {
    return {
      action: '',
      parent_module_id: '',
      parent_module_path: '',
      module_detail: {},
      active: false,
      activeTip: false,
      defaultProps: {
        children: 'children',
        label: 'module_name'
      },
    }
  },
  methods: {
    renderContent(h, {node, data, store}) {
      return (
          <span class="custom-tree-node"
                style="font-size: 14px;display: flex;flex: 1;justify-content: space-between;align-items: center">
            <span>{node.label}</span>
            <span>
              <el-button size="mini" type="text" on-click={() => this.clickAdd(node, data)}>新增</el-button>
              <el-button size="mini" type="text" on-click={() => this.clickEdit(node, data)}>修改</el-button>
              <el-button size="mini" type="text" on-click={() => this.clickRemove(node, data)}>删除</el-button>
            </span>
          </span>);
    },
    clickAdd(node = '', data = '') {
      this.active = true
      this.module_detail = {}
      if (data) {
        // 非根节点新增
        this.parent_module_path = data.module_path
        this.parent_module_id = data.id
      } else {
        // 根节点新增
        this.parent_module_path = ''
        this.parent_module_id = ''
      }
    },
    clickEdit(node, data) {
      this.active = true
      const parent = node.parent
      this.parent_module_path = parent.data.module_path ? parent.data.module_path : ''
      this.parent_module_id = parent.data.id ? parent.data.id : ''
      this.module_detail = {id: data.id, module_name: data.module_name, priority: data.priority}
    },
    clickRemove(node, data) {
      this.activeTip = true
      this.action = 'del'
      const parent = node.parent
      this.parent_module_path = parent.data.module_path ? parent.data.module_path : ''
      this.parent_module_id = parent.data.id ? parent.data.id : ''
      this.module_detail = {id: data.id, module_name: data.module_name, priority: data.priority}
    },
    addModule() {
      this.action = 'edit'
      if (this.parent_module) {
        // 非根节点保存
        this.module_detail.module_path = this.parent_module.module_path + '/' + this.module_detail.module_name
      } else {
        // 根节点保存
        this.module_detail.module_path = '/' + this.module_detail.module_name
      }
      this.editModule()
    },
    removeModule() {
      this.action = 'del'
      this.editModule()
      this.activeTip = false
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
    editModule() {
      this.module_detail.project_id = this.project_id
      axios({
        params: {action: this.action, parent_module: this.parent_module_id},
        url: '/edit_module',
        method: 'post',
        data: this.module_detail,
      }).then(res => {
        this.$message({message: res.data.message, type: res.data.type})
        if (res.data.message === '成功') {
          this.moduleTree()
          this.active = false
        }
      })
    }
  },
}
</script>

<style scoped>
#api_tree /deep/ span {
  font-size: 14px !important;
}

</style>