<template>
  <div class="h-screen overflow-hidden flex flex-col bg-ice-white font-sans text-slate-800">
    <!-- Navbar / Branding -->
    <header class="bg-deep-blue text-white shadow-md z-40 sticky top-0 flex justify-between items-center px-6 py-3 border-b border-indigo-500/30">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-md bg-gradient-to-tr from-indigo-500 to-neon-cyan flex items-center justify-center font-black text-xl shadow-[0_0_10px_rgba(0,240,255,0.4)]">D</div>
        <div>
          <h1 class="text-xl font-bold tracking-wide">DeepBayes <span class="font-normal text-indigo-200 text-sm ml-2">通用多层概率评估系统</span></h1>
          <p class="text-xs text-indigo-300 -mt-1 tracking-wider uppercase">Hierarchical Bayesian Inference Engine</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <button @click="showSettingsModal = true" class="w-8 h-8 rounded-full bg-indigo-500/20 hover:bg-indigo-500/40 text-indigo-200 hover:text-white flex items-center justify-center transition-colors shadow-sm border border-indigo-400/30" title="智库与大模型配置 (RAG Settings)">
          <i class="fas fa-cog"></i>
        </button>
        <button @click="showHelpGuide = true" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-indigo-200 hover:text-white transition-colors" title="帮助与使用手册">
          <i class="fas fa-question"></i>
        </button>
        <span v-if="currentSamplingMode === 'fast'" class="px-2.5 py-1 rounded bg-amber-500/20 border border-amber-500/50 text-xs font-semibold text-amber-400 flex items-center shadow-inner">
          <i class="fas fa-bolt mr-1.5"></i> 快速预览
        </span>
        <span class="px-2.5 py-1 rounded bg-indigo-900/60 border border-indigo-700/50 text-xs font-semibold text-neon-cyan flex items-center shadow-inner">
          <span class="w-2 h-2 rounded-full bg-neon-cyan animate-pulse mr-2 shadow-[0_0_5px_#00f0ff]"></span> v1.0.4 Pro
        </span>
      </div>
    </header>

    <!-- Main Content Area with Transition -->
    <!-- 后端引擎初始化遮罩 -->
    <transition name="fade">
      <div v-if="!backendReady" class="fixed inset-0 bg-gradient-to-br from-[#0a192f] via-[#112240] to-[#0a192f] z-[200] flex flex-col justify-center items-center">
        <div class="relative w-20 h-20 mb-8">
          <div class="absolute inset-0 rounded-full border-2 border-neon-cyan/20"></div>
          <div class="absolute inset-0 rounded-full border-t-2 border-neon-cyan animate-spin"></div>
          <div class="absolute inset-3 rounded-full border-b-2 border-indigo-400 animate-spin" style="animation-direction:reverse;animation-duration:1.8s"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <i class="fas fa-atom text-2xl text-neon-cyan animate-pulse"></i>
          </div>
        </div>
        <h2 class="text-xl font-bold text-white mb-3 tracking-wide">推理引擎预热中</h2>
        <p class="text-sm text-slate-400 mb-6 max-w-sm text-center leading-relaxed">正在启动 PyMC 贝叶斯核心与概率张量图编译器，首次加载约需 5-10 秒...</p>
        <div class="flex items-center space-x-2 bg-white/5 px-4 py-2 rounded-full border border-white/10">
          <span class="w-1.5 h-1.5 rounded-full bg-neon-cyan animate-pulse"></span>
          <span class="text-xs font-mono text-slate-300">Initializing FastAPI Backend Engine...</span>
        </div>
      </div>
    </transition>

    <main class="flex-1 flex flex-col min-h-0 relative">
      <transition name="fade-slide" mode="out-in">
        <DataImporter v-if="currentStep === 'import'" class="overflow-y-auto flex-1 min-h-0" @health-check="openHealthCheck" />
        
        <div v-else-if="currentStep === 'inferencing'" class="absolute inset-0 flex flex-col justify-center items-center bg-ice-white bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white to-slate-50 z-10 p-10">
          <div class="relative w-24 h-24 flex items-center justify-center mb-8">
            <div class="absolute inset-0 rounded-full border-t-4 border-neon-cyan animate-spin opacity-80"></div>
            <div class="absolute inset-2 rounded-full border-b-4 border-indigo-600 animate-spin opacity-60" style="animation-direction: reverse; animation-duration: 1.5s;"></div>
            <i class="fas fa-brain text-4xl text-deep-blue"></i>
          </div>
          <h2 class="text-2xl font-black text-deep-blue tracking-tight mb-8">深度贝叶斯网络推演运算中...</h2>
          
          <!-- Progress Bar -->
          <div class="w-full max-w-2xl bg-white p-6 rounded-2xl shadow-xl border border-slate-200">
             <div class="flex justify-between text-xs font-bold text-slate-500 mb-2">
                 <span>算力推进状态</span>
                 <span class="text-indigo-600">{{ loadingProgress.toFixed(0) }}%</span>
             </div>
             <div class="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden mb-6">
                 <div class="bg-gradient-to-r from-neon-cyan to-indigo-600 h-2.5 rounded-full transition-all duration-300 ease-out" :style="{ width: loadingProgress + '%' }"></div>
             </div>
             
             <!-- Terminal Logs -->
             <div class="bg-[#0a192f] rounded-lg p-4 font-mono text-[11px] text-slate-300 h-40 overflow-y-auto shadow-inner flex flex-col space-y-2 relative">
                <div class="absolute inset-x-0 top-0 h-4 bg-gradient-to-b from-[#0a192f] to-transparent z-10"></div>
                <div v-for="tip in loadingTips" :key="tip.id" class="flex gap-3">
                   <span :class="{'text-emerald-400': tip.status==='done', 'text-amber-400 animate-pulse': tip.status==='loading'}" class="w-4 flex-shrink-0 text-center">
                     <i :class="tip.status === 'done' ? 'fas fa-check' : 'fas fa-cog fa-spin'"></i>
                   </span>
                   <span class="text-slate-500 w-12 flex-shrink-0">[{{ tip.time }}]</span>
                   <span :class="{'text-white': tip.status==='loading', 'text-slate-400': tip.status==='done'}">{{ tip.text }}</span>
                </div>
             </div>
          </div>
        </div>

        <VisualizationDashboard 
          v-else-if="currentStep === 'dashboard'" 
          :modelResults="inferenceResults" 
          :hierarchy-schema="currentHierarchy"
          :display-mapping="currentDisplayMapping"
          :raw-table-data="rawTableData"
          :target-variable="currentTarget"
          @reset="currentStep = 'import'"
        />
      </transition>
    </main>
    
    <!-- Acceleration Info Bar -->
    <div v-if="systemInfo && !systemInfo.has_gpu" class="bg-amber-50 border-t border-amber-200 px-6 py-1.5 flex justify-between items-center text-[10px] text-amber-700">
      <div class="flex items-center">
        <i class="fas fa-exclamation-triangle mr-2"></i>
        检测到未开启 GPU 加速。当前运行于 CPU 模式，对于超大规模模型推演建议下载扩展资源包。
      </div>
      <button 
        @click="installGPUPack" 
        :disabled="gpuInstallStatus === 'loading'"
        class="font-bold underline hover:text-amber-900 flex items-center"
      >
        <i v-if="gpuInstallStatus === 'loading'" class="fas fa-spinner fa-spin mr-2"></i>
        {{ gpuInstallStatus === 'loading' ? '正在安装国内强力资源包 (1GB+)...' : '获取 GPU 增强补丁' }}
      </button>
    </div>

    <!-- Global Footer -->
    <footer class="bg-white border-t border-slate-200 py-2 px-6 flex justify-between items-center text-xs text-slate-500 z-40">
      <div>
        &copy; 2026 DeepBayes Advanced Analytics. All rights reserved @ZR.
      </div>
      <div class="flex space-x-6">
        <span class="flex items-center">
          <i :class="systemInfo ? 'text-emerald-500 fas fa-server' : 'text-slate-300 fas fa-sync fa-spin'" class="mr-1.5"></i> 
          Backend: {{ systemInfo ? 'Connected' : 'Connecting...' }}
        </span>
        <span v-if="systemInfo" class="flex items-center"><i class="fas fa-rocket mr-1.5 text-indigo-500"></i> JAX Engine: {{ systemInfo.backend }}</span>
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
            :displayMapping="currentDisplayMapping"
            :samplingMode="currentSamplingMode"
            :customDraws="currentCustomDraws"
            :customTune="currentCustomTune"
            @close="showHealthCheckModal = false" 
            @proceed="startInference"
          />
        </div>
      </div>
    </transition>

    <!-- RAG & LLM Settings Modal -->
    <SettingsModal :show="showSettingsModal" @close="showSettingsModal = false" @config-saved="onConfigSaved" />

    <!-- 帮助与使用手册弹窗 (新版本) -->
    <HelpModal :show="showHelpGuide" @close="showHelpGuide = false" />

    <!-- GPU 安装中重型 Loading 遮罩 -->
    <div v-if="gpuInstallStatus === 'loading'" class="fixed inset-0 bg-slate-900/90 backdrop-blur-xl z-[100] flex flex-col justify-center items-center text-white p-12 text-center">
       <div class="relative w-32 h-32 mb-10">
         <div class="absolute inset-0 border-4 border-neon-cyan/20 rounded-full"></div>
         <div class="absolute inset-0 border-t-4 border-neon-cyan rounded-full animate-spin"></div>
         <div class="absolute inset-4 border-4 border-indigo-500/20 rounded-full animate-pulse" style="animation-duration: 3s"></div>
         <i class="fas fa-microchip text-5xl text-neon-cyan absolute inset-0 flex items-center justify-center"></i>
       </div>
       <h2 class="text-3xl font-black mb-4 tracking-tight">正在部署 GPU 硬件加速补丁</h2>
       <p class="max-w-md text-slate-400 text-sm leading-relaxed mb-8">
         我们正在检测您的本地环境，并通过 <span class="text-white font-bold">清华大学镜像源 (Tsinghua Tuna)</span> 异步拉取 1GB+ 的张量核心计算组件。这能为您带来 10x 以上的推演提速。
       </p>
       <div class="flex items-center space-x-3 bg-white/5 px-4 py-2 rounded-full border border-white/10 text-xs font-mono">
         <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
         同步进度：正在执行 `pip install jax[cuda12]`...
       </div>
       <p class="mt-10 text-[10px] text-slate-500 uppercase tracking-widest">请勿断开网络或关闭软件进程。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DataImporter from './components/DataImporter.vue';
