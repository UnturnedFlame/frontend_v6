<template>
  
  <div
    id="datasetManagementPanel"
    style="
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding: 10px;
      width: 100%;
    "
  >
    <span style="font-size: 20px; width: 100%; text-align: left;" @click="openDatasetManagementPanel">数据管理</span>
    
  </div>

  <el-dialog v-model="datasetManagementDialog" width="1000px" center top="5vh"> 
    <div style="display: flex; flex-direction: column">
      <h2
        style="margin-bottom: 25px; color: #253b45; text-align: left; font-size: 25px"
      >
        数据管理
      </h2>
      <div style="display: flex; flex-direction: row">
        <el-menu
          :default-active="activeIndex"
          style="width: 150px"
          @select="handleSelect"
        >
          <el-menu-item index="1">数据库</el-menu-item>
          <el-menu-item index="2">上传数据集</el-menu-item>
          <!-- <el-menu-item index="3">数据集整合</el-menu-item> -->
          <el-sub-menu index="3">
            <template #title><span>数据集整理</span></template>
            <el-menu-item index="3-1">数据筛选</el-menu-item>
            <el-menu-item index="3-2">数据整合</el-menu-item>
            <!-- <el-menu-item index="2-4-3">item three</el-menu-item> -->
          </el-sub-menu>
        </el-menu>
        <!-- <a-menu v-model:selectedKeys="datasetManagementType" mode="horizontal" :items="menuItems" /> -->
        <div style="display: flex; flex-direction: column; width: 100%">
          <!-- 数据库 -->
          <div v-if="datasetManagementType === '1'">
            <div
              style="
                padding: 5px;
                display: flex;
                justify-content: left;
                align-items: center;
              "
            >
              <p style="font-size: 22px; font-weight: bold">数据库</p>
            </div>
            <div style="height: 1px; background-color: #d3d3d3; margin: 10px 0"></div>
            <div
              style="
                display: flex;
                flex-direction: row;
                width: 250px;
                margin-bottom: 20px;
              "
            >
              <el-input
                v-model="searchDataKeyword"
                placeholder="输入文件名"
                style="width: 180px"
              >
              </el-input>

              <el-button
                type="primary"
                style="width: 20%; margin-left: 10px"
                @click="searchDataset"
                >搜索</el-button
              >
            </div>
            <el-table :data="fetchedDataFiles" height="500" stripe width="100%" border empty-text="暂无数据">
              <el-table-column
                property="owner"
                label="文件上传者"
                show-overflow-tooltip
              />
              <el-table-column
                property="dataset_name"
                label="文件名称"
                show-overflow-tooltip
              />
              <el-table-column
                property="description"
                label="文件描述"
                show-overflow-tooltip
              />
              <el-table-column
                property="file_type"
                label="文件类型"
                show-overflow-tooltip
              />
              <el-table-column label="操作">
                <template #default="scope">
                  <el-popconfirm
                    title="你确定要删除该数据文件吗"
                    @confirm="deleteDatasetConfirm(scope.$index, scope.row)"
                  >
                    <template #reference>
                      <el-button size="small" type="danger" style="width: 50px">
                        删除
                      </el-button>
                    </template>
                    <template #actions="{ confirm, cancel }">
                      <el-row>
                        <el-col :span="12">
                          <el-button size="small" @click="cancel">取消</el-button>
                        </el-col>
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
          </div>

          <!-- 上传数据集 -->
          <div
            style="
              background-color: white;
              display: flex;
              flex-direction: column;
              align-items: flex-start;
            "
            v-if="datasetManagementType === '2'"
          >
            <!-- 上传数据文件 -->
            <div
              style="
                padding: 5px;
                display: flex;
                justify-content: center;
                align-items: center;
              "
            >
              <p style="font-size: 22px; font-weight: bold">上传数据</p>
            </div>
            <div style="height: 1px; background-color: #d3d3d3; margin: 10px 0"></div>
            <div style="position: relative; padding: 20px">
              <a-space direction="vertical">
                <a-form
                  :model="dataFileFormState"
                  ref="fileUploadFormRef"
                  @finish="onFinish"
                >
                  <a-form-item
                    label="文件名称"
                    name="filename"
                    :rules="[
                      { required: true, message: '请输入文件名!' },
                      {
                        pattern: /^[\u4e00-\u9fa5_a-zA-Z0-9]+$/,
                        message: '请输入中英文/数字/下划线',
                        trigger: 'blur',
                      },
                    ]"
                  >
                    <a-input
                      v-model:value="dataFileFormState.filename"
                      placeholder="请输入文件名"
                    />
                    <!-- 提示文件名命名规则 -->
                    <div style="color: #999; font-size: 12px">
                      (只能包含中英文、数字、下划线)
                    </div>
                  </a-form-item>
                  <a-form-item
                    label="文件描述"
                    name="description"
                    :rules="[
                      { required: true, message: '请输入文件描述!' },
                      {
                        min: 1,
                        max: 200,
                        message: '长度应在1到200个字符之间!',
                        trigger: 'blur',
                      },
                    ]"
                  >
                    <a-input
                      v-model:value="dataFileFormState.description"
                      autofocus
                      placeholder="请输入文件描述"
                    />
                    <!-- 提示文件描述命名规则 -->
                    <div style="color: #999; font-size: 12px">(长度不超过200字符)</div>
                  </a-form-item>
                  <a-form-item label="选择数据类型">
                    <a-radio-group v-model:value="dataFileFormState.multipleSensors">
                      <a-radio :value="'multiple'">多传感器数据</a-radio>
                      <a-radio :value="'single'">单传感器数据</a-radio>
                    </a-radio-group>
                  </a-form-item>
                  <a-form-item label="是否公开">
                    <a-radio-group v-model:value="dataFileFormState.isPublic">
                      <a-radio :value="'public'">是</a-radio>
                      <a-radio :value="'private'">否</a-radio>
                    </a-radio-group>
                  </a-form-item>
                  <a-form-item>
                    <div style="">
                      <a-upload
                        :file-list="fileList"
                        :max-count="1"
                        @remove="handleRemove"
                        :before-upload="beforeUpload"
                      >
                        <a-button
                          style="
                            width: 180px;
                            font-size: 16px;
                            background-color: #2082f9;
                            color: white;
                          "
                          :icon="h(FolderOpenOutlined)"
                        >
                          选择本地文件
                        </a-button>
                      </a-upload>
                      <!-- 文件格式提示 -->
                      <!-- <div style="margin-left: 10px">
                        <el-popover
                          title="上传数据格式"
                          confirm-button-text="确认"
                          trigger="hover"
                          :width="500"
                        >
                          <template #default>
                            <p>
                              目前系统可处理的数据格式为长度为2048的信号序列，<br />
                              如果为多传感器数据则确保其数据形状为（2048，传感器数量），其中2048为信号长度，<br />
                              请按照如上的数据格式，并以.npy或是.mat的文件格式上传。
                            </p>
                          </template>
                          <template #reference>
                            <div>
                              <a class="datatype-trigger-icon"
                                ><question-circle-outlined
                              /></a>
                            </div>
                          </template>
                        </el-popover>
                      </div> -->
                    </div>
                  </a-form-item>
                  <a-form-item>
                    <a-button
                      type="primary"
                      html-type="submit"
                      :disabled="fileList?.length === 0"
                      :loading="uploading"
                      style="width: 180px"
                    >
                      <UploadOutlined />
                      {{ uploading ? "正在上传" : "上传至服务器" }}
                    </a-button>
                  </a-form-item>
                </a-form>
              </a-space>
            </div>
            <!-- <div v-if="loadingDataModel == 2">
                <a-button
                  type="default"
                  style="
                    margin-top: 25px;
                    margin-left: 0px;
                    width: 160px;
                    font-size: 16px;
                    background-color: #2082f9;
                    color: white;
                  "
                  @click="openDatasetManagementPanel"
                  :icon="h(FolderOutlined)"
                  >查看已上传文件</a-button
                >
              </div> -->
          </div>

          <!-- 数据筛选 -->
          <div v-if="datasetManagementType === '3-1'">
            <div
              style="
                padding: 5px;
                display: flex;
                justify-content: left;
                align-items: center;
              "
            >
              <p style="font-size: 22px; font-weight: bold">数据筛选</p>
            </div>
            <div style="height: 1px; background-color: #d3d3d3; margin: 10px 0"></div>
            <div
              style="
                display: flex;
                flex-direction: row;
                width: 50%;
                margin-bottom: 20px;
              "
            >
              <el-input
                v-model="searchDataKeyword"
                placeholder="输入文件名"
                style="width: 45%"
              >
              </el-input>

              <el-button
                type="primary"
                style="width: 20%; margin-left: 10px"
                @click="searchDataset"
                >搜索</el-button
              >
            </div>
            <!-- 浏览数据库中存放的文件 -->
            <el-table :data="fetchedDataFiles" height="300" stripe width="100%" border>
              <el-table-column
                property="owner"
                label="文件上传者"
                show-overflow-tooltip
              />
              <el-table-column
                property="dataset_name"
                label="文件名称"
                show-overflow-tooltip
              />
              <el-table-column
                property="description"
                label="文件描述"
                show-overflow-tooltip
              />
              <el-table-column
                property="file_type"
                label="文件类型"
                show-overflow-tooltip
              />
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button
                    style="width: 80px"
                    @click="selecteDatasetToRefactor(scope.row, scope.$index)"
                    >筛选字段</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
            <div
              style="
                display: flex;
                flex-direction: column;
                position: relative;
                padding: 10px;
                height: 30%;
              "
              v-if="getAttributes"
            >
              <p
                style="
                  font-size: 20px;
                  font-weight: bold;

                  text-align: left;
                "
              >
                原数据集：{{ selectedFile }}
              </p>

              <!-- 点击筛选字段操作按钮，弹出该文件所包含的所有字段供用户选择，并另存为新的文件 -->
              <div
                id="allAttributes"
                style="
                  padding: 30px;
                  display: flex;
                  flex-direction: row;
                  align-items: flex-start;
                "
              >
                <div style="font-size: 16px; min-width: 50%">
                  选择新数据集包含的属性（至少选择一项）：
                </div>
                <el-checkbox
                  v-model="selectAll"
                  @change="toggleSelectAll"
                  style="margin-right: 50px"
                  >全选</el-checkbox
                >
                <el-checkbox-group v-model="selectedAttributes" :min="1">
                  <el-checkbox
                    v-for="attribute in allAttributes"
                    :key="attribute"
                    :label="attribute"
                    :value="attribute"
                  >
                    {{ attribute }}
                  </el-checkbox>
                </el-checkbox-group>
              </div>
              <!-- 将筛选属性后的文件保存为新文件 -->
              <div
                id="saveAsNewFile"
                style="
                  padding: 30px;
                  display: flex;
                  flex-direction: row;
                  align-items: flex-start;
                "
              >
                <!-- <el-form
                  :model="selectAttributeform"
                  :rules="rules"
                  ref="selectAttributeform"
                >
                  <el-form-item label="文件名" prop="fileName">
                    <el-input v-model="selectAttributeform.fileName"></el-input>
                  </el-form-item>
                </el-form> -->
                <div tyle="display: flex; flex-direction: row">
                  <span style="font-size: 16px; text-align: left; margin-right: 20px"
                    >保存为新的数据集：</span
                  >
                  <a-space direction="vertical">
                    <!-- <p style="font-size: 16px; text-align: left">
                    保存为新文件：
                  </p> -->
                    <a-form
                      ref="selectAttributeFormState"
                      :model="selectAttributeForm"
                      :rules="saveSelectedAttributeFileRules"
                    >
                      <a-form-item label="文件名称" name="fileName">
                        <a-input
                          v-model:value="selectAttributeForm.fileName"
                          placeholder="请输入文件名"
                        />
                        <!-- 提示文件名命名规则 -->
                        <div style="color: #999; font-size: 12px">
                          (只能包含中英文、数字、下划线)
                        </div>
                      </a-form-item>
                      <a-form-item label="文件描述" name="description">
                        <a-input
                          v-model:value="selectAttributeForm.description"
                          placeholder="请输入文件描述"
                        />
                        <!-- 提示文件描述命名规则 -->
                        <div style="color: #999; font-size: 12px">
                          (长度不超过200字符)
                        </div>
                      </a-form-item>
                      <a-form-item>
                        <a-button
                          type="primary"
                          :loading="uploading"
                          style="width: 180px"
                          @click="saveSelectedAttributeFile"
                        >
                          <FileOutlined />
                          {{ uploading ? "正在保存" : "保存数据集" }}
                        </a-button>
                      </a-form-item>
                    </a-form>
                  </a-space>
                </div>
              </div>
            </div>
          </div>

          <!-- 数据整合 -->
          <div v-if="datasetManagementType === '3-2'" style="min-height: 300px">
            <div
              style="
                padding: 5px;
                display: flex;
                justify-content: left;
                align-items: center;
              "
            >
              <p style="font-size: 22px; font-weight: bold">数据集整合</p>
            </div>
            <div style="height: 1px; background-color: #d3d3d3; margin: 10px 0"></div>

            <div
              style="
                display: flex;
                flex-direction: row;
                justify-content: left;
                align-items: center;
                width: 100%;
                margin-bottom: 20px;
              "
            >
              <div
                style="
                  display: flex;
                  flex-direction: row;
                  justify-content: flex-start;
                  align-items: center;
                  width: 62%;
                "
              >
                <div
                  style="
                    display: flex;

                    align-items: center;
                    font-size: 17px;
                    margin-right: 10px;
                    width: 50%;
                  "
                >
                  选择文件进行整合
                </div>
                <el-input
                  v-model="searchDataKeyword"
                  placeholder="输入文件名"
                  style="width: 50%"
                >
                </el-input>

                <el-button
                  type="primary"
                  style="width: 20%; margin-left: 10px"
                  @click="searchDataset"
                  >搜索</el-button
                >

                <el-button
                  :type="!browseDatabaseState ? 'primary' : 'danger'"
                  style="width: 100px"
                  @click="browseDatabase"
                  >{{ !browseDatabaseState ? "浏览数据库" : "关闭浏览" }}</el-button
                >
              </div>
            </div>
            <!-- 浏览数据库中存放的文件 -->
            <el-table
              v-if="browseDatabaseState"
              :data="fetchedDataFiles"
              height="300"
              stripe
              border
              empty-text="暂无数据"
              width="100%"
            >
              <el-table-column
                property="owner"
                label="文件上传者"
                show-overflow-tooltip
              />
              <el-table-column
                property="dataset_name"
                label="文件名称"
                show-overflow-tooltip
              />
              <el-table-column
                property="description"
                label="文件描述"
                show-overflow-tooltip
              />
              <el-table-column
                property="file_type"
                label="文件类型"
                show-overflow-tooltip
              />
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button
                    style="width: 80px"
                    @click="selecteDatasetToUnion(scope.row, scope.$index)"
                    >添加</el-button
                  >
                </template>
              </el-table-column>
            </el-table>

            <!-- 待整合的数据集 -->
            <div
              style="
                display: flex;
                flex-direction: column;
                justify-content: left;
                margin-top: 30px;
                width: 100%;
              "
            >
              <div
                style="
                  display: flex;
                  flex-direction: row;
                  align-items: center;
                  width: 100%;
                "
              >
                <span style="font-size: 17px; margin-right: 20px; width: 15%"
                  >待整合的数据集</span
                >
                <!-- <el-tag v-for="tag in fileToUnify" :key="tag.name" closable :type="tag.type">
                  {{ tag.name }}
                </el-tag> -->
                <div
                  style="
                    flex-wrap: wrap;
                    display: flex;
                    flex-direction: row;
                    max-width: 80%;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    width: 70%;
                    min-height: 50px;
                  "
                >
                  <span style="color: #999" v-if="fileToUnify.length === 0"
                    >从数据库中选择并添加文件</span
                  >
                  <div
                    v-for="(file, index) in fileToUnify"
                    :key="index"
                    style="
                      display: flex;
                      width: 150px;
                      align-items: center;
                      margin-right: 10px;
                      margin-bottom: 10px;
                      padding: 5px 10px;
                      border: 1px solid #ccc;
                      border-radius: 4px;
                    "
                  >
                    <el-icon style="font-size: 22px"><DocumentAdd /></el-icon>
                    <span style="margin-left: 5px; min-width: 90px">{{
                      file.name
                    }}</span>
                    <el-button
                      type="text"
                      @click="removeFile(index)"
                      style="margin-left: 15px; font-size: 20px"
                    >
                      <!-- <i class="el-icon-delete"></i> -->
                      <el-icon><CircleClose /></el-icon>
                    </el-button>
                  </div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; margin-top: 20px">
                <!-- <span style="font-size: 17px; margin-right: 20px; width: 15%"
                  >数据集整合</span
                > -->
                <!-- 将筛选属性后的文件保存为新文件 -->
                <div
                  id="saveAsNewFile"
                  style="display: flex; flex-direction: row; align-items: flex-start"
                >
                  <div tyle="display: flex; flex-direction: row">
                    <span style="font-size: 16px; text-align: left; margin-right: 20px"
                      >整合保存为新的数据集：</span
                    >
                    <a-space direction="vertical">
                      <a-form
                        ref="uinonDatasetFormRef"
                        :model="selectAttributeForm"
                        :rules="saveSelectedAttributeFileRules"
                      >
                        <a-form-item label="文件名称" name="fileName">
                          <a-input
                            v-model:value="selectAttributeForm.fileName"
                            placeholder="请输入文件名"
                          />
                          <!-- 提示文件名命名规则 -->
                          <div style="color: #999; font-size: 12px">
                            (只能包含中英文、数字、下划线)
                          </div>
                        </a-form-item>
                        <a-form-item label="文件描述" name="description">
                          <a-input
                            v-model:value="selectAttributeForm.description"
                            placeholder="请输入文件描述"
                          />
                          <!-- 提示文件描述命名规则 -->
                          <div style="color: #999; font-size: 12px">
                            (长度不超过200字符)
                          </div>
                        </a-form-item>
                        <a-form-item>
                          <a-button
                            type="primary"
                            html-type="submit"
                            :loading="uploading"
                            style="width: 180px"
                            @click="saveUnionFile"
                          >
                            <FileOutlined />
                            {{ uploading ? "正在保存" : "保存数据集" }}
                          </a-button>
                        </a-form-item>
                      </a-form>
                    </a-space>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>

