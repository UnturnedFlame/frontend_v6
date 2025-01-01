<template>
  <div>
    <!-- 搜索框 -->
    <el-input
      v-model="searchKeywordOfTree"
      placeholder="请输入关键字查询"
      style="width: 100%; margin-bottom: 5px"
    />
    <!-- 新增树形结构 -->
    <!-- <div style="width: 100%; display: flex; flex-direction: row" v-if="props.userRole === 'superuser'">
      <el-input
        v-model="nameOfNewTree"
        placeholder="输入名称"
        style="width: 60%; margin-bottom: 5px"
      />
      <el-button style="width: 40%" @click="addNewComponentTree"
        >新增结构树</el-button
      >
    </div> -->
     <!-- 新增树形结构 -->
    <div style="width: 100%; margin-bottom: 15px;" v-if="props.userRole === 'superuser'">
      <el-form :model="form" style="width: 100%; display: flex; flex-direction: row" :rules="rules" ref="formRef">
        <el-form-item prop="nameOfNewTree" style="width: 60%;">
          <el-input
            v-model="form.nameOfNewTree"
            placeholder="输入结构树名称"
          />
        </el-form-item>
        <el-form-item style="width: 40%">
          <el-button style="width: 100%"@click="submitForm">新增结构树</el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 已有树形结构，使用 scoped-slot 渲染 -->
    <div style="width: 100%; overflow-x: auto; font-size: 20px">
        <el-tree
          ref="treeRef"
          :data="filteredDataOfTree"
          node-key="id"
          :highlight-current="true"
          :expand-on-click-node="false"
          :default-expand-all="isExpandAllOfTree"
          :filter-node-method="filterNodeOfTree"
          :accordion="false"
          empty-text="无数据"
          style="display: inline-block; min-width: 100%; font-size: 20px"
        >
          <template #default="{ node, data }">
              <span class="custom-tree-node" style="">
                  <el-icon v-if="data.isModel" class="model-icon">
                    <img src="@/assets/model-icon.svg" style="width: 20px; height: 20px;" alt="model">
                 </el-icon>
              <span class="node-label" >{{ getNodeLable(data) }}</span>
              <span class="node-actions" v-if="props.userRole === 'superuser' && !data.isModel">
                <el-icon @click="appendNodeToTree(data)" :style="{ color: '#67c23a' }" v-if="data.disabled === true">
                  <Plus />
                </el-icon>
                
                <el-popconfirm
                  title="你确定要删除该数据文件吗"
                  @confirm="removeNodeOfTree(node, data)"
                >
                  <template #reference>
                    <el-icon :style="{ color: '#f56c6c' }">
                      <Delete />
                    </el-icon>
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
                <el-icon @click="editOfTree(node, data)" :style="{ color: '#409eff' }">
                  <Edit />
                </el-icon>
              </span>
               <div v-if="data.isModel">
                  <el-icon  class="model-icon" @click="modelClick(data)">
                    <i class="fa-solid fa-square-binary"></i>
                  </el-icon>
                  
                  <el-popconfirm
                    title="你确定要删除该数据文件吗"
                    @confirm="deleteModelConfirm(node, data)"
                  >
                    <template #reference>
                      <el-icon v-if="props.userRole=='superuser'" :style="{ color: '#f56c6c' }">
                        <Delete />
                      </el-icon>
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
              </div>
            </span>
          </template>
        </el-tree>
        <!-- 编辑对话框 -->
        <el-dialog
          v-model="isEditDialogVisibleOfTree"
          title="编辑节点"
          :close-on-click-modal="true"
          :before-close="handleCloseOfTree"
          class="custom-dialog"
          style="width: 40%"
        >
          <span style="margin-right: 20px">新的节点名称：</span>
          <el-input
            v-model="editNodeLabelOfTree"
            placeholder="请输入新的节点名称"
            :autofocus="true"
            class="half-width-input"
            style="width: 50%"
          />
          <div style="font-size: 15px; color: gray">只能包含中英文、数字和下划线</div>
          <!-- 标记节点为最终类型后，不可添加子节点，而可以向其中添加模型 -->
          <span>是否标记节点为最终类型：</span>
          <el-radio-group v-model="isNodeEditable" style="width: 50%">
            <el-radio :value="true" size="large">否</el-radio>
            <el-radio :value="false" size="large">是</el-radio>
          </el-radio-group>
          <!-- <span slot="footer" class="dialog-footer">
                <el-button @click="isEditDialogVisibleOfTree = false">取消</el-button>
                <el-button type="primary" @click="saveEditOfTree">保存</el-button>
            </span> -->
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="isEditDialogVisibleOfTree = false" style="width: 100px"
                >取消</el-button
              >
              <el-button type="primary" @click="saveEditOfTree" style="width: 100px"
                >确认</el-button
              >
            </div>
          </template>
        </el-dialog>
      </div>
  </div>
