<template>
  <div>
    <el-container style="height: 100%">
      <el-aside style="height: 100%; width: 210px">
        <Menu></Menu>
      </el-aside>
      <el-container>
        <el-main>
          <HeadName :name="'发布公告'"></HeadName>
          <template>
            <el-table :data="notice_list" :highlight-current-row="true" border>
              <el-table-column prop="create_date" label="创建日期" width="150"></el-table-column>
              <el-table-column prop="expiration_date" label="到期日期" width="150"></el-table-column>
              <el-table-column prop="content" label="公告内容"></el-table-column>
              <el-table-column width="150">
                <template slot="header">
                  <el-button type="text" size="mini" @click="openNew">新增</el-button>
                </template>
                <template slot-scope="scope">
                  <el-button type="text" size="mini" @click="deleteNotice(scope.row.notice_id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-main>
      </el-container>
    </el-container>
    <el-dialog :visible.sync="dialogFormVisible">
      <el-form :model="notice_data">
        <el-form-item label="公告信息" label-width="100px">
          <el-input v-model="notice_data.content" placeholder="请输入公告信息" type="textarea" rows="3"></el-input>
        </el-form-item>
        <el-form-item label="失效日期" label-width="100px">
          <template>
            <div class="block">
              <el-date-picker
                  value-format="yyyy-MM-dd"
                  v-model="notice_data.expiration_date"
                  type="date"
                  placeholder="选择日期">
              </el-date-picker>
            </div>
          </template>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addNotice()">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import HeadName from "@/components/HeadName.vue";
import axios from "axios";

export default {
  name: "PublicNotice",
  components: {
    Menu, HeadName,
  },
  data() {
    return {
      notice_list: [
        {
          content_id: 0,
          content: '',
          create_date: '',
          expiration_date: '',
        },
      ],
      notice_data: {
        content: '',
        expiration_date: '',
      },
      dialogFormVisible: false,
    }
  },
  methods: {
    openNew() {
      this.notice_data = this.$options.data().notice_data;
      this.dialogFormVisible = true;
    },
    publicNoticeList() {
      axios({
        url: '/public_notice_list/',
        method: 'get',
      }).then(res => {
        this.notice_list = res.data.data
      })
    },
    deleteNotice(content_id) {
      axios({
        method: 'get',
        url: '/public_notice_delete/',
        params: {
          notice_id: content_id
        }
      }).then(res => {
        this.notice_list = res.data.data;
        this.$message({message: res.data.message, type: "success"});
      })
    },
    addNotice() {
      axios({
        url: '/public_notice_add/',
        method: 'post',
        data: this.notice_data
      }).then(res => {
        this.notice_list = res.data.data;
        this.dialogFormVisible = false;
        this.$message({message: res.data.message, type: "success"});
      })
    },
  },
  mounted() {
    this.publicNoticeList();
  }
}
</script>

<style scoped>
.el-container {
  height: 100%;
}

.el-aside {
  height: 100%;
  width: 210px;
}

.el-main {
  padding: 5px 10px;
}

</style>