</template>

<script setup lang="ts">
import { ref, h, watch, reactive } from "vue";
import api from "../utils/api.js";
import { message, UploadProps } from "ant-design-vue";
import { FolderOpenOutlined, UploadOutlined, FileOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { Rule } from "ant-design-vue/es/form";

const searchDataKeyword = ref("");
const fetchedDataFiles = ref<Object[]>([]);
const router = useRouter();
const deleteDatasetConfirmVisible = ref(false);
const datasetManagementDialog = ref(false);
const activeIndex = ref("1");
const datasetManagementType = ref("1");
const dataFileFormState = ref({
  filename: "",
  description: "",
  multipleSensors: "single",
  isPublic: "private",
});

const saveSelectedAttributeFileRules: Record<string, Rule[]> = {
  fileName: [
    { required: true, message: "请输入文件名!", trigger: "change" },
    {
      pattern: /^[\u4e00-\u9fa5_a-zA-Z0-9]+$/,
      message: "请输入中英文/数字/下划线",
      trigger: "blur",
    },
  ],
  description: [
    { required: true, message: "请输入文件描述!", trigger: "change" },
    {
      min: 1,
      max: 200,
      message: "长度应在1到200个字符之间!",
      trigger: "blur",
    },
  ],
};

const getAttributes = ref(false);
const allAttributes = ref<string[]>([]); // 用户所选择文件包含的所有属性
const selectedAttributes = ref<string[]>([]); // 用户最终选择的文件中的属性
const selectedFile = ref(""); // 要进行筛选的文件名

const browseDatabaseState = ref(false);
const browseDatabase = async () => {
  let reponse: boolean = await getFileListFromDatabase();
  if (!reponse) return;
  browseDatabaseState.value = !browseDatabaseState.value;
};

// 待整合的数据集
interface fileToUnifyType {
  name: string;
  id: string;
}
const fileToUnify = ref<fileToUnifyType[]>([]);

const removeFile = (index: number) => {
  fileToUnify.value.splice(index, 1);
};

const selecteDatasetToUnion = (row: any, index: number) => {
  // 如果已经添加则提示
  for (let i = 0; i < fileToUnify.value.length; i++) {
    if (fileToUnify.value[i].name == row.dataset_name) {
      ElMessage({
        message: "已添加该数据集，请勿重复添加",
        type: "warning",
      });
      return;
    }
  }
  // 添加文件时，仅支持csv文件
  if (row.file_type != "csv") {
    ElMessage({
      message: "目前仅支持csv文件的整合！",
      type: "warning",
    });
    return;
  }
  fileToUnify.value.push({
    name: row.dataset_name,
    id: row.id,
  });
};

const uinonDatasetFormRef = ref();
// 保存整合文件
const saveUnionFile = () => {
  uinonDatasetFormRef.value.validate().then(() => {
    // 提交表单
    let formData = new FormData();
    formData.append("datasetName", selectAttributeForm.fileName);
    formData.append("description", selectAttributeForm.description);
    if (fileToUnify.value && fileToUnify.value.length > 0) {
      const datasetIds: string[] = fileToUnify.value.map((file) => file.id);
      formData.append("datasetIds", JSON.stringify(datasetIds));
    } else {
      ElMessage({
        message: "请选择要整合的数据集！",
        type: "warning",
      });
      console.warn("fileToUnify is empty or not defined");
    }

    api
      .post("/user/save_union_datafile/", formData)
      .then((response: any) => {
        if (response.data.code === 200) {
          ElMessage({
            message: "保存成功",
            type: "success",
          });
          // datasetManagementDialog.value = false;
          getFileListFromDatabase();
        } else {
          ElMessage({
            message: "保存失败，" + response.data.message,
            type: "error",
          });
        }
      })
      .catch(() => {
        ElMessage({
          message: "保存失败，请重试",
          type: "error",
        });
      });
  });
};

const uploading = ref(false);

const fileList = ref<UploadProps["fileList"]>([]);

const getFileListFromDatabase = async (): Promise<boolean> => {
  let url = "user/fetch_datafiles/";

  try {
    const response = await api.get(url);
    if (response.status === 200) {
      let datasetInfo = response.data;
      fetchedDataFiles.value = datasetInfo.map((item: Object) => item);
      return true;
    } else {
      ElMessage({
        message: "获取数据失败，" + response.data.message,
        type: "error",
      });
      return false;
    }
  } catch (error) {
    ElMessage({
      message: "获取数据失败，请重试",
      type: "error",
    });
    return false;
  }
};
// 打开数据集管理面板
const openDatasetManagementPanel = async () => {
  let response: boolean = await getFileListFromDatabase();
  if (!response) return;
  datasetManagementDialog.value = true;
};

// 用户选择文件进行字段筛选
const handleSelect = (key: string, keyPath: string[]) => {
  // console.log(key, keyPath)
  getFileListFromDatabase();
  getAttributes.value = false;
  datasetManagementType.value = key;

  // 根据不同的菜单项索引重置表单状态
  if (key === "1") {
    // 数据库页面不需要重置表单
  } else if (key === "2") {
    // 上传数据集页面
    resetDataFileForm();
  } else if (key === "3-1") {
    // 数据筛选页面
    resetSelectAttributeForm();
    getAttributes.value = false; // 关闭筛选字段面板
    selectedFile.value = "";
    selectAll.value = false;
    selectedAttributes.value = [];
    allAttributes.value = [];
  } else if (key === "3-2") {
    // 数据整合页面
    resetSelectAttributeForm();
    browseDatabaseState.value = false;
    fileToUnify.value = [];
  }
};
// 移除文件列表中的文件
const handleRemove: UploadProps["onRemove"] = (file) => {
  if (!fileList.value) {
    fileList.value = [];
  }
  const index = fileList.value.indexOf(file);
  const newFileList = fileList.value.slice();
  newFileList.splice(index, 1);
  fileList.value = newFileList;
};

const beforeUpload: UploadProps["beforeUpload"] = (file) => {
  const allowedTypes = [".npy", ".mat", ".csv"];
  const fileType = file.name.split(".").pop().toLowerCase();
  if (!allowedTypes.includes("." + fileType)) {
    // ElMessage({
    //   message: '文件格式错误，请上传mat或npy文件',
    //   type: 'error',
    // });
    message.error("文件格式错误，请上传mat或npy文件");
    return false;
  }
  if (!fileList.value) {
    fileList.value = [];
  }
  fileList.value.length = 0;
  fileList.value = [...(fileList.value || []), file];
  return false;
};

// 确认上传文件对话框
const uploadconfirmLoading = ref<boolean>(false);
const uploadConfirmDialog = ref<boolean>(false);
// 确认上传文件
const onFinish = () => {
  uploadconfirmLoading.value = true;
  const formData = new FormData();
  formData.append("file", fileList.value[0]);
  formData.append("filename", dataFileFormState.value.filename);
  formData.append("description", dataFileFormState.value.description);
  formData.append("multipleSensors", dataFileFormState.value.multipleSensors);
  formData.append("isPublic", dataFileFormState.value.isPublic);
  uploading.value = true;

  api
    .post("/user/upload_datafile/", formData)
    .then((response: any) => {
      if (response.data.message == "save data success") {
        fileList.value = [];
        uploading.value = false;
        // message.success("数据文件上传成功");
        ElMessage({
          message: "数据文件上传成功",
          type: "success",
        });
        uploadconfirmLoading.value = false;
        uploadConfirmDialog.value = false;
      } else {
        uploading.value = false;
        // message.error("文件上传失败, " + response.data.message);
        ElMessage({
          message: "文件上传失败, " + response.data.message,
          type: "error",
        });
        uploadconfirmLoading.value = false;
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
      uploading.value = false;
      uploadconfirmLoading.value = false;
      // message.error("上传失败, " + error);
      ElMessage({
        message: "上传失败, " + error,
        type: "error",
      });
    });
};

const selectAttributeFormState = ref();
// 将筛选后的数据文件保存为新的文件
const selectAttributeForm = reactive({
  fileName: "",
  description: "",
  selectedFileId: "",
});

// 将用户筛选过的数据集保存为新的文件
const saveSelectedAttributeFile = () => {
  selectAttributeFormState.value
    .validate()
    .then(() => {
      let formData = new FormData();
      formData.append("selectedColumns", JSON.stringify(selectedAttributes.value));
      formData.append("datasetName", selectAttributeForm.fileName);
      formData.append("datasetId", selectAttributeForm.selectedFileId);
      formData.append("description", selectAttributeForm.description);

      console.log("正在提交表单曹村新文件。。。");
      uploading.value = true;
      api.post("user/save_selected_file/", formData).then((response: any) => {
        if (response.data.code === 200) {
          ElMessage({
            message: "保存新数据集成功",
            type: "success",
          });

          // 刷新列表
          getFileListFromDatabase();
        } else if (response.data.code === 400) {
          ElMessage({
            message: "保存失败" + response.data.message,
            type: "error",
          });
        }
        uploading.value = false;
      });
    })
    .catch((error: any) => {
      uploading.value = false;
      console.log("error", error);
    });
};

// 按关键字搜索用户数据文件
const searchDataset = () => {
  api
    .get("user/search_dataset/?keywords=" + searchDataKeyword.value)
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      } else if (response.data.code == 200) {
        fetchedDataFiles.value.length = 0;
        for (let item of response.data.data) {
          fetchedDataFiles.value.push(item);
        }
      }
    })
    .catch(() => {
      // message.error("搜索失败，请重试");
      ElMessage({
        message: "搜索失败，请重试",
        type: "error",
      });
    });
};

