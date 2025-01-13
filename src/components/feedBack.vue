<template>
  <div class="shadow-border title-container">用户反馈意见</div>
  <div class="table-container">
    <el-table
      :data="tableData"
      style="width: 100%"
      height="100%"
      :stripe="true"
      :header-cell-style="{ backgroundColor: '#f5f7fa', color: '#606266' }"
      border
      empty-text="暂无数据"
    >
      <!-- <el-table-column prop="id" label="ID" /> -->
      <!-- <el-table-column prop="id" label="序号" width="70px" /> -->
      <el-table-column prop="username" label="反馈用户" />
      <el-table-column prop="time" label="反馈时间" />
      <el-table-column prop="model" label="使用模型" />
      <el-table-column prop="datafile" label="使用数据文件" />
      <!-- <el-table-column prop="password" label="密码" /> -->
      <el-table-column prop="module" label="有疑问的组件" />
      <el-table-column prop="status" label="处理状态" />
      <el-table-column label="操作" width="250px">
        <template #default="scope">
          <div style="display: flex">
            <!-- 单选框 -->
            
            <!-- 删除用户反馈 -->
            <el-popconfirm
              title="你确定要删除该条反馈吗?"
              @confirm="handleDeleteFeedBack(scope.$index, scope.row)"
              width="100px"
            >
              <template #reference>
                
                <el-button
                  size="large"
                  type="danger"
                  circle
                  plain
                  style="margin-right: 10px"
                  
                  ><el-icon><Delete /></el-icon></el-button
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
           
            <!-- 点击显示用户反馈详情 -->
            <el-tooltip content="查看反馈详情" placement="top" effect="light">
              <el-button
                size="large"
                type="primary"
                plain
                circle
                @click="handleSelectFeedback(scope.row)"
              >
                <el-icon><View /></el-icon>
              </el-button>
            </el-tooltip>

            <span style="margin-left: 20px; display: flex; justify-content: center; align-items: center;">
            <p>已处理：</p>
            <el-checkbox
              v-model="scope.row.processed"
              @change="handleProcessedChange(scope.row)"
              style="margin-left: 10px;"
            ></el-checkbox></span>
            
            <!-- <el-popconfirm
              title="你确定要重置该用户的密码吗?"
              @confirm="complete(scope.$index, scope.row)"
              width="100px"
            >
              <template #reference>
                <el-button size="small" type="primary" style="width: 100px"
                  >重置密码</el-button
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
            </el-popconfirm> -->
            <!-- <el-button size="small" type="primary" @click="handleResetPassword(scope.$index, scope.row)" style="width: 100px;">
              重置密码
            </el-button> -->
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <div v-if="selectedFeedback.id" class="detail-container">
    <el-scrollbar height="100%">
      
      <h3>反馈详情</h3>
      <p><strong>反馈序号:</strong> {{ selectedFeedback.id }}</p>
      <p><strong>反馈用户:</strong> {{ selectedFeedback.username }}</p>
      <p><strong>反馈时间:</strong> {{ selectedFeedback.time }}</p>
      <p><strong>使用模型:</strong> {{ selectedFeedback.model }}</p>
      <p><strong>使用数据文件:</strong> {{ selectedFeedback.datafile }}</p>
      <p><strong>有疑问的组件:</strong> {{ selectedFeedback.module }}</p>
      
      <p><strong>问题描述:</strong> {{ selectedFeedback.question }}</p>
      
    </el-scrollbar>
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

interface Feedback {
  id: number;
  username: string;
  model: string;
  datafile: string;
  module: string;
  question: string;
  status: string;
  time: string;
  processed: boolean;
}
const tableData = reactive<Feedback[]>([]);

const router = useRouter(); // 获取路由实例

const selectedFeedback = reactive<Feedback>({
  id: 0,
  username: "",
  model: "",
  datafile: "",
  module: "",
  question: "",
  status: "",
  time: "",
  processed: false,
});
// 获取用户模型
const fetchFeedBack = () => {
  api
    .get("administration/fetch_feedbacks/")
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      } else if (response.data.code == 200) {
        let feedbacks = response.data.data;
        tableData.length = 0;
        for (let feedback of feedbacks) {
          tableData.push({
            ...feedback,
            processed: feedback.status === "已处理", // 根据实际情况设置初始状态
          });
        }
      }
    })
    .catch(() => {
      ElMessage.error("获取用户反馈失败，请稍后重试");
    });
};

onMounted(() => {
  fetchFeedBack();
});

const handleDeleteFeedBack = (index: number, row: any) => {
  api.get("administration/delete_feedbacks/?feedbackId=" + row.id).then((response: any) => {
    if (response.data.code == 401) {
      ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
        confirmButtonText: "确定",
        callback: () => {
          router.push("/");
        },
      });
    } else if (response.data.code == 200) {
      if (index !== -1) {
        tableData.splice(index,1);
      }
    }
  })
  .catch(() => {
    ElMessage.error("删除用户反馈失败，请稍后重试");
  });
};

// 处理单选框变化
const handleProcessedChange = (row: Feedback) => {
  const newStatus = row.processed ? "已处理" : "待处理";
  let formData = new FormData();
  formData.append("feedbackId", String(row.id));
  formData.append("newStatus", newStatus);
  api.post("administration/update_feedback_status/", formData)
  .then((response: any) => {
    if (response.data.code == 401) {
      ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
        confirmButtonText: "确定",
        callback: () => {
          router.push("/");
        },
      });
    } else if (response.data.code == 200) {
      row.status = newStatus; // 更新本地状态
      ElMessage.success("反馈状态更新成功");
    }
  })
  .catch(() => {
    ElMessage.error("更新反馈状态失败，请稍后重试");
    row.processed = !row.processed; // 恢复原状态
  });
};

// 显示反馈详情
const handleSelectFeedback = (row: any) => {
  selectedFeedback.id = row.id;
  selectedFeedback.username = row.username;
  selectedFeedback.model = row.model;
  selectedFeedback.datafile = row.datafile;
  selectedFeedback.module = row.module;
  selectedFeedback.question = row.question;
  selectedFeedback.status = row.status;
  selectedFeedback.time = row.time;
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
  height: 40%;
  padding: 20px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin-left: 30px;
}

.detail-container {
  width: 86%;
  height: 30%;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin-left: 30px;
  text-align: left;
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
