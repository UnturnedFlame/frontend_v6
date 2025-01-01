<script setup>
import {Handle, Position, useVueFlow} from '@vue-flow/core'
import {NodeToolbar} from '@vue-flow/node-toolbar'
import {NodeResizer} from '@vue-flow/node-resizer'
import {ref, nextTick} from "vue"
const {updateNodeData, removeNodes, findNode} = useVueFlow()

const props = defineProps(['id', 'data'])

// const actions = ['delete']
const actions = ['结果', '特征选择结果','相关系数矩阵热力图','连续样本指标变换','不同类型样本占比','原始信号波形图','总结论','详情']

// 编辑状态绑定到每个节点
const isEditing = ref(false)
const editedLabel = ref(props.data.label)
const inputRef = ref(null)
const emit = defineEmits(['showResults'])
// 切换编辑状态
function toggleEdit(event) {
  isEditing.value = !isEditing.value
  if (isEditing.value) {
    nextTick(() => {
      if (inputRef.value) {
        inputRef.value.focus()  // 聚焦到输入框
      }
    })
    // 禁用拖动
    //let node = findNode(props.id)
    //node.draggable = false
  } else {
    // 恢复拖动
    //updateNodeData(props.id, {draggable: true})
    //let node = findNode(props.id)
    //node.draggable = true
  }
  event.stopPropagation()
}

// 保存编辑后的文本
function saveEdit() {
  updateNodeData(props.id, {label: editedLabel.value})
  isEditing.value = false
  // 退出编辑时恢复拖动
  // updateNodeData(props.id, {draggable: true})
  //let node = findNode(props.id)
  //node.draggable = true
}

function getIconClassByAction(action) {
  if (action === '结果')
    return `fa-solid fa-square-poll-vertical`
  if (action === '特征选择结果')
    return 'fa-solid fa-square-poll-vertical'
  if (action === '相关系数矩阵热力图')
    return 'fa-solid fa-magnet'
  if (action){
    return 'fa-solid fa-magnet'
  }

}

//根据action来操作node
function updateNodeDataByAction(id, action) {
  emit('showResults', props,action)
}

function shouldShowIcon(props, action){
  if(props.data.laglabel === '数据源' ){
    return false
  }else if(props.data.laglabel === '特征选择' && (action === '特征选择结果' | action === '相关系数矩阵热力图')){
    return true
  }else if((props.data.laglabel === '特征选择' | props.data.laglabel === '层次分析模糊综合评估'| props.data.laglabel === '故障诊断') && action === '结果') {
    return false
  }else if(props.data.laglabel !== '数据源' && action === '结果') {
    return true
  }else if(props.data.laglabel == '层次分析模糊综合评估' && (action === '总结论' | action==='详情')) {
    return true
  }
  else if(props.data.laglabel == '故障诊断' && (action === '连续样本指标变换' | action==='不同类型样本占比' | action==='原始信号波形图')) {
    return true
  }
}

// 防止输入框点击时触发父级的双击事件
function preventClick(event) {
  event.stopPropagation()
}

//删除
function delete_button(id){
  removeNodes(id)
}
</script>

<template>
  <NodeResizer :is-visible="true" min-width="100" min-height="30" :color="'#ccd0d6'"
               :handle-style="{width: 0, height: 0,background: '#ccd0d6'}"/>

  <NodeToolbar :is-visible="data.toolbarVisible" :position="data.toolbarPosition">
    <el-tooltip
        v-for="action in actions"
        :key="action"
        class="box-item"
        effect="dark"
        :content="action"
    placement="top-start"
    >
    <template #content>
      {{ action }}
    </template>
    <button
        v-if="shouldShowIcon(props, action)"
        type="button"
        :class="{ selected: action === data.action }"
        @click="updateNodeDataByAction(props.id, action, props)"
    >
      <i v-if="shouldShowIcon(props, action)" :class="getIconClassByAction(action)"></i>

    </button>
    </el-tooltip>

  </NodeToolbar>
  <!-- 删除按钮 -->
  <button class="delete-button" @click="delete_button(id)">
    <i class="fa-solid fa-xmark"></i>
  </button>
  <div class="node-content">
    <span class="node-label" v-if="!isEditing">{{ data.label }}</span>
  </div>

  <Handle id="source-a" type="source" :position="Position.Right"/>
  <Handle id="source-b" type="source" :position="Position.Bottom"/>
  <Handle id="source-c" type="source" :position="Position.Left"/>
  <Handle id="source-d" type="source" :position="Position.Top"/>
</template>

<style scoped>
.delete-button{
  position: absolute;
  top: 0;
  right: 0;
}
.node-content {
  font-family: 'JetBrains Mono', monospace;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.node-label {
  font-size: 30px;
  color: #333;
}

.node-input {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  border: 1px solid #ccd0d6;
  border-radius: 5px;
  padding: 5px 10px;
  width: 100%;
  height: 100%;
  outline: none;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
}

.node-input:focus {
  border-color: #0099ff;
  background-color: #fff;
  box-shadow: 0 0 5px rgba(0, 153, 255, 0.5);
}

.action-button {
  background-color: #ffffff;
  border: 1px solid #ccd0d6;
  border-radius: 8px;
  padding: 6px 12px;
  margin: 0 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.action-button:hover {
  background-color: #f0f0f0;
  box-shadow: 0 0 5px rgba(0, 153, 255, 0.5);
}

.action-button.selected {
  background-color: #e0f7ff;
  border-color: #0099ff;
}
</style>