const deleteDatasetConfirm = (index: any, row: any) => {
  api
    .get("/user/delete_datafile/?filename=" + row.dataset_name)
    .then((response: any) => {
      if (response.data.code == 200) {
        // 删除前端表中数据
        fetchedDataFiles.value.splice(index, 1);
        deleteDatasetConfirmVisible.value = false;
        ElMessage({
          message: "文件删除成功",
          type: "success",
        });
        // message.success("文件删除成功");
        // 如果文件已经被加载，则需要取消加载行为
        // if (row.dataset_name == usingDatafile.value) {
        //   usingDatafile.value = '无'
        // }
      } else if (response.data.code == 400) {
        // message.error("删除失败: " + response.data.message);
        ElMessage({
          message: "删除失败: " + response.data.message,
          type: "error",
        });
      } else if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      }
    })
    .catch(() => {
      // message.error("删除文件失败");
      ElMessage({
        message: "删除文件失败",
        type: "error",
      });
    });
};

// 用户根据属性筛选数据集
const selecteDatasetToRefactor = (row: Object, index: number) => {
  console.log("row: ", row);
  let datasetFileId = row.id;
  api
    .get("user/get_dataset_columns/?datasetId=" + datasetFileId)
    .then((response: any) => {
      if (response.data.code == 200) {
        console.log("response.resuly: ", response.data.columnNames);
        // 将返回的属性全部以多选框的选项的实行展现出来
        allAttributes.value = response.data.columnNames;
        // selectedAttributes.value.push(allAttributes.value[0]);
        // 确保至少选中原数据集的一项属性作为新数据集的属性
        selectedAttributes.value = [allAttributes.value[0]];
        getAttributes.value = true;
        selectedFile.value = row.dataset_name;
        selectAttributeForm.selectedFileId = datasetFileId;
      } else if (response.data.code == 400) {
        ElMessage({
          message: response.data.message,
          type: "error",
        });
      }
    })
    .catch(() => {
      ElMessage({
        message: "请求错误",
        type: "error",
      });
    });
};

