<template>
  <div :class="['my-collapse-item', { disabled }]" :style="{ backgroundColor: itemBackground }">
    <div
        class="my-collapse-header"
        @click="handleClick"
        :style="{ cursor: disabled ? 'not-allowed' : 'pointer' }"
    >
      <slot name="title"/>
      <span
          class="arrow"
          :class="{ rotated: isActive }"
          :style="arrowStyle"
      >
        <slot name="arrow" :isActive="isActive">
          <!-- 默认没有图标 -->
        </slot>
      </span>
    </div>
    <transition name="collapse-transition">
      <div v-show="isActive" class="my-collapse-content">
        <slot/>
      </div>
    </transition>
  </div>
</template>

<script>
import {defineComponent, inject, computed} from "vue";

export default defineComponent({
  name: "MyCollapseItem",
  props: {
    data: { // 统一使用 data 属性，包含 name 和其他自定义数据
      type: Object,
      required: true,
      validator: (value) => {
        return 'name' in value;
      },
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    arrowColor: {
      type: String,
      default: "#000", // 箭头颜色
    },
    itemBackground: {
      type: String,
      default: "#ffffff", // 子项背景色
    },
  },
  setup(props, {emit}) {
    const collapseState = inject("collapseState");

    const isActive = computed(() =>
        collapseState.activeItems.value.includes(props.data.name)
    );

    const arrowStyle = computed(() => ({
      color: props.arrowColor,
    }));

    const handleClick = () => {
      if (!props.disabled) {
        collapseState.toggle(props.data); // 传递 data 对象
      }
      emit("click");
    };

    return {isActive, arrowStyle, handleClick};
  },
});
</script>

<style scoped>
.my-collapse-item {
  border-bottom: 1px solid #e4e7ed;
  transition: background-color 1s ease;
}

.my-collapse-header {
  display: flex;
  border-bottom: 1px solid #e4e7ed;
  justify-content: space-between;
  align-items: center;
  /*padding: 12px;*/
  user-select: none;
}

.my-collapse-header:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.my-collapse-content {
  padding: 0;
  /* 添加一些内边距使内容更美观 */
}

.my-collapse-item.disabled .my-collapse-header {
  color: #bcbcbc;
}

.arrow {
  transition: transform 1s ease, color 1s ease;
  display: inline-block;
  transform: rotate(0deg);
}

/* 优化过渡动画 */
.collapse-transition {
  transition: max-height 1s ease, padding 1s ease;
  overflow: hidden;
}
</style>