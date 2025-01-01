// 管理系统用户上传的增值服务组件
<template>
  <a-button class="private-algorithm-button" ghost @click="showExtraModules">
    <i class="fa-solid fa-screwdriver-wrench" style="margin-right: 3px;"></i>
    <span style="font-family: 'Microsoft YaHei';">管理组件</span>
  </a-button>
  <!-- 管理增值服务组件的弹窗 -->
  <a-modal
      v-model:open="dialogVisible"
      :ok-button-props="{ style: { display: 'none' } }"
      :cancel-button-props="{ style: { display: 'none' } }"
      title="管理增值服务组件"
      width="800px"
  >
    <div style="display: flex; flex-direction: row; font-family: 'Microsoft YaHei';">
      <el-input v-model="searchKeyword" placeholder="输入组件名称" style="width: 200px; margin-right: 15px" />
      <el-button type="primary" :icon="Search" style="width: 100px" @click="searchExtraAlgorithm(searchKeyword)">搜索</el-button>
    </div>
    <el-table :data="fetchedExtraAlgorithm" height="500" stripe>
      <!-- <el-table-column :width="100" property="author" label="模型作者" /> -->
      <el-table-column
          property="algorithmType"
          label="组件类型"
          show-overflow-tooltip
      />
      <el-table-column
          
          property="alias"
          label="组件名称"
          show-overflow-tooltip
      />
      <el-table-column
          width="200"
          property="statement"
          label="组件描述"
          show-overflow-tooltip
      />
      <el-table-column
          
          property="algorithmName"
          label="组件源文件"
          show-overflow-tooltip
      />

      <el-table-column :width="100" label="操作">
        <template #default="scope">
          <!-- <el-button size="small" type="primary" style="width: 50px;" @click="useModel(scope.row)">
              使用
            </el-button> -->
          <el-popconfirm title="你确定要删除该增值服务组件吗" @confirm="deleteExtraModule(scope.$index, scope.row)">
            <template #reference>
              <el-button
                  size="small"
                  type="danger"
                  style="width: 50px"
              >
                删除组件
              </el-button>
            </template>
            <template #actions="{ confirm, cancel }">
              <el-row>
                <el-col :span="12">
                  <el-button size="small" @click="cancel">取消</el-button>
                </el-col>
                <el-col :span="12">
                  <el-button
                      type="primary"
                      size="small"
                      @click="confirm"
                  >
                    确定
                  </el-button>
                </el-col>
              </el-row>
            </template>
          </el-popconfirm>
          <!-- <el-popover placement="bottom" :width='500' trigger="click">
              <el-descriptions :title="modelName" :column="3" direction="vertical"
              >
                <el-descriptions-item label="使用模块" :span="3">
                  <el-tag size="small" v-for="algorithm in modelAlgorithms">{{ algorithm }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="算法参数" :span="3">
                  <div v-for="item in modelParams">{{ item.模块名 }}: {{ item.算法 }}</div>
                </el-descriptions-item>
              </el-descriptions>
              <template #reference>
                <el-button size="small" type="info" style="width: 80px" @click="showModelInfo(scope.row)">
                  查看模型
                </el-button>
              </template>
            </el-popover> -->
        </template>
      </el-table-column>
    </el-table>
  </a-modal>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import api from "../utils/api.js";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import { Search } from "@element-plus/icons-vue";

// 按关键字搜索增值服务组件
const searchKeyword = ref("");

const dialogVisible = ref(false);
const router = useRouter();

// 声明一种对象类型，其中包括组件名、组件类型和作者
const fetchedExtraAlgorithm = ref([]);
const showExtraModules = () => {
  dialogVisible.value = true;
  getExtraAlgorithm();
};
// 获取已上传的增值服务组件
const getExtraAlgorithm = () => {
  api.get("/user/user_fetch_extra_algorithm/").then((response: any) => {
    if (response.data.code == 401) {
      ElMessageBox.alert("登录状态失效，请重新登陆", "提示", {
        confirmButtonText: "确定",
        callback: () => {
          router.push("/");
        },
      });
    }
    if (response.data.code == 200) {
      fetchedExtraAlgorithm.value = response.data.data;
    }
  });
};
// 根据关键字搜索已上传的增值服务组件
const searchExtraAlgorithm = (keyword: string) => {
  api.get("/user/user_fetch_extra_algorithm/?keyword=" + keyword).then((response: any) => {
    if (response.data.code == 401) {
      ElMessageBox.alert("登录状态失效，请重新登陆", "提示", {
        confirmButtonText: "确定",
        callback: () => {
          router.push("/");
        },
      });
    }
    if (response.data.code == 200) {
      fetchedExtraAlgorithm.value = response.data.data;
    }
  });
};

const emit = defineEmits(["deleteExtraModule"]);

// 删除增值服务组件
const deleteExtraModule = (index: number, row: any) => {
  // 发送删除请求到后端，row 是要删除的数据行
  api
    .get("/user/delete_extra_algorithm/?algorithmAlias=" + row.alias)
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
        // if (modelLoaded.value == row.model_name) {
        //   modelLoaded.value = '无'
        //   modelHasBeenSaved = false
        //   canStartProcess.value = true
        //   handleClear()
        // }
        emit("deleteExtraModule", index);
        if (index !== -1) {
          // 删除前端表中数据
          fetchedExtraAlgorithm.value.splice(index, 1);

          ElMessage({
            message: "删除组件成功",
            type: "success",
          });
        }
      } else {
        if (response.data.code == 404) {
          ElMessage({
            message: "没有权限删除该组件",
            type: "error",
          });
        } else {
          ElMessage({
            message: "删除组件失败，请稍后重试",
            type: "error",
          });
        }
      }
    })
    .catch((error: any) => {
      // 处理错误
      console.error(error);
      ElMessage({
        message: "删除组件失败," + error,
        type: "error",
      });
    });
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

.algorithm-management-dialog {
  width: 60%;
}
</style>
