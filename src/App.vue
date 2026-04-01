<template>
  <div class="min-h-screen bg-slate-50 text-slate-800">
    <DataImporter v-if="currentStep === 'import'" @health-check="openHealthCheck" />

    <div v-if="showHealthCheckModal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex justify-center items-center z-50">
      <div class="w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-white rounded-xl shadow-2xl">
        <DataHealthCheck 
          :hierarchy="currentHierarchy" 
          :targetVariable="currentTarget" 
          :tableData="rawTableData"
          @close="showHealthCheckModal = false" 
          @proceed="startInference"
        />
      </div>
    </div>

    <div v-if="currentStep === 'inferencing'" class="min-h-screen flex flex-col justify-center items-center">
      <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-indigo-600 mb-4"></div>
      <h2 class="text-xl font-bold text-slate-700">正在调用高算力节点执行 NUTS 采样...</h2>
      <p class="text-slate-500 mt-2">《视频侦查技术》多层效能网络推演中</p>
    </div>

    <VisualizationDashboard 
      v-if="currentStep === 'dashboard'" 
      :modelResults="inferenceResults" 
      :hierarchySchema="currentHierarchy"
      @reset="currentStep = 'import'"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DataImporter from './components/DataImporter.vue';
import DataHealthCheck from './components/DataHealthCheck.vue';
import VisualizationDashboard from './components/VisualizationDashboard.vue';

const currentStep = ref('import');
const showHealthCheckModal = ref(false);

const rawTableData = ref([]);
const currentHierarchy = ref([]);
const currentTarget = ref(null);
const inferenceResults = ref(null);

const openHealthCheck = (payload) => {
  rawTableData.value = payload.tableData;
  currentHierarchy.value = payload.hierarchy;
  currentTarget.value = payload.target;
  showHealthCheckModal.value = true;
};

const startInference = async (cleanSchema) => {
  showHealthCheckModal.value = false;
  currentStep.value = 'inferencing';
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/run_inference', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_name: '通用效能评估',
        target_variable: cleanSchema.target,
        hierarchy: cleanSchema.hierarchy,
        raw_data: rawTableData.value
      })
    });
    
    if(!response.ok) throw new Error("后端计算失败");
    const data = await response.json();
    
    inferenceResults.value = data.results;
    currentStep.value = 'dashboard';

  } catch (error) {
    console.error(error);
    alert("推理失败，请检查后端 FastAPI 服务是否启动。");
    currentStep.value = 'import';
  }
};
</script>