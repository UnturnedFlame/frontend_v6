<script setup>
import {BaseEdge, EdgeLabelRenderer, getBezierPath, useVueFlow} from '@vue-flow/core'
import {computed} from 'vue'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  sourceX: {
    type: Number,
    required: true,
  },
  sourceY: {
    type: Number,
    required: true,
  },
  targetX: {
    type: Number,
    required: true,
  },
  targetY: {
    type: Number,
    required: true,
  },
  sourcePosition: {
    type: String,
    required: true,
  },
  targetPosition: {
    type: String,
    required: true,
  },
  markerEnd: {
    type: String,
    required: false,
  },
  style: {
    type: Object,
    required: false,
  },
  removeBtnDisabled: {
    type: Boolean,
    required: false,
  }
})

const {removeEdges} = useVueFlow()

const path = computed(() => getBezierPath(props))

// 定义自定义样式对象
const customStyle = computed(() => ({
  stroke: '#738eac', // 连线颜色
  strokeWidth: '3px', // 连线宽度
  strokeDasharray: '5, 5', // 虚线样式
  transition: 'stroke 0.3s ease', // 过渡效果
}))
</script>

<script>
export default {
  inheritAttrs: false,
}
</script>

<template>
  <!-- You can use the `BaseEdge` component to create your own custom edge more easily -->
  <!-- <BaseEdge :id="id" :style="style" :path="path[0]" :marker-end="markerEnd"/> -->
  <BaseEdge :id="id" :style="customStyle" :path="path[0]" :marker-end="markerEnd"/>

  <!-- Use the `EdgeLabelRenderer` to escape the SVG world of edges and render your own custom label in a `<div>` ctx -->
  <EdgeLabelRenderer>
    <div
        :style="{
        pointerEvents: 'all',
        position: 'absolute',
        transform: `translate(-50%, -50%) translate(${path[1]}px,${path[2]}px)`,
      }"
        class="nodrag nopan"
    >
      <button :disabled="removeBtnDisabled" class="edgebutton" @click="removeEdges(id)">×</button>
    </div>
  </EdgeLabelRenderer>
</template>

<style scoped>
.custom-edge {
  stroke: #3c4d61; /* 连线颜色 */
  stroke-width: 2px; /* 连线宽度 */
  stroke-dasharray: 5, 5; /* 虚线样式 */
  transition: stroke 0.3s ease; /* 过渡效果 */
}

.custom-edge:hover {
  stroke: #0056b3; /* 鼠标悬停时的颜色 */
}
</style>