</template>

<script setup lang="ts">
import {ElForm, ElMessage, ElMessageBox, ElTree} from "element-plus";
import { ref, watch, reactive, onMounted } from "vue";
import api from "../utils/api.js";
import type Node from 'element-plus/es/components/tree/src/model/node'
import { isNode } from "@vue-flow/core";
import { useRouter } from "vue-router";
//向父组件传递信息
const emit = defineEmits(["resetModel", "loadModel"]);
interface modelInfo {
  id: number;
  model_name: string;
  description: string;
  author: string;
  model_info: any;
  isPublish: string;
}
// 从后端获取到的历史模型的信息
const fetchedModelsInfo = ref<modelInfo[]>([]);
// 删除模型确认
const deleteModelConfirmVisible = ref(false);
const store = ref(
    {
      modelId:null,
      modelName:'',
      modelInfo:{}
    }
)
const router = useRouter();
const modelLoaded = ref("无");
const modelClick =(data) => {
  console.log('当前点击的节点信息',data);
  console.log('获取的模型信息',fetchedModelsInfo)
  store.value.modelId = data.modelId;
  store.value.modelName = data.label;
  store.value.modelInfo = fetchedModelsInfo.value.filter(item => item.id === store.value.modelId);
  emit("loadModel", store);

}


const form = reactive({
  nameOfNewTree: ""
});

const rules = reactive({
  nameOfNewTree: [
    { required: true, message: '请输入新增结构树名称', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_\u4e00-\u9fa5]+$/, message: '组件名称只能包含中英文、下划线和数字', trigger: 'blur' }
  ]
});

const formRef = ref<InstanceType<typeof ElForm>>();

const submitForm = () => {
  formRef.value!.validate((valid) => {
    if (valid) {
      addNewComponentTree();
    } else {
      console.log('校验失败');
      return false;
    }
  });
};


