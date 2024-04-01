<template>
  <div>
    <el-tabs v-model="activeTab">
      <el-tab-pane name="first">
        <span slot="label" style="font-size: 20px">JSONPATH</span>
        <el-form style="margin-bottom: 5px" @submit.native.prevent>
          <el-form-item label-width="80">
            <template slot="label">
              <el-button style="width: 150px" type="primary" @click="getJsonPath" native-type="submit">JSONPATH查询
              </el-button>
            </template>
            <el-input placeholder="请输入jsonpath表达式" style="width: calc(100% - 150px)"
                      v-model="jsonPathExp"></el-input>
          </el-form-item>
          <el-form-item>
            <el-row>
              <el-col :span="12">
                <span style="text-align: center">输入json</span>
                <b-code-editor :theme="'material'" :auto-format="false" v-model="jsonData"
                               class="code_edit"></b-code-editor>
              </el-col>
              <el-col :span="12">
                <span style="text-align: center">输出结果</span>
                <b-code-editor :theme="'material'" :auto-format="false" v-model="jsonPathRes" class="code_edit"
                               :readonly="true"></b-code-editor>
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>

</template>

<script>
import Menu from "@/components/Menu.vue";
import JSONPath from 'JSONPath'
import axios from "axios";

export default {
  name: "PracticeManage",
  components: {Menu},
  created() {
    this.jsonData = JSON.stringify(JSON.parse(this.jsonData), null, 2)
  },
  mounted() {
    this.getJsonPath()
  },
  data() {
    return {
      resInit: '[]',
      jsonData: '{"title":"练习json数据","children":[{"name":"子项名称", "desc":"子项说明" },{"name":"子项名称1", "desc":"子项说明1" }]}',
      jsonPathExp: '$.children[:1][name]',
      jsonPathRes: '[]',
      activeTab: 'first',
    }
  },
  methods: {
    getJsonPath() {
      axios({
        method: 'post',
        url: 'get_jsonpath',
        data: {data: JSON.parse(this.jsonData), express: this.jsonPathExp}
      }).then(res => {
              try {
        this.jsonPathRes = JSON.stringify(res.data.data, null, 2)
      } catch (e) {
        this.jsonPathRes = '[]'
      }
      })
    },
    // CalJsonPath() {
    //   try {
    //     this.jsonPathRes = JSON.stringify(JSONPath({json: JSON.parse(this.jsonData), path: this.jsonPathExp}), null, 2)
    //   } catch (e) {
    //     this.jsonPathRes = '[]'
    //   }
    // }
  }
}
</script>
<style scoped>

.code_edit {
  font-size: 13px;
  line-height: 13px !important;
  height: 600px !important;
}

.el-form /deep/ .el-form-item__label {
  padding: 0 0 0 0 !important;
}

/*//.my-awesome-json-theme {*/
/*//  overflow-x: auto;*/
/*//  overflow-y: auto;*/
/*//  background: black;*/
/*//  white-space: nowrap;*/
/*//  color: #01fef4;*/
/*//  font-size: 14px;*/
/*//  height: 850px;*/
/*//  font-family: Consolas, Menlo, Courier, monospace;*/
/*//*/
/*//  .jv-ellipsis {*/
/*//    color: rgb(237, 13, 13);*/
/*//    background-color: rgb(241, 11, 11);*/
/*//    display: inline-block;*/
/*//    line-height: 0.9;*/
/*//    font-size: 0.9em;*/
/*//    padding: 0 4px 2px 4px;*/
/*//    border-radius: 3px;*/
/*//    vertical-align: 2px;*/
/*//    cursor: pointer;*/
/*//    user-select: none;*/
/*//  }*/
/*//*/
/*//  .jv-button {*/
/*//    color: #49b3ff;*/
/*//  }*/
/*//*/
/*//  ::v-deep .jv-key {*/
/*//    color: #67C23A !important;*/
/*//  }*/
/*//*/
/*//  ::v-deep .jv-push {*/
/*//    color: #c4a000;*/
/*//  }*/
/*//*/
/*//  .jv-item {*/
/*//    &.jv-array {*/
/*//      color: #111111;*/
/*//    }*/
/*//*/
/*//    &.jv-boolean {*/
/*//      color: #fc1e70;*/
/*//    }*/
/*//*/
/*//    &.jv-function {*/
/*//      color: #067bca;*/
/*//    }*/
/*//*/
/*//    &.jv-number {*/
/*//      color: #fc1e70;*/
/*//    }*/
/*//*/
/*//    &.jv-number-float {*/
/*//      color: #fc1e70;*/
/*//    }*/
/*//*/
/*//    &.jv-number-integer {*/
/*//      color: #fc1e70;*/
/*//    }*/
/*//*/
/*//    &.jv-object {*/
/*//      color: #111111;*/
/*//    }*/
/*//*/
/*//    &.jv-undefined {*/
/*//      color: #e08331;*/
/*//    }*/
/*//*/
/*//    &.jv-string {*/
/*//      color: #42b983;*/
/*//      word-break: break-word;*/
/*//      white-space: normal;*/
/*//    }*/
/*//  }*/
/*//*/
/*//  .jv-code {*/
/*//    ::v-deep .jv-toggle {*/
/*//      color: #067bca !important;*/
/*//*/
/*//      &:before {*/
/*//        padding: 0 2px;*/
/*//        border-radius: 2px;*/
/*//      }*/
/*//*/
/*//      &:hover {*/
/*//        &:before {*/
/*//          background: rgb(242, 5, 5);*/
/*//        }*/
/*//      }*/
/*//    }*/
/*//  }*/
/*//}*/

</style>