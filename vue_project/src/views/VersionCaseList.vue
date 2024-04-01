<template>
  <div style="height: 100%">
    <el-tabs v-model="active_name">
      <el-tab-pane name="基本用例">
        <span slot="label" style="font-size: 20px">基本用例</span>
        <ProjectCaseList :project_id="$route.query.project_id" :case_type="1"
                         :version_id="$route.query.version_id"></ProjectCaseList>
      </el-tab-pane>
      <el-tab-pane name="前置用例">
        <span slot="label" style="font-size: 20px">前置用例</span>
        <ProjectCaseList :project_id="$route.query.project_id" :case_type="2"
                         :version_id="$route.query.version_id"></ProjectCaseList>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import Menu from "@/components/Menu.vue";
import ProjectCaseList from "@/components/ProjectCaseList.vue";

export default {
  name: "version_case_list",
  components: {
    Menu, ProjectCaseList
  },
  data() {
    return {
      active_name: '基本用例',
    }
  }
}
</script>

<style scoped>

</style>