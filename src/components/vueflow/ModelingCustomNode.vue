<script setup>
import {Handle, Position, useVueFlow} from '@vue-flow/core'
import {NodeToolbar} from '@vue-flow/node-toolbar'
import {NodeResizer} from '@vue-flow/node-resizer'
import {ref, nextTick} from "vue"
import { String } from 'lodash'
const {updateNodeData, removeNodes, findNode} = useVueFlow()

const props = defineProps(['id', 'data', 'userRole'])

// const actions = ['delete']
const actions = ['结果', '特征选择结果','相关系数矩阵热力图','连续样本指标变换','不同类型样本占比','原始信号波形图','总结论','详情']

// 编辑状态绑定到每个节点
const isEditing = ref(false)
const editedLabel = ref(props.data.label)
const inputRef = ref(null)
const emit = defineEmits(['showResults'])

//添加图标
// 建模区中各个算法节点的图标url
const setIconOfAlgorithms = (label) => {
  let iconName;
  switch (label) {
    case '插值处理':
      iconName = 'interpolation-icon.svg'
      break
    case '特征提取':
      iconName = 'extraction-icon.svg'
      break
    case '无量纲化':
      iconName = 'normalization-icon.svg'
      break
    case '特征选择':
      iconName = 'feature-selection-icon.svg'
      break
    case '小波变换':
      iconName = 'wavelet-icon.svg'
      break
    case '数据源':
      iconName = 'data-source-icon.svg'
      break
    case '故障诊断':
      iconName = 'fault-diagnosis-icon.svg'
      break
    case '故障预测':
      iconName = 'fault-prediction-icon.svg'
      break
    case '自定义模块':
      iconName = 'custom-module-icon.svg'
      break
    case '异常值检测':
      iconName = 'abnormal-detection-icon.svg'
      break
    case '层次分析模糊综合评估':
    case '层次逻辑回归评估':
    case '层次朴素贝叶斯评估':
    case '健康评估':
      iconName = 'health-evaluation-icon.svg'
  }
  return new URL(`../../assets/${iconName}`, import.meta.url).href
}
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

  let iconName;
  if (action === '结果')
    iconName = 'analysis-result-icon.svg'
    // return 'fa-solid fa-square-poll-vertical'
  else if (action === '特征选择结果')
    iconName = 'features-selection-result-icon.svg'
  else if (action === '相关系数矩阵热力图')
    iconName = 'heatmap-icon.svg'
  else if (action === '连续样本指标变换')
    iconName = 'indicators-trend-icon.svg'
  else if (action === '不同类型样本占比')
    iconName = 'pie-chart-icon.svg'
  else if (action === '原始信号波形图')
    iconName = 'waveform-icon.svg'
  else if (action === '总结论')
    iconName = 'summary-icon.svg'
  else if (action === '详情')
    iconName = 'details-icon.svg'
  else if(action){
    return 'fa-solid fa-magnet'
  }

  return new URL(`../../assets/${iconName}`, import.meta.url).href

}

//根据action来操作node
function updateNodeDataByAction(id, action) {
  emit('showResults', props,action)
}

function shouldShowIcon(props, action){
  if(props.data.laglabel === '数据源'){
    return false
  }else if(props.data.laglabel === '特征选择' && (action === '特征选择结果' | action === '相关系数矩阵热力图')){
    return true
  }else if((props.data.laglabel === '特征选择' | props.data.laglabel === '层次分析模糊综合评估' | props.data.laglabel == '层次朴素贝叶斯评估' | props.data.laglabel == '层次逻辑回归评估'| props.data.laglabel === '故障诊断') && action === '结果') {
    return false
  }else if(props.data.laglabel !== '数据源' && action === '结果') {
    return true
  // }else if(props.data.laglabel == '异常值检测' && action === '结果') {
  //   return false
  }else if((props.data.laglabel == '层次分析模糊综合评估' || props.data.laglabel == '层次朴素贝叶斯评估' || props.data.laglabel == '层次逻辑回归评估') && (action === '总结论' | action==='详情')) {
    return true
  }else if(props.data.laglabel == '故障诊断' && (action === '连续样本指标变换' | action==='不同类型样本占比' | action==='原始信号波形图')) {
    if (props.id.includes('deeplearning') && action === '连续样本指标变换')
      return false
    else 
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

<!--  <NodeToolbar :is-visible="data.toolbarVisible" :position="data.toolbarPosition">-->
<!--    <el-tooltip-->
<!--        v-for="action in actions"-->
<!--        :key="action"-->
<!--        class="box-item"-->
<!--        effect="dark"-->
<!--        :content="action"-->
<!--    placement="top-start"-->
<!--    >-->
<!--    <template #content>-->
<!--      {{ action }}-->
<!--    </template>-->
<!--    <button-->
<!--        v-if="shouldShowIcon(props, action)"-->
<!--        type="button"-->
<!--        :class="{ selected: action === data.action }"-->
<!--        @click="updateNodeDataByAction(props.id, action, props)"-->
<!--    >-->
<!--      <i v-if="shouldShowIcon(props, action)" :class="getIconClassByAction(action)"></i>-->

<!--    </button>-->
<!--    </el-tooltip>-->

<!--  </NodeToolbar>-->
  <!-- 删除按钮 -->
  <button class="delete-button" v-if="props.userRole == 'superuser'" @click="delete_button(id)">
    <i class="fa-solid fa-xmark"></i>
  </button>
  <div class="node-content">
    <div style="display: flex;flex-direction: row;justify-content: center;align-items: center;width: 100%;">
      <img style="height: 30px;width: 30px;" :src="setIconOfAlgorithms(data.laglabel)"
           alt="none"/>
      <span class="node-label" v-if="!isEditing">{{ data.label }}</span>
    </div>
    <div style="width: 100%;justify-content: right;align-items: center;display: flex;margin-right: 8px;padding: 0;">
      <div
          v-for="action in actions"
          :key="action"
      >
        <el-tooltip
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
              style="border: 0;padding: 0;background: white;margin: 5px;"
          >
            <!-- <i style="font-size: 30px;" v-if="shouldShowIcon(props, action)" :class="getIconClassByAction(action)"></i> -->
            <img style="height: 30px; width: 30px;" :src="getIconClassByAction(action)" alt="none"/>
          </button>
        </el-tooltip>
      </div>
    </div>
  </div>

  <Handle id="source-a" type="source" :position="Position.Right" class="custom-handle"/>
  <Handle id="source-b" type="source" :position="Position.Bottom" class="custom-handle"/>
  <Handle id="source-c" type="source" :position="Position.Left" class="custom-handle"/>
  <Handle id="source-d" type="source" :position="Position.Top" class="custom-handle"/>
</template>

<style scoped>

.custom-handle {
  background-color: #97c0ec;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  border: 2px solid #81c6db8a;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.delete-button{
  position: absolute;
  top: 3px;
  right: 3px;
  background: #ffffff;
  border: 0;
}
.node-content {
  font-family: 'JetBrains Mono', monospace;
  display: flex;
  flex-direction: column;
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