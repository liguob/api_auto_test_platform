<template>
  <div class="project_list" style="height: 100%">
    <el-container style="height: 100%">
      <el-aside style="width: 210px;background: white">
        <Menu></Menu>
      </el-aside>
      <el-container style="border-left: 1px black">
        <el-main style="padding: 5px 10px">
          <HeadName :name="'环境管理'"></HeadName>
          <div>
            <template>
              <el-table :data="env_list" border style="width: 100%" :highlight-current-row="true">
                <el-table-column label="环境名称" prop="name" width="300"></el-table-column>
                <el-table-column label="标签" prop="tag_type" width="250">
                  <template slot-scope="scope">
                    <el-tag>{{ scope.row.tag_type }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="描述" prop="desc"></el-table-column>
                <el-table-column width="200" align="center">
                  <template slot="header">
                    <el-button type="primary" @click="Open_new_env">新增环境</el-button>
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" @click="Delete_env(scope.row.id)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </div>
        </el-main>
      </el-container>
    </el-container>
    <el-dialog title="环境信息" :visible.sync="dialogFormVisible" :destroy-on-close="true">
      <el-form :model="env_data">
        <el-form-item label="名称" :label-width="formLabelWidth">
          <el-input v-model="env_data.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="标签" :label-width="formLabelWidth">
          <el-input v-model="env_data.tag_type"></el-input>
        </el-form-item>
        <el-form-item label="描述" :label-width="formLabelWidth">
          <el-input v-model="env_data.desc" type="textarea" :rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="Add_env">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import axios from "axios";
import HeadName from "@/components/HeadName.vue";

export default {
  name: "EnvManage",
  components: {
    HeadName,
    Menu
  },
  data() {
    return {
      env_list: [],
      env_data: {
        name: '',
        tag_type: '',
        desc: '',
      },
      formLabelWidth: '100px',
      dialogFormVisible: false,
      activeName: 'first',
    };
  },
  methods: {
    Open_new_env() {
      this.env_data = this.$options.data().env_data;
      this.dialogFormVisible = true;
    },
    Add_env() {
      axios({
        method: 'post',
        url: '/env_add/',
        data: this.env_data,
      }).then(res => {
        this.env_list = res.data;
        this.$message({message: '成功', type: "success"});
        this.dialogFormVisible = false;
      })
    },
    Delete_env(id) {
      axios({
        method: "post",
        url: '/env_delete/',
        data: {
          id: id
        }
      }).then(res => {
        this.$message({message: '成功', type: "success"});
        this.env_list = res.data;
      })
    }
  },
  mounted() {
    axios.get('/env_list/', {}).then(
        res => {
          this.env_list = res.data;
        })
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

.project_table el-table-column {
  align-items: center;
}

.search .el-input {
  width: 250px;
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>