<template>
  <div class="min-h-screen flex flex-col bg-ice-white font-sans text-slate-800">
    <!-- Navbar / Branding -->
    <header class="bg-deep-blue text-white shadow-md z-40 sticky top-0 flex justify-between items-center px-6 py-3 border-b border-indigo-500/30">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-md bg-gradient-to-tr from-indigo-500 to-neon-cyan flex items-center justify-center font-black text-xl shadow-[0_0_10px_rgba(0,240,255,0.4)]">D</div>
        <div>
          <h1 class="text-xl font-bold tracking-wide">DeepBayes <span class="font-normal text-indigo-200 text-sm ml-2">通用多层概率评估系统</span></h1>
          <p class="text-xs text-indigo-300 -mt-1 tracking-wider uppercase">Hierarchical Bayesian Inference Engine</p>
        </div>
      </div>
      <div class="flex items-center space-x-4">
        <span class="px-2.5 py-1 rounded bg-indigo-900/60 border border-indigo-700/50 text-xs font-semibold text-neon-cyan flex items-center shadow-inner">
          <span class="w-2 h-2 rounded-full bg-neon-cyan animate-pulse mr-2 shadow-[0_0_5px_#00f0ff]"></span> V2.0 Pro
        </span>
      </div>
    </header>

    <!-- Main Content Area with Transition -->
    <main class="flex-1 overflow-auto relative">
      <transition name="fade-slide" mode="out-in">
        <DataImporter v-if="currentStep === 'import'" @health-check="openHealthCheck" />
        
        <div v-else-if="currentStep === 'inferencing'" class="absolute inset-0 flex flex-col justify-center items-center bg-ice-white bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white to-slate-100 z-10">
          <div class="relative w-24 h-24 flex items-center justify-center mb-6">
            <div class="absolute inset-0 rounded-full border-t-4 border-neon-cyan animate-spin opacity-80"></div>
            <div class="absolute inset-2 rounded-full border-b-4 border-indigo-600 animate-spin opacity-60" style="animation-direction: reverse; animation-duration: 1.5s;"></div>
            <i class="fas fa-brain text-4xl text-deep-blue"></i>
          </div>
          <h2 class="text-2xl font-black text-deep-blue tracking-tight">正在解析 N 维张量网络...</h2>
          <p class="text-slate-500 mt-3 flex items-center">
            <i class="fas fa-microchip mr-2"></i> 核心推演引擎 MCMC NUTS 采样启动
          </p>
        </div>

        <VisualizationDashboard 
          v-else-if="currentStep === 'dashboard'" 
          :modelResults="inferenceResults" 
          :hierarchySchema="currentHierarchy"
          @reset="currentStep = 'import'"
        />
      </transition>
    </main>

    <!-- Global Footer -->
    <footer class="bg-white border-t border-slate-200 py-2 px-6 flex justify-between items-center text-xs text-slate-500 z-40">
      <div>
        &copy; 2026 DeepBayes Advanced Analytics. All rights reserved.
      </div>
      <div class="flex space-x-6">
        <span class="flex items-center"><i class="fas fa-server mr-1.5 text-emerald-500"></i> Backend: Connected</span>
        <span class="flex items-center"><i class="fas fa-rocket mr-1.5 text-indigo-500"></i> JAX/Numpyro Engine: Active</span>
        <span class="flex items-center"><i class="fas fa-layer-group mr-1.5 text-blue-500"></i> Max MCMC Chains: 4</span>
      </div>
    </footer>

    <!-- Modals -->
    <transition name="fade">
      <div v-if="showHealthCheckModal" class="fixed inset-0 bg-deep-blue/40 backdrop-blur-md flex justify-center items-center z-50">
        <div class="w-full max-w-5xl max-h-[90vh] overflow-hidden bg-white rounded-xl shadow-[0_20px_50px_rgba(10,25,47,0.3)] flex flex-col">
          <DataHealthCheck 
            :hierarchy="currentHierarchy" 
            :targetVariable="currentTarget" 
            :tableData="rawTableData"
            @close="showHealthCheckModal = false" 
            @proceed="startInference"
          />
        </div>
      </div>
    </transition>
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
        project_name: '通用效能评估 (DeepBayes)',
        target_variable: cleanSchema.target,
        hierarchy: cleanSchema.hierarchy,
        raw_data: cleanSchema.tableData
      })
    });
    
    if(!response.ok) throw new Error("后端计算失败");
    const data = await response.json();
    
    inferenceResults.value = data.results;
    currentStep.value = 'dashboard';

  } catch (error) {
    console.error(error);
    alert("推理失败，请检查后端 FastAPI 服务是否启动或数据格式是否存在严重错误。");
    currentStep.value = 'import';
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

body {
  font-family: 'Inter', sans-serif;
  margin: 0;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>