import DataHealthCheck from './components/DataHealthCheck.vue';
import VisualizationDashboard from './components/VisualizationDashboard.vue';
import SettingsModal from './components/SettingsModal.vue';
import HelpModal from './components/HelpModal.vue';

const isProd = import.meta.env.PROD;
const API_BASE_URL = 'http://127.0.0.1:18521';

const currentStep = ref('import');
const showHealthCheckModal = ref(false);
const showSettingsModal = ref(false);
const backendReady = ref(false);  // 后端是否已就绪

const rawTableData = ref([]);
const currentHierarchy = ref([]);
const currentTarget = ref(null);
const inferenceResults = ref(null);
const currentDisplayMapping = ref({});
const currentSamplingMode = ref('fast');
const currentCustomDraws = ref(500);
const currentCustomTune = ref(300);
const showHelpGuide = ref(false);
const systemInfo = ref(null);
const gpuInstallStatus = ref('idle'); // idle, loading, success, error

const loadingProgress = ref(0);
const loadingTips = ref([]);
let progressInterval = null;
let logPollInterval = null;

// 轻量级健康检查：仅检测后端是否可访问
const checkBackendHealth = async () => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/health`, { signal: AbortSignal.timeout(2000) });
        if (res.ok) return true;
    } catch (e) { /* 后端尚未就绪 */ }
    return false;
};

const fetchSystemInfo = async () => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/system_info`);
        if (res.ok) {
            systemInfo.value = await res.json();
            return true;
        }
    } catch (e) { 
        console.warn("Backend not ready yet, retrying..."); 
    }
    return false;
};

