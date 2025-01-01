<template>
  <el-tooltip :content="tooltip_text" placement="right" :hide-after="100" effect="light">
    <div
        class="drag-model-item"
        :style="dragModelItemStyle"
        @mouseenter="hover = true"
        @mouseleave="hover = false"
        @click="handleClick"
        :draggable="true"
    >
      <div class="content" :style="contentStyle" :class="{ hovered: hover }">
        <slot name="icon">
          <component v-if="icon" :is="icon" class="item-icon"/>
        </slot>
        <slot name="text">
          <!--          <span class="item-text" style="border: red solid 2px;">{{ text }}</span>-->
          <span class="item-text">{{ text }}</span>
        </slot>
      </div>
    </div>
  </el-tooltip>
</template>

<script setup>
import {ref, computed} from 'vue'

const props = defineProps({
  icon: {
    type: Object,
    default: null
  },
  text: {
    type: String,
    default: ''
  },
  tooltip_text: {
    type: String,
    default: ''
  },
  bgColor: {
    type: String,
    default: '#fefefe'
  },
  customStyles: {
    type: Object,
    default: () => ({})
  },
  contentStyle: {
    type: Object,
    default: () => ({})
  },
})

const emit = defineEmits(['click', 'dragend'])

const hover = ref(false)

const handleClick = () => {
  console.log("SquareItem handleClick 方法执行了......")
  emit('click')
}

const dragModelItemStyle = computed(() => ({
  backgroundColor: props.bgColor,
  ...props.customStyles
}))

const contentStyle = computed(() => ({
  ...props.contentStyle,
}))

</script>

<style scoped lang="scss">
.drag-model-item {
  display: flex;
  border: 1px solid #ddd;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s, opacity 0.5s;
  opacity: 0;
  animation: fadeIn 0.5s forwards;

  &:hover {
    transform: translateY(-2.5px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  &:active {
    transform: translateY(-5px) scale(0.95);
  }
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.content {
  display: flex;
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
  width: 100%;
  //background-color: #66e748;
  text-align: center;
  transition: transform 0.3s;

  /*&.hovered {
    transform: translate(1%, 1%) scale(1.05);
  }

  &.vertical-layout {
    flex-direction: column; !* 垂直布局时，图标和文字排列在同一列 *!
  }*/
}

.item-icon {
  font-size: 30px;
  color: #bdc4cd;
  transition: color 0.3s;
}

.item-text {
  display: block;
  margin-top: 2px;
  margin-left: 5px;
  font-size: 12px;
  color: #333;
  line-height: 1.1;
  white-space: normal;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
}

.drag-model-item:hover .item-icon {
  color: #66b1ff;
}
</style>
