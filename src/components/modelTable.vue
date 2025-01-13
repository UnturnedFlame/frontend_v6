<template>
  <div style="display: flex; flex-direction: column">
    <div class="shadow-border title-container" style="">用户模型管理</div>

    <div class="roleManage">
      <div class="tableTool" style="position: relative; width: 100%; height: 30px">
        <div style="position: absolute; right: 12%; display: flex; flex-direction: row">
          <span style="display: flex; flex-direction: row; margin-right: 20px">
            <div style="display: flex; flex-direction: row; margin-right: 20px">
              <span
                style="
                  width: 100px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                "
                >选择关键字</span
              >
              <a-select style="width: 110px" v-model:value="keywordType">
                <a-select-option value="username">作者</a-select-option>
                <a-select-option value="modelname">模型名称</a-select-option>
              </a-select>
            </div>
            <a-input v-model:value="keyword" placeholder="按关键字搜索"></a-input>
            <a-button @click="search">搜索</a-button>
          </span>
        </div>
      </div>
    </div>

    <div class="table-container">
      <el-table
        :data="fetchedModelsInfo"
        stripe
        style="width: 100%"
        height="500px"
        :stripe="true"
        border
        empty-text="暂无数据"
        :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#606266' }"
      >
        <el-popover
          placement="bottom-start"
          title="模型信息"
          :width="400"
          trigger="hover"
          content="这是模型信息"
        >
        </el-popover>
        <!-- <el-table-column property="id" label="序号" /> -->
        <el-table-column property="model_name" label="模型名称" />
        <el-table-column property="author" label="作者" />
        <el-table-column property="jobNumber" label="工号" />

        <el-table-column label="操作">
          <template #default="scope">
            <el-button
              size="small"
              type="danger"
              style="width: 50px"
              @click="deleteModel(scope.$index, scope.row)"
            >
              删除
            </el-button>
            <template></template>
            <el-popover placement="bottom" :width="500" trigger="click">
              <el-descriptions :title="modelName" :column="3" direction="vertical">
                <el-descriptions-item label="使用模块" :span="3">
                  <el-tag size="small" v-for="algorithm in modelAlgorithms">{{
                    algorithm
                  }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="算法参数" :span="3">
                  <div v-for="item in modelParams">
                    {{ item.模块名 }}: {{ item.算法 }}
                  </div>
                </el-descriptions-item>
              </el-descriptions>
              <template #reference>
                <el-button
                  size="small"
                  type="info"
                  style="width: 80px"
                  @click="showModelInfo(scope.row)"
                >
                  查看模型
                </el-button>
              </template>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="deleteModelConfirmVisible" title="提示" width="500">
      <span style="font-size: 20px">确定删除该模型吗？</span>
      <template #footer>
        <el-button style="width: 150px" @click="deleteModelConfirmVisible = false"
          >取消</el-button
        >
        <el-button
          style="width: 150px; margin-right: 70px"
          type="primary"
          @click="deleteModelConfirm"
          >确定</el-button
        >
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
import api from "../utils/api.js";
import { labelsForAlgorithms } from "./constant.ts";
import { ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";

// 按关键字搜索模型
const keyword = ref("");
const keywordType = ref("username");

const search = () => {
  api
    .get(
      "administration/search_model/?keywords=" +
        keyword.value +
        "&keywordType=" +
        keywordType.value
    )
    .then((response) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: (action) => {
            router.push("/");
          },
        });
      } else if (response.data.code == 200) {
        fetchedModelsInfo.value.length = 0;
        for (let item of response.data.result) {
          fetchedModelsInfo.value.push(item);
        }
      }
    })
    .catch((error) => {
      message.error("搜索失败，请重试");
    });
};

const fetchedModelsInfo = ref([]);

const router = useRouter();

onMounted(() => {
  fetchModels();
});

// 获取用户模型
const fetchModels = () => {
  // let url = 'http://127.0.0.1:8000/administration/fetch_users_models/'
  api
    .get("/administration/fetch_users_models/")
    .then((response) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: (action) => {
            router.push("/");
          },
        });
      } else {
        let modelsInfo = response.data;
        fetchedModelsInfo.value.length = 0;
        for (let item of modelsInfo) {
          fetchedModelsInfo.value.push(item);
        }
      }
    })
    .catch((error) => {
      ElMessage.error("获取用户模型信息失败，请稍后重试");
    });
};

let index = 0;
let row = 0;
const deleteModelConfirmVisible = ref(false);
const deleteModel = (indexIn, rowIn) => {
  index = indexIn;
  row = rowIn;
  deleteModelConfirmVisible.value = true;
};

// 查看模型信息
const modelName = ref("");
const modelAlgorithms = ref([]);
const modelParams = ref([]); // {'模块名': xx, '算法': xx, '参数': xx}

const showModelInfo = (row) => {
  let objects = JSON.parse(row.model_info);
  console.log("showModelInfo objects: ", objects)
  let node_list = objects.nodeList.nodes; // 模型节点信息
  console.log("------", node_list)
  let connection = objects.modelConfig.modules; // 模型连接顺序

  modelName.value = row.model_name;
  modelAlgorithms.value = connection;
  modelParams.value.length = 0;
  node_list.forEach((node) => {
    let item = { 模块名: "", 算法: "" };
    item.模块名 = node.nodeInfo.label;
    item.算法 = labelsForAlgorithms[node.nodeInfo.use_algorithm];
    modelParams.value.push(item);
  });
};

// 删除用户模型
const deleteModelConfirm = () => {
  // 发送删除请求到后端，row 是要删除的数据行
  api
    .get("/administration/delete_user_model/?row_id=" + row.id)
    .then((response) => {
      if (response.data.message === "delete user model success") {
        if (index !== -1) {
          // 删除前端表中数据
          fetchedModelsInfo.value.splice(index, 1);
          deleteModelConfirmVisible.value = false;
          ElMessage({
            message: "模型删除成功",
            type: "success",
          });
        }
      }
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: (action) => {
            router.push("/");
          },
        });
      }
    })
    .catch((error) => {
      // 处理错误
      ElMessage({
        message: "删除失败，请稍后重试",
        type: "error",
      });
      console.error(error);
    });
};
</script>

<style scoped>
.shadow-border {
  width: 200px;
  height: 200px;
  /* border: 1px solid #888; */
  box-shadow: 4px 4px 8px 0 rgba(136, 136, 136, 0.5); /* 水平偏移, 垂直偏移, 模糊距离, 扩展距离, 颜色 */
}

.title-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  width: 89%;
  height: 100px;
  font-weight: 8px;
  font-size: 30px;
  margin-bottom: 10px;
  margin-left: 10px;
  margin-top: 20px;
  padding-left: 20px;
  border-radius: 5px;
  font-family: "微软雅黑", sans-serif;
}

.table-container {
  width: 86%;
  height: 510px;
  padding: 20px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin-left: 30px;
}

.roleManage {
  .tableTool {
    padding: 10px 0;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }
  :deep(.el-table thead .el-table__cell) {
    text-align: center;
  }
}
</style>