// 启动时先等待后端就绪，再获取系统信息
const waitForBackend = async () => {
    const maxRetries = 40;  // 最多等 60 秒 (40 * 1.5s)
    for (let i = 0; i < maxRetries; i++) {
        const healthy = await checkBackendHealth();
        if (healthy) {
            backendReady.value = true;
            // 后端就绪后再获取详细系统信息（非阻塞）
            fetchSystemInfo();
            return;
        }
        await new Promise(r => setTimeout(r, 1500));
    }
    // 超时后仍然放行，让用户看到界面
    backendReady.value = true;
    console.error("Backend health check timed out after 60s");
};

const installGPUPack = async () => {
    if(!confirm("准备下载约 1.2GB 的 GPU 加速组件？国内下载可能需要 2-5 分钟。")) return;
    
    gpuInstallStatus.value = 'loading';
    try {
        const res = await fetch(`${API_BASE_URL}/api/install_gpu_pack`, { method: 'POST' });
        const data = await res.json();
        
        if (data.status === 'success') {
            gpuInstallStatus.value = 'success';
            alert("✅ GPU 增强驱动部署完成！\n\n为了使 CUDA 张量核心生效，请您立即手动重启 DeepBayes 软件。");
            window.location.reload(); // 简易重载预览，实际在 Tauri 中应引导重启
        } else {
            throw new Error(data.message);
        }
    } catch (e) {
        gpuInstallStatus.value = 'error';
        alert(`❌ 安装失败: ${e.message}\n请检查网络连接或尝试以管理员身份运行。`);
        gpuInstallStatus.value = 'idle';
    }
};

