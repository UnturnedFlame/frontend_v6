<template>
  <div class="shadow-border title-container">模型审核</div>
  <div class="table-container">
    <el-table
      :data="tableData"
      style="width: 100%"
      height="500px"
      :stripe="true"
      :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#606266' }"
      border
      empty-text="暂无数据"
    >
      <!-- <el-table-column prop="id" label="ID" /> -->
      <!-- <el-table-column prop="id" label="序号" width="100px" /> -->
      <el-table-column prop="create_time" label="申请时间" />
      <el-table-column prop="applicant" label="申请人" />
      <el-table-column prop="modelName" label="申请发布模型" />
      <el-table-column prop="status" label="申请状态" />
      <el-table-column prop="auditor" label="审批人" />
      <el-table-column prop="audition_time" label="审批时间" />

      <!-- <el-table-column prop="password" label="密码" /> -->
      <el-table-column label="操作" width="300px">
        <template #default="scope">
          <div style="display: flex;">
            <!-- 单选框 -->

            <!-- 删除模型发布申请 -->
            <el-popconfirm
              title="你确定要删除该条申请吗?"
              @confirm="handleDeleteApplications(scope.$index, scope.row)"
            >
              <template #reference>
                <!-- <el-button
                  size="large"
                  type="danger"
                  circle
                  plain
                  style="margin-right: 10px"
                  ><el-icon><Delete /></el-icon
                ></el-button> -->
                <el-button
                  type="danger"
                  style="max-width: 100px;"
                  >删除</el-button>
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

            <!-- 审核发布模型申请 -->
            <el-button
              style="width: 100px"
              type="success"
              v-if="scope.row.status === '未处理'"
              @click="publishModelConfirm(scope.$index, scope.row)"
              >通过</el-button
            >
            <el-button
              style="width: 100px"
              type="warning"
              v-if="scope.row.status === '未处理'"
              @click="publishModelDenny(scope.$index, scope.row)"
              >不通过</el-button
            >
            <!-- <el-popconfirm
              title="你确定该条申请吗?"
              @confirm="handleDeleteApplications(scope.$index, scope.row)"
              width="100px"
            >
              <template #reference>
                <el-button
                  size="large"
                  type="danger"
                  circle
                  plain
                  style="margin-right: 10px"
                  ><el-icon><Delete /></el-icon
                ></el-button>
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
            </el-popconfirm> -->

            <!-- <span
              style="
                margin-left: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-width: 100px;
              "
            >
              <p>是否已处理：</p>
              <el-checkbox
                v-model="scope.row.processed"
                @change="handleProcessedChange(scope.row)"
                style="margin-left: 10px"
              ></el-checkbox
            ></span> -->
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { onMounted } from "vue";
import { ElMessage } from "element-plus";
import api from "../utils/api.js";
// import { labelsForAlgorithms } from "./constant.ts";
import { ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";

interface publishModelApplication {
  id: number;
  applicant: string;
  modelName: string;
  status: string;
  create_time: string;
  // processed: boolean;
}
const tableData = reactive<publishModelApplication[]>([]);

const router = useRouter(); // 获取路由实例

// 获取用户提交的模型发布申请
const fetchApplications = () => {
  api
    .get("administration/fetch_publish_model_applications/")
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      } else if (response.data.code == 200) {
        let applications = response.data.data;
        tableData.length = 0;
        for (let application of applications) {
          tableData.push({
            ...application,
            // processed: application.status === "已处理", // 根据实际情况设置初始状态
          });
        }
      } else {
        ElMessage.error("获取发布模型申请失败，" + response.data.message);
      }
    })
    .catch(() => {
      ElMessage.error("获取发布模型申请失败，请稍后重试");
    });
};

onMounted(() => {
  fetchApplications();
});

const handleDeleteApplications = (index: number, row: any) => {
  api
    .get("administration/delete_publish_model_applications/?applicationId=" + row.id)
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      } else if (response.data.code == 200) {
        if (index !== -1) {
          tableData.splice(index, 1);
        }
      } else {
        ElMessage.error("删除发布模型申请失败，" + response.data.message);
      }
    })
    .catch(() => {
      ElMessage.error("删除发布模型申请失败，请稍后重试");
    });
};

// 处理单选框变化
// const handleProcessedChange = (row: publishModelApplication) => {
//   const newStatus = row.processed ? "已处理" : "待处理";
//   let formData = new FormData();
//   formData.append("feedbackId", String(row.id));
//   formData.append("newStatus", newStatus);
//   api
//     .post("administration/update_feedback_status/", formData)
//     .then((response: any) => {
//       if (response.data.code == 401) {
//         ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
//           confirmButtonText: "确定",
//           callback: () => {
//             router.push("/");
//           },
//         });
//       } else if (response.data.code == 200) {
//         row.status = newStatus; // 更新本地状态
//         ElMessage.success("反馈状态更新成功");
//       }
//     })
//     .catch(() => {
//       ElMessage.error("更新反馈状态失败，请稍后重试");
//       row.processed = !row.processed; // 恢复原状态
//     });
// };

const publishModelConfirm = (index: number, row: publishModelApplication) => {
  api
    .get(
      "administration/handle_publish_model_request/?applicationId=" +
        row.id +
        "&status=审核通过"
    )
    .then((response: any) => {
      if (response.data.code == 200) {
        ElMessage.success("发布模型申请审核通过");
        fetchApplications();
      } else {
        if (response.data.code == 401) {
          ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
            confirmButtonText: "确定",
            callback: () => {
              router.push("/");
            },
          })
        } else {
          ElMessage.error("发布模型申请审核失败，" + response.data.message);
        }
      }
    })
    .catch(() => {
      ElMessage.error("发布模型申请审核失败，请稍后重试");
    });
};

const publishModelDenny = (index: number, row: publishModelApplication) => {
  api
    .get(
      "administration/handle_publish_model_request/?applicationId=" +
        row.id +
        "&status=审核不通过"
    )
    .then((response: any) => {
      if (response.data.code == 200) {
        ElMessage.success("发布模型申请审核不通过");
        fetchApplications();
      }else{
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      } else {
        ElMessage.error("发布模型申请审核失败，" + response.data.message);
      }}
    })
    .catch(() => {
      ElMessage.error("发布模型申请审核失败，请稍后重试");
    });
};
</script>

<style>
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

.detail-container {
  width: 86%;
  padding: 20px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin-left: 30px;
  margin-top: 20px;
}

/* 按钮悬停效果 */
.el-button--danger.is-plain:hover {
  background-color: #fde2e2;
  color: #f56c6c;
}

.el-button--primary.is-plain:hover {
  background-color: #e0f3ff;
  color: #409eff;
}
</style>
