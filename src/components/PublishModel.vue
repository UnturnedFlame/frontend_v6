/** * 组件名称: PublishModel * 功能描述:
该组件用于发布模型，允许用户上传模型文件、填写模型相关信息，并提交发布请求。 * 主要功能: *
- 提供文件上传功能，支持特定格式的模型文件。 * -
包含表单用于填写模型的详细信息，如名称、描述等。 * -
提交按钮用于将模型信息和文件发送到服务器进行发布。 */

<template>
  <div>
    <div
    >
      <a-button class="private-algorithm-button" ghost @click="openPublishModelPanel">
        <i class="fa-solid fa-screwdriver-wrench" style="margin-right: 3px;"></i>
        <span style="font-family: 'Microsoft YaHei'">模型管理</span>
      </a-button>
      
        <!-- <a-button v-if="props.userRole === 'superuser'" @click="openPublishModelPanel" >
          <span style="font-family: 'Microsoft YaHei';">模型管理</span>
        </a-button> -->
      <!-- <a-button v-if="props.userRole === 'superuser'" @click="fetchModels" >
          <span style="font-family: 'JetBrains Mono', monospace;width:100%">打开模型库</span>
      </a-button> -->
     
      
      <!-- <div
        class="highlight"
        :style="{ bottom: '15px', color: getColor(modelLoaded) }"
        :title="modelLoaded"
      >
        <p>已加载模型</p>
        {{ modelLoaded }}
      </div> -->
      <!-- <div v-if="props.userRole === 'superuser'" @click="openPublishModelPanel"
        >模型管理</div> -->
      <!-- <div
        class="highlight"
        :style="{ bottom: '15px', color: getColor(modelLoaded) }"
        :title="modelLoaded"
      >
        <p>已加载模型</p>
        {{ modelLoaded }}
      </div> -->
    </div>

    <!-- 开发者用户发布已保存的模型 -->
    <el-dialog
      v-model="publishModelPanelVisible"
      :close-on-press-escape="false"
      :close-on-click-modal="false"
    >
      <div
        style="padding: 5px; display: flex; justify-content: left; align-items: center"
      >
        <p style="font-size: 26px; font-weight: bold">模型管理</p>
      </div>
      <div style="height: 1px; background-color: #d3d3d3; margin: 10px 0"></div>
      <el-table :data="fetchedModelsInfo" height="500" stripe border style="width: 100%" empty-text="暂无模型">
        <el-table-column :width="100" property="author" label="模型作者" />
        <el-table-column
          :width="200"
          property="model_name"
          label="模型名称"
          show-overflow-tooltip
        />
        <el-table-column
          
          property="description"
          label="模型描述"
          show-overflow-tooltip
        />
        <el-table-column
          
          property="isPublish"
          label="是否发布"
          show-overflow-tooltip
        />

        <el-table-column :width="350" label="操作">
          <template #default="scope">
           
            <!-- 删除已保存的模型 -->
            <el-popconfirm
              title="确定要删除该模型吗？"
              @confirm="deleteModelConfirm(scope.$index, scope.row)"
            >
              <template #reference>
                <el-button
                  size="small"
                  type="danger"
                  style="width: 90px;"
                  >删除</el-button
                >
              </template>

              <template #actions="{ confirm, cancel }">
                <el-row>
                  <el-col :span="12"
                    ><el-button size="small" @click="cancel">取消</el-button></el-col
                  >
                  <el-col :span="12">
                    <el-button type="primary" size="small" @click="confirm">
                      确定
                    </el-button>
                  </el-col>
                </el-row>
              </template>
            </el-popconfirm>
           
            <!-- 查看模型信息 -->
            <el-popover placement="bottom" :width="500" trigger="focus">
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
                  style="width: 90px"
                  @click="showModelInfo(scope.row)"
                >
                  查看模型
                </el-button>
              </template>
            </el-popover>

            <!-- 发布模型 -->
            <el-popconfirm
              :title="scope.row.isPublish == '已发布' ? '是否取消发布该模型？' : '是否发布该模型？'"
              @confirm="publishModelConfirm(scope.$index, scope.row)"
            >
              <template #reference>
                <el-button
                  size="small"
                  :type="scope.row.isPublish == '未发布' ? 'success' : 'warning'"
                  v-if="scope.row.isPublish === '未发布'"
                  style="width: 90px;"
                  >{{scope.row.isPublish == '未发布' ? '申请发布' : '取消发布'}}</el-button
                >
              </template>

              <template #actions="{ confirm, cancel }">
                <el-row>
                  <el-col :span="12"
                    ><el-button size="small" @click="cancel">取消</el-button></el-col
                  >
                  <el-col :span="12">
                    <el-button type="primary" size="small" @click="confirm">
                      确定
                    </el-button>
                  </el-col>
                </el-row>
              </template>
            </el-popconfirm>

          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 以抽屉的形式打开开发者用户已发布的模型 -->
    <el-drawer v-model="modelsDrawer" direction="ltr" size="35%">
      <div style="display: flex; flex-direction: column">
        <el-col>
          <h2 style="margin-bottom: 25px; color: #253b45">系统模型库</h2>
          <span style="font-size: 15px; color: #a1a2b1"
            >*当前用户权限为{{
              userRole === "user"
                ? "普通用户，可以使用系统中的模型"
                : "系统用户，可以添加模型和删除本用户添加的模型"
            }}</span
          >
          <el-table :data="fetchedModelsInfo" height="500" stripe style="width: 100%">
            <el-table-column :width="100" property="author" label="模型作者" />
            <el-table-column
              property="model_name"
              label="模型名称"
              show-overflow-tooltip
            />
            <el-table-column
              property="description"
              label="模型描述"
              show-overflow-tooltip
            />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button
                  size="small"
                  type="primary"
                  style="width: 50px"
                  @click="loadModel(scope.row)"
                >
                  使用
                </el-button>
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
        </el-col>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ElMessage, ElMessageBox } from "element-plus";
