<template>
  <div class="h-screen overflow-hidden flex flex-col bg-ice-white font-sans text-slate-800">
    <!-- 全局导航栏 -->
    <header class="bg-[#0b1121] text-white z-40 sticky top-0 flex items-center px-8 py-0 border-b border-white/5 shadow-2xl shadow-black/20">
      <!-- 缓慢漂移的环境光效 -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-24 -left-24 w-96 h-96 bg-indigo-600/10 rounded-full blur-[120px] animate-[drift_12s_ease-in-out_infinite]"></div>
        <div class="absolute -bottom-32 -right-16 w-80 h-80 bg-cyan-500/8 rounded-full blur-[100px] animate-[drift_15s_ease-in-out_infinite_reverse]"></div>
      </div>
      <!-- 背景微纹点阵 -->
      <div class="absolute inset-0 opacity-[0.04]" style="background-image: radial-gradient(circle at 1px 1px, rgba(99,102,241,0.8) 1px, transparent 0); background-size: 20px 20px;"></div>
      <!-- 浮动微粒子 -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <div class="absolute w-1 h-1 bg-indigo-400/60 rounded-full top-1/4 left-[15%] animate-[floatUp_8s_ease-in-out_infinite]"></div>
        <div class="absolute w-[3px] h-[3px] bg-cyan-400/50 rounded-full top-1/3 left-[35%] animate-[floatUp_11s_ease-in-out_infinite_1s]"></div>
        <div class="absolute w-[2px] h-[2px] bg-indigo-300/40 rounded-full top-1/2 left-[55%] animate-[floatUp_9s_ease-in-out_infinite_2s]"></div>
        <div class="absolute w-1 h-1 bg-cyan-300/50 rounded-full top-[30%] left-[75%] animate-[floatUp_13s_ease-in-out_infinite_0.5s]"></div>
        <div class="absolute w-[2px] h-[2px] bg-indigo-500/40 rounded-full top-[20%] left-[90%] animate-[floatUp_10s_ease-in-out_infinite_3s]"></div>
      </div>
      <!-- 底部动态发光条 -->
      <div class="absolute inset-x-0 bottom-0 h-[2px]">
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-50"></div>
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent opacity-30 blur-sm animate-[glowShift_4s_ease-in-out_infinite]"></div>
      </div>
      <!-- 角落装饰 -->
      <div class="absolute top-0 left-0 w-3 h-3 border-t-[2px] border-l-[2px] border-indigo-500/20 rounded-tl"></div>
      <div class="absolute top-0 right-0 w-3 h-3 border-t-[2px] border-r-[2px] border-cyan-500/20 rounded-tr"></div>
      
      <!-- 左侧：品牌 -->
      <div class="flex items-center gap-5 py-4 relative z-10">
        <!-- Logo 徽标 -->
        <div class="relative shrink-0 group/logo">
          <!-- 多层辉光 -->
          <div class="absolute -inset-3 rounded-2xl bg-gradient-to-br from-indigo-500/15 to-cyan-500/10 blur-2xl animate-[pulseGlow_4s_ease-in-out_infinite]"></div>
          <div class="absolute -inset-2 rounded-2xl bg-gradient-to-br from-indigo-600/25 to-cyan-500/15 blur-xl group-hover/logo:blur-2xl transition-all duration-700"></div>
          <!-- 主体 -->
          <div class="relative w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-600 via-indigo-500 to-cyan-500 flex items-center justify-center shadow-2xl shadow-indigo-500/30 ring-1 ring-white/10 overflow-hidden group-hover/logo:scale-105 transition-transform duration-500">
            <div class="absolute inset-0 bg-gradient-to-tr from-indigo-600/50 to-transparent"></div>
            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-white/5 to-transparent translate-y-[60%] group-hover/logo:translate-y-[0%] transition-transform duration-700"></div>
            <span class="relative text-2xl font-black tracking-tighter" style="font-family: 'Inter', sans-serif; background: linear-gradient(180deg, #e0f2fe, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 8px rgba(99,102,241,0.4));">B</span>
          </div>
          <!-- 状态指示点 -->
          <div class="absolute -top-1 -right-1">
            <div class="w-3 h-3 bg-emerald-400 rounded-full border-2 border-[#0b1121] shadow-lg shadow-emerald-400/50 relative">
              <div class="absolute inset-0 rounded-full bg-emerald-400 animate-[pulse-dot_2s_ease-in-out_infinite]"></div>
            </div>
          </div>
        </div>
        
        <!-- 品牌文字 -->
        <div>
          <div class="flex items-baseline gap-2 flex-wrap">
            <h1 class="group/title relative">
              <span class="text-xl font-extrabold tracking-tight" style="font-family: 'Inter', 'Segoe UI', sans-serif;">
                <span class="text-white">Deep</span>
                <span class="bg-gradient-to-r from-indigo-400 via-cyan-400 to-indigo-300 bg-clip-text text-transparent bg-[length:200%_auto] animate-[gradientShift_4s_ease-in-out_infinite]">Bayes</span>
              </span>
              <!-- 标题底部辉光 -->
              <span class="absolute -bottom-1 left-0 w-full h-px bg-gradient-to-r from-indigo-500/40 via-cyan-400/40 to-transparent opacity-0 group-hover/title:opacity-100 transition-opacity duration-500"></span>
            </h1>
            <span class="text-[10px] font-bold tracking-wider px-2 py-0.5 rounded-md bg-white/8 border border-white/10 text-indigo-300/90 hover:bg-white/12 transition-colors select-none" title="版本号">v1.0.8</span>
          </div>
          <div class="flex items-center gap-2 mt-1.5">
            <span class="text-sm font-semibold text-slate-400 tracking-wide"><span class="inline-block w-1 h-1 rounded-full bg-indigo-400/60 mr-2 align-middle shadow-sm shadow-indigo-400/30"></span>贝叶斯层次网络分析平台</span>
            <span class="w-px h-3.5 bg-white/10"></span>
            <span class="relative flex items-center gap-1.5">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" :class="systemInfo ? 'bg-emerald-400' : 'bg-slate-600'" style="animation-duration: 1.5s;"></span>
                <span class="relative inline-flex rounded-full h-2 w-2" :class="systemInfo ? 'bg-emerald-500 shadow-sm shadow-emerald-500/50' : 'bg-slate-500'"></span>
              </span>
              <span class="text-[11px] text-slate-500 font-medium tracking-wide">{{ systemInfo ? '推理引擎就绪' : '引擎启动中...' }}</span>
            </span>
          </div>
        </div>
      </div>
      <!-- 右侧：操作区 -->
      <div class="flex items-center gap-2 ml-auto relative z-10">
        <span v-if="currentSamplingMode === 'fast'" class="h-7 px-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-[11px] font-semibold text-amber-400 flex items-center gap-1.5">
          <i class="fas fa-bolt text-[10px]"></i>快速
        </span>
        <div class="w-px h-5 bg-white/10 mx-1"></div>
        <button @click="showHelpGuide = true" class="h-9 px-3.5 text-[12px] font-medium text-slate-400 hover:text-white hover:bg-white/5 rounded-xl transition-all flex items-center gap-2 group relative overflow-hidden">
          <span class="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-indigo-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></span>
          <i class="fas fa-book-open relative text-slate-500 group-hover:text-indigo-300 transition-colors"></i>
          <span class="relative">使用手册</span>
        </button>
        <button @click="showSettingsModal = true" class="h-9 px-3.5 text-[12px] font-medium text-slate-400 hover:text-white hover:bg-white/5 rounded-xl transition-all flex items-center gap-2 group relative overflow-hidden">
          <span class="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-indigo-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></span>
          <i class="fas fa-sliders-h relative text-slate-500 group-hover:text-indigo-300 transition-colors"></i>
          <span class="relative">设置</span>
        </button>
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
        <h2 class="text-xl font-bold text-white mb-3 tracking-wide">分析引擎启动中</h2>
        <p class="text-sm text-slate-400 mb-6 max-w-sm text-center leading-relaxed">正在初始化分析引擎，首次启动约需 5-10 秒...</p>
        <div class="flex items-center space-x-2 bg-white/5 px-4 py-2 rounded-full border border-white/10">
          <span class="w-1.5 h-1.5 rounded-full bg-neon-cyan animate-pulse"></span>
          <span class="text-xs font-mono text-slate-300">正在连接分析计算服务...</span>
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
          <h2 class="text-2xl font-black text-deep-blue tracking-tight mb-8">正在分析数据规律，为您生成决策洞见...</h2>
          
          <!-- Progress Bar -->
          <div class="w-full max-w-2xl bg-white p-6 rounded-2xl shadow-xl border border-slate-200">
             <div class="flex justify-between text-xs font-bold text-slate-500 mb-2">
                 <span>分析推进状态</span>
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
          @open-decision="currentStep = 'decision'"
          @live-data="(data) => { if (data) { livePerformanceData = data.performanceData; liveCovariates = data.covariates; } else { livePerformanceData = null; liveCovariates = null; } }"
        />
        <DecisionCenter
          v-else-if="currentStep === 'decision'"
          :modelResults="inferenceResults"
          :livePerformanceData="livePerformanceData"
          :liveCovariates="liveCovariates"
          :hierarchy-schema="currentHierarchy"
          :display-mapping="currentDisplayMapping"
          :raw-table-data="rawTableData"
          :target-variable="currentTarget"
          @back="currentStep = 'dashboard'"
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

    <!-- 底部状态栏 -->
    <footer class="bg-white border-t border-slate-200 py-2 px-6 flex justify-between items-center text-[11px] text-slate-400 z-40 select-none">
      <div class="flex items-center gap-4">
        <span class="flex items-center gap-2 font-semibold text-slate-500">
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-indigo-400 shadow-sm shadow-indigo-400/40"></span>
          DeepBayes
          <span class="text-slate-400 font-normal">v1.0.8</span>
        </span>
        <span class="w-px h-3.5 bg-slate-200"></span>
        <span class="text-slate-400 tracking-wide">&copy; 海外安全风险监测预警创新研究院</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full" :class="systemInfo ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-slate-300'"></span>
          {{ systemInfo ? '引擎已连接' : '连接中...' }}
        </span>
        <span v-if="systemInfo" class="flex items-center gap-1 text-slate-300">
          <i class="fas fa-microchip"></i>{{ systemInfo.backend }}
        </span>
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
import DecisionCenter from './components/DecisionCenter.vue';

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
const livePerformanceData = ref(null);
const liveCovariates = ref(null);
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
    { id: 1, time: '0.0s', text: '构建业务层级网络结构...', status: 'done' },
    { id: 2, time: '...', text: '解析变量间的影响关系...', status: 'loading' }
  ];

  const startTime = Date.now();
  const speedMultiplier = cleanSchema.samplingMode === 'fast' ? 3 : 1;
  progressInterval = setInterval(() => {
    if(loadingProgress.value < 88) loadingProgress.value += Math.random() * 4 * speedMultiplier;
    
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
    if(loadingProgress.value > 30 && loadingTips.value.length === 2) {
       loadingTips.value[1].status = 'done';
       loadingTips.value[1].time = elapsed;
       loadingTips.value.push({ id: 3, time: '...', text: '运行贝叶斯概率推断（最耗时环节）...', status: 'loading' });
    }
    if(loadingProgress.value > 65 && !loadingTips.value.find(t => t.id === 4)) {
       const lastLoader = loadingTips.value.find(t => t.status === 'loading');
       if(lastLoader) { lastLoader.status = 'done'; lastLoader.time = elapsed; }
       loadingTips.value.push({ id: 4, time: '...', text: '验证模型可信度并提取关键洞察...', status: 'loading' });
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
    loadingTips.value.push({ id: 5, time: '完成', text: '分析完成！正在为您呈现决策支撑视图...', status: 'done' });
    
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

/* ===== 头部动画特效 ===== */
@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(60px, -30px) scale(1.1); }
  66% { transform: translate(-30px, 20px) scale(0.95); }
}
@keyframes floatUp {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.6; }
  50% { transform: translateY(-20px) scale(1.5); opacity: 1; }
}
@keyframes glowShift {
  0%, 100% { transform: translateX(-30%); opacity: 0.3; }
  50% { transform: translateX(30%); opacity: 0.8; }
}
@keyframes pulseGlow {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}
@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
@keyframes pulse-dot {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.3); }
}

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