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
      <div class="flex items-center space-x-3">
        <button @click="showHelpGuide = true" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-indigo-200 hover:text-white transition-colors" title="帮助与使用手册">
          <i class="fas fa-question"></i>
        </button>
        <span v-if="currentSamplingMode === 'fast'" class="px-2.5 py-1 rounded bg-amber-500/20 border border-amber-500/50 text-xs font-semibold text-amber-400 flex items-center shadow-inner">
          <i class="fas fa-bolt mr-1.5"></i> 快速预览
        </span>
        <span class="px-2.5 py-1 rounded bg-indigo-900/60 border border-indigo-700/50 text-xs font-semibold text-neon-cyan flex items-center shadow-inner">
          <span class="w-2 h-2 rounded-full bg-neon-cyan animate-pulse mr-2 shadow-[0_0_5px_#00f0ff]"></span> v1.0.0 Stable
        </span>
      </div>
    </header>

    <!-- Main Content Area with Transition -->
    <main class="flex-1 overflow-auto relative">
      <transition name="fade-slide" mode="out-in">
        <DataImporter v-if="currentStep === 'import'" @health-check="openHealthCheck" />
        
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
          :hierarchySchema="currentHierarchy"
          :displayMapping="currentDisplayMapping"
          :rawTableData="rawTableData"
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

    <!-- 帮助与使用手册弹窗 -->
    <transition name="fade">
      <div v-if="showHelpGuide" class="fixed inset-0 bg-deep-blue/50 backdrop-blur-md flex justify-center items-center z-50" @click.self="showHelpGuide = false">
        <div class="w-full max-w-3xl max-h-[85vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden">
          <div class="px-6 py-4 bg-gradient-to-r from-indigo-600 to-indigo-500 text-white flex justify-between items-center shrink-0">
            <h2 class="text-lg font-bold flex items-center"><i class="fas fa-book-open mr-3"></i>DeepBayes 使用指南与帮助手册</h2>
            <button @click="showHelpGuide = false" class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"><i class="fas fa-times"></i></button>
          </div>
          <div class="flex-1 overflow-y-auto p-6 space-y-6 text-sm text-slate-700 leading-relaxed">
            
            <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-100">
              <h3 class="font-bold text-indigo-800 mb-2 flex items-center"><i class="fas fa-rocket mr-2 text-indigo-600"></i>快速入门</h3>
              <p>DeepBayes 是一款基于<strong>层次贝叶斯模型 (Hierarchical Bayesian Model)</strong> 的多层级效能评估与归因分析平台。您只需导入数据、拖拽构建拓扑、点击推演，即可获得专业的统计推断结果。</p>
            </div>
            
            <div>
              <h3 class="font-bold text-slate-800 mb-2 flex items-center"><i class="fas fa-database mr-2 text-blue-500"></i>数据准备要求</h3>
              <ul class="space-y-2 text-slate-600">
                <li class="flex items-start"><span class="text-emerald-500 mr-2 mt-0.5"><i class="fas fa-check-circle"></i></span><strong>格式</strong>: CSV 宽表，首行必须为列名（表头）</li>
                <li class="flex items-start"><span class="text-emerald-500 mr-2 mt-0.5"><i class="fas fa-check-circle"></i></span><strong>必含列</strong>: 至少 1 列“标识列” (ID，如地点名) + 1 列“数值目标列” (Y，如效率指数)</li>
                <li class="flex items-start"><span class="text-emerald-500 mr-2 mt-0.5"><i class="fas fa-check-circle"></i></span><strong>可选列</strong>: 协变量 (X，影响因素，如经费、密度等，必须为数值)</li>
                <li class="flex items-start"><span class="text-blue-500 mr-2 mt-0.5"><i class="fas fa-map-marker-alt"></i></span><strong>地图功能</strong>: 若想启用地理布控图，请包含“经度坐标”和“纬度坐标”两列</li>
              </ul>
            </div>

            <div>
              <h3 class="font-bold text-slate-800 mb-2 flex items-center"><i class="fas fa-project-diagram mr-2 text-indigo-500"></i>核心概念说明</h3>
              <div class="grid grid-cols-3 gap-3">
                <div class="bg-amber-50 p-3 rounded-lg border border-amber-200">
                  <div class="font-bold text-amber-800 text-xs mb-1"><i class="fas fa-bullseye mr-1"></i>观测靶点 (Y)</div>
                  <p class="text-[11px] text-amber-700">您想要评估的最终指标，例如“综合效率”、“稳定指数”。必须是连续数值。</p>
                </div>
                <div class="bg-blue-50 p-3 rounded-lg border border-blue-200">
                  <div class="font-bold text-blue-800 text-xs mb-1"><i class="fas fa-sitemap mr-1"></i>节点标识 (ID)</div>
                  <p class="text-[11px] text-blue-700">层级的分组变量，如“省份”、“分局名称”。可以是文本或数字。</p>
                </div>
                <div class="bg-emerald-50 p-3 rounded-lg border border-emerald-200">
                  <div class="font-bold text-emerald-800 text-xs mb-1"><i class="fas fa-chart-line mr-1"></i>协变量 (X)</div>
                  <p class="text-[11px] text-emerald-700">影响结果的因素，如“经费投入”、“兵力密度”。必须是数值。</p>
                </div>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-800 mb-2 flex items-center"><i class="fas fa-chart-bar mr-2 text-emerald-500"></i>图表解读指南</h3>
              <div class="space-y-2 text-slate-600">
                <p><strong>▶ DAG 拓扑图</strong>: 展示您构建的贝叶斯网络结构，可以观察节点之间的因果关系。</p>
                <p><strong>▶ 偏差散点图</strong>: 横轴=模型预期值，纵轴=偏差。亮点(超出预期)和暗点(低于预期)被标色区分。</p>
                <p><strong>▶ PPC 后验检验</strong>: 将真实数据分布和模型预测分布拟合，曲线越接近说明模型拟合度越高。</p>
                <p><strong>▶ 森林图与 What-If</strong>: 森林图展示每个协变量的影响力系数及95%可信区间。拖动滑块可实时观察参数变化对结果的影响。</p>
              </div>
            </div>

            <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <h3 class="font-bold text-slate-800 mb-2 flex items-center"><i class="fas fa-cog mr-2 text-slate-500"></i>采样引擎说明</h3>
              <p>本软件使用 PyMC 的 NUTS (No-U-Turn Sampler) 马尔可夫链蒙特卡洛采样器。<strong>快速模式</strong>保护了运算效率 (~5秒)，适合快速验证模型构建是否合理。<strong>精确模式</strong>大幅提高采样量 (~20秒)，能得到更可信的统计结果。您也可以通过“高级参数”自行设置 Draws 和 Tune 数值。</p>
            </div>
          </div>
        </div>
      </div>
    </transition>

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

const isProd = import.meta.env.PROD;
const API_BASE_URL = isProd ? 'http://127.0.0.1:18521' : 'http://127.0.0.1:8000';

const currentStep = ref('import');
const showHealthCheckModal = ref(false);

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

const fetchSystemInfo = async () => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/system_info`);
        if (res.ok) systemInfo.value = await res.json();
    } catch (e) { console.warn("Backend not ready for system info"); }
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
    fetchSystemInfo();
});

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
    if(loadingProgress.value > 65 && loadingTips.value.length === 3) {
       loadingTips.value[2].status = 'done';
       loadingTips.value[2].time = elapsed;
       loadingTips.value.push({ id: 4, time: '...', text: '核对 R_hat 收敛度并提取后验预测核密度 (PPC)...', status: 'loading' });
    }
  }, 400);

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
    loadingProgress.value = 100;
    loadingTips.value[loadingTips.value.length-1].status = 'done';
    loadingTips.value[loadingTips.value.length-1].time = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
    loadingTips.value.push({ id: 5, time: '完成', text: '参数矩阵装填完毕，即将开启全息控制台！', status: 'done' });
    
    setTimeout(() => {
        inferenceResults.value = data.results;
        currentStep.value = 'dashboard';
    }, 800);
    

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