import { onMounted, ref } from "vue";
import api from "../utils/api.js";
import { useRouter } from "vue-router";
import { labelsForAlgorithms } from "./constant.js";

const publishModelPanelVisible = ref(false);
// 从后端获取到的历史模型的信息
const fetchedModelsInfo = ref<modelInfo[]>([]);
const openPublishModelPanel = () => {
  publishModelPanelVisible.value = true;
  fetchModelInfoFromDatabase();
};

// 从父组件userPLatform.vue传来的用户权限信息
const props = defineProps({
  userRole: String,
});

// 删除模型确认
const deleteModelConfirmVisible = ref(false);
const router = useRouter();
// let index = 0
// let row = 0
// 删除模型操作
// const deleteModel = (indexIn, rowIn) => {
//   index = indexIn
//   row = rowIn
//   deleteModelConfirmVisible.value = true
// }
const emit = defineEmits(["resetModel", "loadModel"]);
interface modelInfo {
  id: number;
  model_name: string;
  description: string;
  author: string;
  model_info: any;
  isPublish: string;
}

// 查看模型的具体信息，按如下方式构造信息卡片
const modelName = ref("");
const modelAlgorithms = ref([]);
const modelParams = ref([]); // {'模块名': xx, '算法': xx, '参数': xx}

const showModelInfo = (row: modelInfo) => {
  let objects = JSON.parse(row.model_info);
  let nodesList = objects.nodeList; // 模型节点信息
  let connection = objects.connection; // 模型连接顺序

  modelName.value = row.model_name;
  modelAlgorithms.value = connection;
  modelParams.value.length = 0;
  nodesList.forEach((element) => {
    let item = { 模块名: "", 算法: "" };
    item.模块名 = element.label;
    item.算法 = labelsForAlgorithms[element.use_algorithm];
    modelParams.value.push(item);
  });
};
// 用户删除模型操作确认
const deleteModelConfirm = (index: number, row: modelInfo) => {
  // 发送删除请求到后端，row 是要删除的数据行
  api
    .get("/user/delete_model/?row_id=" + row.id)
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      }
      if (response.data.code == 200) {
        // 如果被删除的模型已经被加载，则需要取消加载
        emit("resetModel", row.model_name);

        if (index !== -1) {
          // 删除前端表中数据
          fetchedModelsInfo.value.splice(index, 1);
          deleteModelConfirmVisible.value = false;
          ElMessage({
            message: "删除模型成功",
            type: "success",
          });
        }
      } else {
        if (response.data.code == 404) {
          ElMessage({
            message: "没有权限删除该模型",
            type: "error",
          });
        } else {
          ElMessage({
            message: "删除模型失败，请稍后重试",
            type: "error",
          });
        }
      }
    })
    .catch((error: any) => {
      // 处理错误
      console.error(error);
      ElMessage({
        message: "删除模型失败," + error,
        type: "error",
      });
    });
};