// 点击子组件的加载模型，加载模型并到父组件userPlatForm.vue显示出来
const loadModel = (row: modelInfo) => {
  modelLoaded.value = row.model_name;
  emit("loadModel", row);
};
// 从数据库获取模型信息
const fetchModelInfoFromDatabase = () => {
  //   dataDrawer.value = false; // 打开历史模型抽屉
  // 向后端发送请求获取用户的历史模型
  api
      .get(props.userRole=='superuser' ? "user/fetch_models/" : "user/fetch_models_published/")
      .then((response: any) => {
        if (response.data.code === 200) {
          // modelsDrawer.value = true;
          let modelsInfo = response.data.models;
          fetchedModelsInfo.value = [];
          for (let item of modelsInfo) {

            if(props.userRole=='user'){
              console.log('进入用户角色获取树结构',item)
              if(item.isPublish=='已发布'){
                console.log('进入已发布判断',item);
                fetchedModelsInfo.value.push(item);
              }else{
                continue
              }
            }else{
              fetchedModelsInfo.value.push(item);
            }

          }
          console.log('huoqudeshujiegou',fetchedModelsInfo.value)
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
//删除模型
const deleteModelConfirm = (node: Node, data: Tree) => {
  // 发送删除请求到后端，row 是要删除的数据行
  api
      .get("/user/delete_model/?row_id=" + data.modelId)
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
          emit("resetModel", data.label);
          console.log('删除成功');
          // 刷新数据
          // getComponentTrees();
          const parent = node.parent
          const children: Tree[] = parent.data.children || parent.data
          const index = children.findIndex((d) => d.value === data.value)
          children.splice(index, 1)
          // dataSourceOfTree = [...dataSourceOfTree]
          Object.assign(dataSourceOfTree, [...dataSourceOfTree])
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
interface Tree {
  label: string; // 节点名称
  value: string; // 节点id
  disabled: boolean; // 是否禁用添加子类型
  children?: Tree[]; // 子节点
  isModel: boolean;  // 是否为模型
  modelId: string;  // 模型id
  isPublished: string; // 是否发布
}

const treeRef = ref<InstanceType<typeof ElTree>>();

let idOfTree = 1000;

//是否展开全部
let isExpandAllOfTree = ref(false);

// 搜索关键字
const searchKeywordOfTree = ref("");
// 是否显示编辑对话框
const isEditDialogVisibleOfTree = ref(false);
// 当前编辑的节点
const editingNodeOfTree = ref<Tree | null>(null);
// 编辑框中的节点名称
const editNodeLabelOfTree = ref("");

// 定义从父组件接收到的userrole
const props = defineProps({
  userRole: String,
});



// 树形结构数据
const dataSourceOfTree = reactive<Tree[]>([]);
onMounted(() => {
  // 获取树形结构
  getComponentTrees();
  //获取模型信息
  fetchModelInfoFromDatabase();

});

//递归过滤未发布节点
function filterTree(data) {
  return data
      .map(node => {
        // 如果有子节点，递归处理子节点
        if (node.children && node.children.length > 0) {
          const filteredChildren = filterTree(node.children);
          // 如果子节点过滤后不为空，保留当前节点
          if (filteredChildren.length > 0) {
            return {
              ...node,
              children: filteredChildren
            };
          }
          // 如果子节点过滤后为空，不保留当前节点
          return null;
        }
        // 处理叶子节点，根据条件过滤
        if (node.isModel && node.isPublished === '未发布') {
          return null; // 不保留isModel为true且isPublished为未发布的叶子节点
        }
        return node; // 保留其他叶子节点
      })
      .filter(node => node !== null); // 移除所有null节点
}
// 从后端获取树形结构
const getComponentTrees = () => {
  api.get("user/get_component_trees").then((response: any) => {
    // 请求成功，后端返回数据
    if (response.data.code === 200) {
      dataSourceOfTree.length = 0;

      if(props.userRole=='user'){
        let filteredDataOfTreeS
        response.data.trees.map((tree: Tree) => dataSourceOfTree.push(tree));
        // 过滤后的数据
        filteredDataOfTreeS = filterTree(dataSourceOfTree);
        dataSourceOfTree.length = 0;
        filteredDataOfTreeS.map((tree: Tree) => dataSourceOfTree.push(tree));
        console.log("获取到树形结构: ", dataSourceOfTree);
      }else{
        response.data.trees.map((tree: Tree) => dataSourceOfTree.push(tree));
      }

    } else {
      ElMessage.error("获取树形结构失败，" + response.data.message);
    }
  });
};

// 将子组件的刷新树形结构操作暴露给父组件
// 暴露给父组件的方法
defineExpose({
  getComponentTrees,
  fetchModelInfoFromDatabase
});

// const nameOfNewTree = ref("");
// 新增组件树形结构
const addNewComponentTree = () => {
  // 检验nameOfNewTree的格式，不能为空，且只能包含中英文、下划线和数字
  // if (nameOfNewTree.value.trim() === "") {
  //   ElMessage.error("请输入新增结构树名称");
  //   return;
  // }
  // if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(nameOfNewTree.value)) {
  //   ElMessage.error("组件名称只能包含中英文、下划线和数字");
  //   return;
  // }
  // 向后端发送建立新的结构树的post请求，请求内容包含新的结构树的树名
  let formData = new FormData();
  formData.append("treeName", form.nameOfNewTree);
  api
    .post("user/create_component_tree", formData)
    .then((response: any) => {
      // 请求成功，后端返回数据
      if (response.data.code === 200) {
        // 添加成功
        ElMessage.success("添加成功");
        getComponentTrees();
        // 重置输入框
        form.nameOfNewTree = "";
      } else {
        ElMessage.error("新建树失败，" + response.data.message);
      }
    })
    .catch((error: any) => {
      console.log(error);
      ElMessage.error("新建树失败，" + error);
    });
};



// 搜索过滤后的数据
const filteredDataOfTree = ref<Tree[]>(dataSourceOfTree);

// 添加子节点
const appendNodeToTree = (data: Tree) => {
  console.log("添加节点方法执行...");
  console.log("data: ", data);

  if (data.disabled) {
    let parentNodeValue = data.value;
    let treeName = data.value.split(".")[0];
    let formData = new FormData();
    formData.append("treeName", treeName);
    formData.append("parentNodeValue", parentNodeValue);

    api
      .post("user/add_node_to_tree/", formData)
      .then((response: any) => {
        if (response.data.code === 200) {
          ElMessage.success("添加节点成功");
          // getComponentTrees();
          const newChild = response.data.node;
          console.log("appendNodeToTree newChild: ", newChild);
          if (!data.children) {
            data.children = []
          }
          data.children.push(newChild)
          // Object.assign(dataSourceOfTree, [...dataSourceOfTree])
        } else {
          ElMessage.error("添加节点失败, " + response.data.message);
        }
      })
      .catch((error: any) => {
        ElMessage.error(error + ", 添加节点失败, 请重试");
      });
  } else {
    ElMessage.warning("该节点不可添加子节点");
  }

  //   const newChild = { id: idOfTree++, label: "New Node", children: [] };
  //   if (!data.children) {
  //     data.children = [];
  //   }
  //   data.children.push(newChild);
  // data.children = [];
};

// 删除节点
const removeNodeOfTree = (node: Node, data: Tree) => {
  console.log("删除节点方法执行...");
  let formData = new FormData();
  formData.append("treeName", data.value.split(".")[0]);
  formData.append("nodeValue", String(data.value));

  api
    .post("user/delete_node/", formData)
    .then((response: any) => {
      if (response.data.code == 200) {
        ElMessage.success("节点删除成功");
        // 刷新数据
        // getComponentTrees();
        const parent = node.parent
        const children: Tree[] = parent.data.children || parent.data
        console.log("removeNodeOfTree children: ", children)
        const index = children.findIndex((d) => d.value === data.value)
        console.log("removeNodeOfTree index: ", index)
        children.splice(index, 1)
        // dataSourceOfTree = [...dataSourceOfTree]
        // Object.assign(dataSourceOfTree, [...dataSourceOfTree])
      } else {
        ElMessage.error("节点删除失败, " + response.data.message);
      }
    })
    .catch((error: any) => {
      ElMessage.error("节点删除失败, " + error);
    });
};


const getNodeLable = (data: Tree) => {
  if (!data.isModel){
    return data.label
  }else{
    // // 如果用户是普通用户，并且节点未发布，则不显示
    // if (props.userRole=== 'user' && data.isPublished !== '已发布') {
    //   return false; // 或者返回null，或者不返回任何内容
    // }
    return data.isPublished == '已发布' ? data.label + " (已发布)" : data.label + " (未发布)";
  }
};


let nodeOfTreeBeingEdited: Node
// 编辑节点
const editOfTree = (node: Node, data: Tree) => {

  editingNodeOfTree.value = data; // 正在修改的节点
  isEditDialogVisibleOfTree.value = true;

  editNodeLabelOfTree.value = data.label
  nodeOfTreeBeingEdited = node
  isNodeEditable.value = data.disabled
};

// 修改节点的可修改性
const isNodeEditable = ref(true);

// 递归遍历节点子节点的isModel属性是否为真
const nodeHasSubModels = (node: Tree) => {
  if (node.children?.length){
    return node.children[0].isModel
  }
}

// 保存编辑
const saveEditOfTree = () => {

  if (
    !editNodeLabelOfTree.value ||
    !/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(editNodeLabelOfTree.value)
  ) {
    // console.log("data: ", data);
    ElMessage({
      message: "请输入有效的组件名称",
      type: "error",
    });
    return;
  } else {
    let formData = new FormData();
    if (editingNodeOfTree.value) {
      if(!isNodeEditable.value && editingNodeOfTree.value.disabled && editingNodeOfTree.value.children?.length){
        ElMessage.warning("无法将已经添加子节点的节点设置为最终类型节点")
        return
      }
      if (isNodeEditable.value && !editingNodeOfTree.value.disabled && editingNodeOfTree.value.children?.length ){
        ElMessage.warning("该节点类型下已经添加了模型，无法将其设为非最终类型节点")
        return
      }
      formData.append("treeName", editingNodeOfTree.value.value.split(".")[0]); // 树的根节点的名称
      formData.append("newNodeName", editNodeLabelOfTree.value); // 新节点的名称
      formData.append("nodeValue", editingNodeOfTree.value.value);
      formData.append("nodeType", isNodeEditable.value ? "node" : "leaf");
    } else {
      console.log("editingNodeOfTree is null");
      return;
    }

    api.post("user/edit_node_name/", formData).then((response: any) => {
      if (response.data.code === 200) {
        ElMessage({
          message: "修改成功",
          type: "success",
        });
        // 刷新树
        // getComponentTrees();
        if (nodeOfTreeBeingEdited) {
          nodeOfTreeBeingEdited.data.label = editNodeLabelOfTree.value;
          nodeOfTreeBeingEdited.data.disabled = isNodeEditable.value;
        }else{
          console.log("nodeOfTreeBeingEdited is null");
        }

        isEditDialogVisibleOfTree.value = false;
      } else {
        ElMessage({
          message: "修改失败，" + response.data.message,
        });
      }
    });
  }
};

// 关闭编辑对话框时清理状态
const handleCloseOfTree = () => {
  editingNodeOfTree.value = null;
  editNodeLabelOfTree.value = "";
};

// 递归过滤节点数据
const filterDataOfTree = (nodes: Tree[], keyword: string): Tree[] => {
  return nodes
    .filter((node) => node.label.toLowerCase().includes(keyword.toLowerCase())) // 匹配节点名称
    .map((node) => {
      // 递归过滤子节点
      if (node.children) {
        node.children = filterDataOfTree(node.children, keyword);
      }
      return node;
    });
};

// 处理搜索输入
watch(searchKeywordOfTree, (val) => {
  treeRef.value!.filter(val);
});

const filterNodeOfTree = (value: string, data: any) => {
  // if(props.userRole === 'superuser'){
    if (!value) return true;
    return data.label ? data.label.includes(value) : false;
  // }else{
  //   return false
  // }
  // if(props.userRole === 'user'){
  //   if (!value) {
  //     if (data.isModel && data.isPublished !== '已发布') {
  //       return false; // 未发布的叶子节点模型不显示
  //     }else {
  //       return true
  //     }
  //   }
  // }
};
</script>

<style scoped>
.custom-dialog {
  width: 30%;
  display: flex;
  flex-direction: column;
}

.custom-dialog .dialog-footer {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: right;
  align-items: flex-end;
}

.custom-dialog .dialog-footer .small-button {
  margin-left: 10px;
  width: 100px;
  padding: 8px 16px; /* Adjust padding to make buttons smaller */
}

.custom-tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
}

.node-actions {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-left: 8px;
}

.model-icon {
  width: 20px; 
  height: 20px;
}

.node-label {
  font-size: 17px
}
</style>
