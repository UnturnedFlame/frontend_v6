<template>
  <div :class="['my-collapse', theme]" :style="{ backgroundColor: background }">
    <slot/>
  </div>
</template>

<script>
import {defineComponent, provide, reactive, toRefs} from "vue";

export default defineComponent({
  name: "MyCollapse",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    accordion: {
      type: Boolean,
      default: false,
    },
    theme: {
      type: String,
      default: "light", // 'light' 或 'dark'
    },
    background: {
      type: String,
      default: "#ebeef4", // 背景色
    },
  },
  emits: ["update:modelValue", "item-click"],
  setup(props, {emit}) {
    const state = reactive({
      activeItems: props.modelValue,
    });

    const toggle = (data) => { // 接收 data 对象
      const name = data.name;
      let newValue = [...state.activeItems];
      if (props.accordion) {
        newValue = newValue[0] === name ? [] : [name];
      } else {
        const index = newValue.indexOf(name);
        if (index > -1) {
          newValue.splice(index, 1);
        } else {
          newValue.push(name);
        }
      }
      state.activeItems = newValue;
      emit("update:modelValue", newValue);
      emit("item-click", data); // 传递整个 data 对象
    };

    provide("collapseState", {
      activeItems: toRefs(state).activeItems,
      toggle,
    });

    return {...toRefs(state)};
  },
});
</script>

<style scoped>
.my-collapse.light {
  border: 1px solid #ebeef4;
  border-radius: 4px;
  width: 100%;
  /*overflow: hidden;*/
}

.my-collapse.dark {
  border: 1px solid #444;
  border-radius: 4px;
  /*overflow: hidden;*/
  color: #fff;
  width: 100%;
}
</style>