const modelLoaded = ref("无");

// 点击子组件的加载模型，加载模型并到父组件userPlatForm.vue显示出来
const loadModel = (row: modelInfo) => {
  modelLoaded.value = row.model_name;
  emit("loadModel", row);
};

onMounted(() => {
  fetchModelInfoFromDatabase();
});

// 从数据库获取模型信息
const fetchModelInfoFromDatabase = () => {
  //   dataDrawer.value = false; // 打开历史模型抽屉

  // 向后端发送请求获取用户的历史模型
  api
    .get("user/fetch_models/")
    .then((response: any) => {
      if (response.data.code === 200) {
        // modelsDrawer.value = true;
        let modelsInfo = response.data.models;
        fetchedModelsInfo.value = [];
        for (let item of modelsInfo) {
          fetchedModelsInfo.value.push(item);
        }
      }
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      }
    })
    .catch((error: any) => {
      ElMessage({
        message: "获取历史模型失败," + error,
        type: "error",
      });
    });
};

// 打开抽屉，同时从后端获取历史模型
const modelsDrawer = ref(false);
const fetchModels = () => {
  //   dataDrawer.value = false  // 打开历史模型抽屉

  // 向后端发送请求获取用户的历史模型
  api
    .get("/user/fetch_models_published/")
    .then((response: any) => {
      if (response.data.code == 200) {
        modelsDrawer.value = true;
        let modelsInfo = response.data.models;
        fetchedModelsInfo.value = [];
        for (let item of modelsInfo) {
          fetchedModelsInfo.value.push(item);
        }
      }
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      }
    })
    .catch((error: any) => {
      ElMessage({
        message: "获取历史模型失败," + error,
        type: "error",
      });
    });
};

// 申请发布模型
const publishModelConfirm = (index: number, row: modelInfo) => {
    let modelId = row.id
    let formData = new FormData()
    formData.append('modelId', String(modelId))
    api.post('user/publish_model/', formData)
    .then((response: any) => {
        if (response.data.code === 200){
            ElMessage({
                message: response.data.message,
                type: 'success'
            })
            // 刷新发布模型数据列表
            fetchModelInfoFromDatabase()
        }else{
            ElMessage({
                message: '发布失败，'+response.data.message
            })
        }
    })
    .catch(()=>{
        ElMessage({
            message: '模型发布失败，请重试',
            type: 'error'
        })
    })

}

// 已加载模型和已加载数据字体颜色更改
const getColor = (value: string) => {
  if (value == "无") {
    return "red";
  } else {
    return "green";
  }
};
</script>

<style scoped>
.private-algorithm-button {
  background-color: #ffffff;
  color: #333333;
  font-size: 16px;
  width: 100%;
  height: 100%;
  margin: 0;
  border-radius: 0;
}


</style>
