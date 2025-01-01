<template>
  <el-popconfirm
    width="220"
    :icon="InfoFilled"
    icon-color="#626AEF"
    title="Are you sure to delete this?"
    @cancel="onCancel"
  >
    <template #reference>
      <el-button>Delete</el-button>
    </template>
    <template #actions="{ confirm, cancel }">
      <el-row>
        <el-col :span="12"
          ><el-button size="small" @click="cancel">取消</el-button></el-col
        >
        <el-col :span="12">
          <el-button type="primary" size="small" @click="confirm"> 确定 </el-button>
        </el-col>
      </el-row>
    </template>
  </el-popconfirm>

  <el-select
    v-model="value"
    placeholder="Select"
    size="large"
    style="width: 240px"
    popper-class="select"
  >
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
  <p>sdawdas</p>
  <div>sdwassssssssssssss</div>
  <div id="ssd" style="width: 500px; height: 400px"></div>
</template>

<script setup lang="ts">
import { nextTick, ref } from "vue";
import { InfoFilled } from "@element-plus/icons-vue";
import * as echarts from "echarts";

// 基于准备好的dom，初始化echarts实例
// var myChart = echarts.init(document.getElementById("main"));
// // 绘制图表
// myChart.setOption({
//   title: {
//     text: "ECharts 入门示例",
//   },
//   tooltip: {},
//   xAxis: {
//     data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
//   },
//   yAxis: {},
//   series: [
//     {
//       name: "销量",
//       type: "bar",
//       data: [5, 20, 36, 10, 10, 20],
//     },
//   ],
// });

// 基于准备好的dom，初始化echarts实例
nextTick(() => {
  let myChart = echarts.init(document.getElementById("ssd"));

  // 指定图表的配置项和数据
  let option = {
    title: {
      text: "ECharts 入门示例",
    },
    tooltip: {},
    legend: {
      data: ["销量"],
    },
    xAxis: {
      data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
    },
    yAxis: {},
    series: [
      {
        name: "销量",
        type: "bar",
        data: [5, 20, 36, 10, 10, 20],
      },
    ],
  };
  
  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
});


const clicked = ref(false);
function onCancel() {
  clicked.value = true;
}

const value = ref("");

const options = [
  {
    value: "Option1",
    label: "Option1",
  },
  {
    value: "Option2",
    label: "Option2",
  },
  {
    value: "Option3",
    label: "Option3",
  },
  {
    value: "Option4",
    label: "Option4",
  },
  {
    value: "Option5",
    label: "Option5",
  },
];
</script>
