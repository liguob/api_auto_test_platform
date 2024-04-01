<template>
  <div>
    <el-container style="height: 100%">
      <el-aside style="width: 210px;height: 100%">
        <Menu></Menu>
      </el-aside>
      <el-container style="border-left: 1px black">
        <el-main style="padding: 5px 10px">
          <HeadName :name="'个人资料'"></HeadName>
          <div>
            <template>
              <el-form :model="user_detail">
                <el-form-item label="姓名" :label-width="formLabelWidth">
                  <el-input v-model="user_detail.name"></el-input>
                </el-form-item>
                <el-form-item label="职位" :label-width="formLabelWidth">
                  <el-input v-model="user_detail.title"></el-input>
                </el-form-item>
                <el-form-item label="昵称" :label-width="formLabelWidth">
                  <el-input v-model="user_detail.nickname"></el-input>
                </el-form-item>
                <el-form-item label="自我介绍" :label-width="formLabelWidth">
                  <el-input v-model="user_detail.self_introduce" type="textarea" rows="3" style="width: 300px"></el-input>
                </el-form-item>
                <el-button type="primary">保存</el-button>
              </el-form>
            </template>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import HeadName from "@/components/HeadName.vue";

export default {
  name: "UserDetail",
  components: {
    Menu,
    HeadName
  },
  data(){
    return {
      user_detail:{
        name:'',
        username:'',
        nickname:'',
        title:'',
        self_introduce:'',
        picture:'',
      },
      formLabelWidth:'80px'
    }
  },
}
</script>

<style scoped>
.el-input{
  width: 300px;
}

</style>