onMounted(() => {
    waitForBackend();
});

const onConfigSaved = (config) => {
    console.log("LLM Config Updated", config);
};

const openHealthCheck = (payload) => {
  rawTableData.value = payload.tableData;
  currentHierarchy.value = payload.hierarchy;
  currentTarget.value = payload.target;
  currentDisplayMapping.value = payload.displayMapping || {};
  currentSamplingMode.value = payload.samplingMode || 'fast';
  currentCustomDraws.value = payload.customDraws || 500;
  currentCustomTune.value = payload.customTune || 300;
  showHealthCheckModal.value = true;
};

const startInference = async (cleanSchema) => {
  showHealthCheckModal.value = false;
  currentStep.value = 'inferencing';
  
  loadingProgress.value = 0;
  loadingTips.value = [
    { id: 1, time: '0.0s', text: '正在初始化贝叶斯有向无环图 (DAG) 引擎...', status: 'done' },
    { id: 2, time: '...', text: '编译张量核心及构建对数似然梯度映射...', status: 'loading' }
  ];

  const startTime = Date.now();
  const speedMultiplier = cleanSchema.samplingMode === 'fast' ? 3 : 1;
  progressInterval = setInterval(() => {
    if(loadingProgress.value < 88) loadingProgress.value += Math.random() * 4 * speedMultiplier;
    
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
    if(loadingProgress.value > 30 && loadingTips.value.length === 2) {
       loadingTips.value[1].status = 'done';
       loadingTips.value[1].time = elapsed;
       loadingTips.value.push({ id: 3, time: '...', text: '启动 MCMC NUTS 并行马尔可夫链抽样 (耗时最长)...', status: 'loading' });
    }
    if(loadingProgress.value > 65 && !loadingTips.value.find(t => t.id === 4)) {
       const lastLoader = loadingTips.value.find(t => t.status === 'loading');
       if(lastLoader) { lastLoader.status = 'done'; lastLoader.time = elapsed; }
       loadingTips.value.push({ id: 4, time: '...', text: '核对 R_hat 收敛度并提取后验预测核密度 (PPC)...', status: 'loading' });
    }
  }, 400);

  // 独立轮询真实后端日志流
  logPollInterval = setInterval(async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/logs`);
      const data = await res.json();
      if(data.log) {
         // 防止日志过长刷屏，只找特定 ID 显示进度
         const existingLog = loadingTips.value.find(t => t.id === 'backend_log');
         const elapsed = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
         if(existingLog) {
            existingLog.text = "> " + data.log;
            existingLog.time = elapsed;
         } else {
            loadingTips.value.push({ id: 'backend_log', time: elapsed, text: "> " + data.log, status: 'loading' });
         }
      }
    } catch(e) {}
  }, 500);

  try {
    const response = await fetch(`${API_BASE_URL}/api/run_inference`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_name: '通用效能评估 (DeepBayes)',
        target_variable: cleanSchema.target,
        hierarchy: cleanSchema.hierarchy,
        raw_data: cleanSchema.tableData,
        sampling_mode: cleanSchema.samplingMode,
        custom_draws: cleanSchema.customDraws,
        custom_tune: cleanSchema.customTune
      })
    });
    
    if(!response.ok) throw new Error("后端计算失败");
    const data = await response.json();
    
    clearInterval(progressInterval);
    clearInterval(logPollInterval);
    loadingProgress.value = 100;
    const lastLoader = loadingTips.value.find(t => t.status === 'loading');
    if(lastLoader) {
        lastLoader.status = 'done';
        lastLoader.time = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
    }
    loadingTips.value.push({ id: 5, time: '完成', text: '参数矩阵装填完毕，即将开启全息控制台！', status: 'done' });
    
    setTimeout(() => {
        inferenceResults.value = data.results;
        currentStep.value = 'dashboard';
    }, 800);
    

  } catch (error) {
    console.error(error);
    clearInterval(progressInterval);
    clearInterval(logPollInterval);
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