const selectAll = ref(false); // 全选状态

// 处理全选逻辑
const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedAttributes.value = [...allAttributes.value];
  } else {
    // 取消全选时至少保留第一项
    if (allAttributes.value.length > 0) {
      selectedAttributes.value = [allAttributes.value[0]];
    } else {
      selectedAttributes.value = [];
    }
  }
};

// 监听 selectedAttributes 的变化，更新 selectAll 状态
watch(selectedAttributes, (newVal) => {
  if (newVal.length === allAttributes.value.length) {
    selectAll.value = true;
  } else {
    selectAll.value = false;
  }

  // 确保至少保留第一项
  if (newVal.length === 0 && allAttributes.value.length > 0) {
    selectedAttributes.value = [allAttributes.value[0]];
  }
});

const resetDataFileForm = () => {
  dataFileFormState.value = {
    filename: "",
    description: "",
    multipleSensors: "multiple",
    isPublic: "public",
  };
  fileList.value = [];
  uploading.value = false;
};
const resetSelectAttributeForm = () => {
  selectAttributeForm.selectedFileId = "";
  selectAttributeForm.fileName = "";
  selectAttributeForm.description = "";
};
// 用户浏览原始数据
// const browseDataset = (row: { dataset_name: any; }) => {

// // 清除可视化区域内容
// resultsViewClear()
// canShowResults.value = true
// // 发送请求获取原始数据的波形图
// let filename = row.dataset_name

// api.get('user/browse_datafile/?filename=' + filename).then((response: any) => {
//   if (response.status === 200) {
//     displayRawDataWaveform.value = true
//     let data = response.data
//     let figure = data.figure_Base64

//     rawDataWaveform.value = 'data:image/png;base64,' + figure
//     currentDataBrowsing.value = filename

//     console.log('访问成功：')
//   } else {
//     ElMessage.error('访问文件失败')
//   }
// })
//     .catch((error: any) => {
//       console.log('访问文件失败：', error)
//     })
// }
</script>

<style scoped></style>
