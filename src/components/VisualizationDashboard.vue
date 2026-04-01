<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6 bg-white p-4 rounded-lg shadow-sm">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">多层效能网络推断报告</h1>
        <p class="text-sm text-gray-500">已识别实际效能远超预期的亮点，及资源转化低下的暗点</p>
      </div>
      <button @click="$emit('reset')" class="px-4 py-2 text-sm text-white bg-indigo-600 rounded hover:bg-indigo-700">
        重新导入数据
      </button>
    </div>

    <div class="grid grid-cols-2 gap-6">
      <div class="bg-white p-5 rounded-lg shadow-sm h-[500px] flex flex-col">
        <h2 class="text-lg font-bold mb-2">期望效能 vs 实际偏差 (散点图)</h2>
        <div ref="scatterChartRef" class="flex-1 w-full"></div>
      </div>

      <div class="bg-white p-5 rounded-lg shadow-sm h-[500px] flex flex-col">
        <h2 class="text-lg font-bold mb-2">协变量驱动力归因 (森林图)</h2>
        <div ref="forestChartRef" class="flex-1 w-full"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, shallowRef } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  modelResults: { type: Object, required: true },
  hierarchySchema: { type: Array, required: true }
});

const scatterChartRef = ref(null);
const forestChartRef = ref(null);
const charts = shallowRef({});

onMounted(() => {
  charts.value.scatter = echarts.init(scatterChartRef.value);
  charts.value.forest = echarts.init(forestChartRef.value);
  if (props.modelResults) renderAll();
  window.addEventListener('resize', () => Object.values(charts.value).forEach(c => c && c.resize()));
});

watch(() => props.modelResults, (newVal) => { if(newVal) renderAll(); }, { deep: true });

const renderAll = () => {
  renderScatter(props.modelResults.performance_data);
  renderForest(props.modelResults.summary_df);
};

const renderScatter = (data) => {
  const parsedData = data.map(d => [d.Expected, d.Deviation, d.NodeName, d.Actual]);
  // 此处动态阈值可由后端传入，为确保视觉效果暂设固定偏移值
  const threshold = 1.0; 
  
  charts.value.scatter.setOption({
    tooltip: { formatter: (p) => `${p.value[2]}<br/>期望: ${p.value[0].toFixed(2)}<br/>偏差: ${p.value[1].toFixed(2)}` },
    xAxis: { type: 'value', name: '模型期望值' },
    yAxis: { type: 'value', name: '实际偏差 (Deviation)' },
    visualMap: {
      show: false, dimension: 1,
      pieces: [{ min: threshold, color: '#eab308' }, { max: -threshold, color: '#0f172a' }],
      outOfRange: { color: '#cbd5e1' }
    },
    series: [{ type: 'scatter', symbolSize: (d) => Math.abs(d[1]) > threshold ? 16 : 8, data: parsedData }]
  });
};

const renderForest = (summaryDf) => {
  const effectData = Object.entries(summaryDf)
    .filter(([k]) => k.startsWith('beta_'))
    .map(([k, v]) => [k.replace('beta_', ''), v['hdi_3%'], v['mean'], v['hdi_97%']]);

  charts.value.forest.setOption({
    tooltip: { formatter: (p) => `${p.value[0]}: ${p.value[2].toFixed(3)}` },
    xAxis: { type: 'value', name: '影响系数 (Effect Size)' },
    yAxis: { type: 'category', data: effectData.map(d => d[0]), inverse: true },
    series: [
      {
        type: 'custom',
        renderItem: (params, api) => {
          const y = api.coord([0, api.value(0)])[1];
          return {
            type: 'group',
            children: [
              { type: 'line', shape: { x1: api.coord([api.value(1),0])[0], y1: y, x2: api.coord([api.value(3),0])[0], y2: y }, style: { stroke: '#4f46e5', lineWidth: 3 } },
              { type: 'circle', shape: { cx: api.coord([api.value(2),0])[0], cy: y, r: 6 }, style: { fill: '#fff', stroke: '#4f46e5', lineWidth: 2 } }
            ]
          };
        },
        data: effectData
      }
    ]
  });
};
</script>