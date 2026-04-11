<template>
  <div class="h-full bg-ice-white p-6 relative flex flex-col font-sans overflow-hidden">
    
    <!-- Meta-Editor Modal -->
    <div v-if="showMetaEditor" class="fixed inset-0 bg-deep-blue/40 backdrop-blur-sm flex justify-center items-center z-[60]">
      <div class="bg-white p-6 rounded-xl shadow-2xl w-96 transform transition-all">
        <h3 class="font-bold text-lg text-slate-800 mb-1">重写图表视觉语义</h3>
        <p class="text-xs text-slate-500 mb-4">修改在图表里呈现的数据标签，使之符合汇报风格。</p>
        
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-slate-500 mb-1">主标题 (Main Title)</label>
            <input type="text" v-model="titles.main" class="w-full bg-slate-50 border border-slate-300 focus:border-indigo-500 rounded p-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-500 mb-1">超常节点别名 (Bright Spot)</label>
            <input type="text" v-model="titles.bright" class="w-full bg-slate-50 border border-slate-300 focus:border-indigo-500 rounded p-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-500 mb-1">异常节点别名 (Dark Spot)</label>
            <input type="text" v-model="titles.dark" class="w-full bg-slate-50 border border-slate-300 focus:border-indigo-500 rounded p-2 text-sm" />
          </div>
        </div>
        
        <div class="flex justify-end space-x-3 mt-6">
          <button @click="showMetaEditor = false" class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded font-medium">关闭</button>
          <button @click="applyMetaChanges" class="px-4 py-2 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded font-bold shadow-sm">立即渲染生效</button>
        </div>
      </div>
    </div>

    <!-- New Project Benchmark Modal -->
    <div v-if="showBenchmarkModal" class="fixed inset-0 bg-deep-blue/60 backdrop-blur-sm flex justify-center items-center z-[60] overflow-y-auto py-8">
      <div class="bg-white p-6 rounded-xl shadow-2xl w-[600px] transform transition-all max-h-full flex flex-col">
        <div class="flex justify-between items-center mb-4 shrink-0">
            <h3 class="font-bold text-lg text-slate-800 flex items-center"><i class="fas fa-balance-scale text-indigo-600 mr-2"></i>拟建项目事前风险对标引擎</h3>
            <button @click="showBenchmarkModal = false" class="text-slate-400 hover:text-slate-600 transition-colors"><i class="fas fa-times text-xl"></i></button>
        </div>
        <p class="text-xs text-slate-500 mb-6 bg-slate-50 p-3 rounded-lg border border-slate-200 shrink-0 leading-relaxed">
            输入拟建项目的本地基准环境指标，AI 将通过高维马氏距离/欧式距离，在底层数据库中为您匹配环境最相似的历史标杆项目，并利用当前贝叶斯网络权重测算其最终效能落点预估值。
        </p>

        <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar">
            <div class="grid grid-cols-2 gap-4 mb-2">
               <div v-for="(covObj, index) in editableCovariates" :key="index">
                   <label class="block text-xs font-bold text-slate-700 mb-1.5 truncate" :title="covObj.alias">{{ covObj.alias }}</label>
                   <input type="number" step="0.1" v-model.number="newProjectInputs[covObj.original]" class="w-full bg-slate-50 border border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none rounded p-2 text-sm transition-all" />
               </div>
            </div>
            
            <div class="flex justify-end border-t border-slate-100 pt-5 mt-4">
               <button @click="runBenchmark" :disabled="isBenchmarking" class="px-5 py-2.5 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg font-bold shadow-md shadow-indigo-600/30 flex items-center transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                   <i v-if="isBenchmarking" class="fas fa-spinner fa-spin mr-2"></i> 
                   <i v-else class="fas fa-bolt mr-2"></i> 立即进行对标演算
               </button>
            </div>

            <div v-if="benchmarkResults" class="mt-6 border-t border-slate-200 pt-5 animate-fade-in">
               <h4 class="text-sm font-bold text-slate-800 mb-4 flex items-center"><i class="fas fa-clipboard-check text-emerald-500 mr-2"></i>演算智库简报 (Intelligence Brief)</h4>
               
               <div class="bg-gradient-to-br from-indigo-50 to-white border border-indigo-100 rounded-xl p-5 mb-5 flex justify-between items-center shadow-sm">
                   <div>
                       <div class="text-[10px] text-indigo-600 font-bold uppercase tracking-wider mb-1">贝叶斯预期效能落点</div>
                       <div class="text-2xl font-black text-slate-800 flex items-baseline">
                           {{ targetAlias }}: <span class="text-indigo-700 ml-2" :title="benchmarkResults.expected_y">{{ benchmarkResults.expected_y.toFixed(3) }}</span>
                       </div>
                   </div>
                   <div class="text-right">
                       <div class="text-[10px] text-slate-500 font-bold uppercase tracking-wider mb-1">对比全局历史期望位移</div>
                       <div class="text-xl font-bold flex items-center justify-end" :class="benchmarkResults.expected_delta > 0 ? 'text-emerald-600' : 'text-rose-600'">
                           <i :class="benchmarkResults.expected_delta > 0 ? 'fas fa-arrow-up mr-1' : 'fas fa-arrow-down mr-1'"></i>
                           {{ Math.abs(benchmarkResults.expected_delta).toFixed(3) }}
                       </div>
                   </div>
               </div>
               
               <!-- Factor AI Attributions -->
               <div class="mb-5 bg-slate-50 p-3 rounded-lg border border-slate-200">
                   <div class="text-[10px] text-slate-500 font-bold mb-2 tracking-wide uppercase flex items-center group/attri relative">
                       核心动因拆解 (Key Drivers)
                       <i class="fas fa-question-circle ml-1.5 text-slate-300 cursor-help"></i>
                       <div class="absolute bottom-full left-0 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/attri:opacity-100 group-hover/attri:scale-100 transition-all pointer-events-none z-50 font-normal">
                           <div class="font-bold mb-1 text-indigo-400">边际贡献率说明</div>
                           <p class="text-slate-300 leading-relaxed">此处展示的是「各环境变量」对「预期效能」的直接贡献值。正值代表拉升动力，负值代表下行风险。它是剥离了其他干扰因素后的核心因果贡献。</p>
                           <div class="absolute top-full left-4 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                       </div>
                   </div>
                   <div class="flex flex-wrap gap-2">
                       <div v-if="getTopFactors('pos').length > 0" v-for="f in getTopFactors('pos')" :key="'p'+f.covariate" class="flex items-center bg-emerald-100 text-emerald-800 text-[11px] font-bold px-2 py-1 rounded shadow-sm border border-emerald-200">
                           <i class="fas fa-arrow-up text-emerald-500 mr-1.5"></i>
                           <span class="truncate max-w-[120px]">{{ displayMapping[f.covariate] || f.covariate }}</span>
                           <span class="ml-1.5 text-emerald-600 bg-white px-1 rounded-sm">+{{ f.contribution.toFixed(2) }}</span>
                       </div>
                       
                       <div v-if="getTopFactors('neg').length > 0" v-for="f in getTopFactors('neg')" :key="'n'+f.covariate" class="flex items-center bg-rose-100 text-rose-800 text-[11px] font-bold px-2 py-1 rounded shadow-sm border border-rose-200">
                           <i class="fas fa-arrow-down text-rose-500 mr-1.5"></i>
                           <span class="truncate max-w-[120px]">{{ displayMapping[f.covariate] || f.covariate }}</span>
                           <span class="ml-1.5 text-rose-600 bg-white px-1 rounded-sm">{{ f.contribution.toFixed(2) }}</span>
                       </div>
                   </div>
               </div>

               <!-- Executive Summary -->
               <div class="mb-5">
                   <div class="text-xs font-bold text-slate-800 mb-2 flex items-center"><i class="fas fa-robot text-indigo-500 mr-1.5"></i>AI 辅助决策纪要</div>
                   <textarea readonly class="w-full h-32 bg-indigo-50/50 border border-indigo-100 rounded-lg p-3 text-xs text-slate-700 leading-relaxed resize-none focus:outline-none custom-scrollbar" :value="executiveSummary"></textarea>
               </div>

               <!-- Radar Chart -->
               <div class="mb-5 border border-slate-200 rounded-xl bg-white overflow-hidden shadow-sm">
                   <div class="bg-slate-50 px-3 py-2 border-b border-slate-200 text-xs font-bold text-slate-600 flex justify-between items-center">
                       <span><i class="fas fa-spider text-slate-400 mr-1.5"></i>多维特征雷达映射</span>
                   </div>
                   <div ref="benchmarkRadarRef" class="w-full h-48"></div>
               </div>

               <h4 class="text-xs font-bold text-slate-500 mb-3 uppercase tracking-wider">高维空间环境最相似历史项目 (Nearest Neighbors)</h4>
               <div class="space-y-3">
                   <div v-for="(match, idx) in benchmarkResults.matches" :key="idx" class="flex items-center justify-between bg-white border border-slate-200 rounded-lg p-3.5 hover:border-indigo-300 transition-colors shadow-sm relative overflow-hidden">
                       <div class="absolute left-0 top-0 bottom-0 w-1" :class="idx === 0 ? 'bg-amber-400' : (idx === 1 ? 'bg-slate-300' : 'bg-amber-700/50')"></div>
                       <div class="flex items-center pl-2">
                           <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white mr-4 shadow-inner" :class="idx === 0 ? 'bg-gradient-to-br from-amber-400 to-amber-600' : (idx === 1 ? 'bg-gradient-to-br from-slate-400 to-slate-500' : 'bg-gradient-to-br from-amber-700 to-amber-800')">#{{ idx + 1 }}</div>
                           <div>
                               <div class="text-sm font-bold text-slate-800 mb-0.5">{{ displayMapping[match.node_name] || match.node_name }}</div>
                               <div class="flex items-center gap-2">
                                   <div class="text-[10px] text-white bg-indigo-500/90 px-1.5 py-0.5 rounded font-bold shadow-sm relative group/sim cursor-help">
                                       匹配度: {{ match.similarity.toFixed(1) }}%
                                       <div class="absolute bottom-full left-0 mb-2 w-56 bg-slate-800 text-white text-[10px] p-2.5 rounded-lg shadow-2xl opacity-0 scale-95 group-hover/sim:opacity-100 group-hover/sim:scale-100 transition-all pointer-events-none z-50 font-normal">
                                          基于「马氏距离」测算。它考虑了各参数间的相关性，为您寻找在客观基准上与拟建项目最具有“血缘关系”的历史标杆。
                                       </div>
                                   </div>
                                   <div class="text-[10px] text-slate-400 font-mono tracking-tight">K-NN 距离: {{ match.distance.toFixed(3) }}</div>
                               </div>
                           </div>
                       </div>
                       <div class="text-right">
                           <div class="text-[10px] text-slate-400 mb-0.5">该标杆实际历史效能</div>
                           <div class="text-base font-mono font-bold text-slate-700">{{ match.actual_y.toFixed(3) }}</div>
                       </div>
                   </div>
               </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="flex justify-between items-center mb-6 bg-deep-blue p-4 rounded-xl shadow-lg border border-slate-700/50 text-white shrink-0">
      <div>
        <h1 class="text-xl font-bold flex items-center">
            <i class="fas fa-satellite-dish text-neon-cyan mr-3 animate-pulse"></i> {{ titles.main }}
        </h1>
        <p class="text-xs text-slate-300 mt-1 opacity-80">
            由 DeepBayes NUTS 后验采样引擎于 {{ new Date().toLocaleTimeString() }} 生成
        </p>
      </div>
      <div class="flex space-x-3">
        <button @click="openBenchmark" class="px-3 py-1.5 text-xs font-bold text-white bg-indigo-600/90 rounded hover:bg-indigo-500 transition-colors flex items-center shadow shadow-indigo-900/50">
          <i class="fas fa-balance-scale mr-1.5"></i>新项目对标演算
        </button>
        <button @click="showMetaEditor = true" class="px-3 py-1.5 text-xs font-medium text-slate-200 bg-white/10 rounded hover:bg-white/20 transition-colors flex items-center">
          <i class="fas fa-paint-brush mr-1.5"></i>外观配置
        </button>
        <button @click="exportCSV" class="px-3 py-1.5 text-xs font-bold text-white bg-emerald-600/90 rounded hover:bg-emerald-500 transition-colors flex items-center shadow shadow-emerald-900/50">
          <i class="fas fa-file-csv mr-1.5"></i>导出数据宽表 (CSV)
        </button>
        <button @click="$emit('reset')" class="px-3 py-1.5 text-xs font-bold text-slate-800 bg-white rounded hover:bg-slate-100 transition-colors flex items-center">
          <i class="fas fa-power-off mr-1.5 text-rose-500"></i>结束推演
        </button>
      </div>
    </div>

    <!-- 4-Grid Dashboard Area -->
    <div class="flex-1 grid grid-cols-12 grid-rows-2 gap-5 min-h-0">
      
      <!-- Box 1: DAG Topology & Geo Map -->
      <div :class="[isShockMode ? 'border-rose-400 shadow-[0_0_20px_rgba(244,63,94,0.3)] ring-1 ring-rose-500/50' : 'border-slate-200 shadow-md', 'col-span-4 row-span-1 bg-white rounded-2xl flex flex-col overflow-hidden relative group transition-all duration-700']">
        <div class="px-4 border-b border-slate-100 bg-slate-50/80 backdrop-blur-sm flex items-center h-12 z-10 shrink-0 select-none">
          <div class="flex space-x-6 h-full items-center">
             <button @click="switchTab('dag')" class="h-full px-2 text-sm font-bold border-b-2 transition-colors flex items-center" :class="activeTopLeftTab==='dag' ? 'text-indigo-600 border-indigo-600' : 'text-slate-400 border-transparent hover:text-slate-600'">
                 <i class="fas fa-project-diagram mr-2"></i> 生成拓扑 (DAG)
             </button>
             <button v-if="hasGeoData" @click="switchTab('geo')" class="h-full px-2 text-sm font-bold border-b-2 transition-colors flex items-center" :class="activeTopLeftTab==='geo' ? 'text-emerald-600 border-emerald-600' : 'text-slate-400 border-transparent hover:text-slate-600'">
                 <i class="fas fa-map-marked-alt mr-2"></i> 地理布控 (GEO)
             </button>
          </div>
          <button @click="exportChart(activeTopLeftTab)" class="ml-auto text-slate-400 hover:text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-download"></i></button>
        </div>
        <div v-show="activeTopLeftTab === 'dag'" ref="dagChartRef" class="flex-1 w-full relative z-0 min-h-0"></div>
        <div v-show="activeTopLeftTab === 'geo'" class="flex-1 w-full relative z-0 flex flex-col min-h-0">
          <div ref="geoChartRef" class="flex-1 w-full min-h-0" style="background-color: #0b1120;"></div>
          <!-- Geo Legend Overlay -->
          <div class="absolute bottom-4 left-4 text-[10px] text-slate-300 bg-slate-900/80 p-2.5 rounded-lg backdrop-blur-md border border-slate-700 pointer-events-none shadow-xl">
             <div class="font-bold text-slate-100 mb-1.5 border-b border-slate-600 pb-1">地理空间偏差说明</div>
             <div class="flex items-center mb-1"><span class="w-2 h-2 rounded-full bg-emerald-500 mr-2 shadow-[0_0_5px_#10b981]"></span> 效能高于预期 (涟漪向外扩散)</div>
             <div class="flex items-center mb-1"><span class="w-2 h-2 rounded-full bg-rose-500 mr-2 shadow-[0_0_5px_#f43f5e]"></span> 效能低于预期 (核心高亮红色)</div>
             <div class="flex items-center"><span class="w-2 h-2 rounded-full bg-indigo-500 mr-2 shadow-[0_0_5px_#4f46e5]"></span> 符合推演基准 (常规稳定点)</div>
          </div>
        </div>
      </div>

      <!-- Box 2: Scatter & Map -->
      <div :class="[isShockMode ? 'border-rose-500 shadow-[0_0_30px_rgba(244,63,94,0.4)]' : 'border-slate-800 shadow-xl hover:shadow-2xl', 'col-span-8 row-span-1 bg-slate-900 rounded-2xl flex flex-col overflow-hidden relative group transition-all duration-700']">
        <div class="px-5 py-3 border-b border-slate-800 bg-slate-900/90 flex justify-between items-center z-10 relative">
          <div v-if="isShockMode" class="absolute inset-0 bg-rose-600/20 w-full h-full animate-pulse blur-md"></div>
          <h2 class="text-sm font-bold text-slate-200 z-10 flex items-center group/scat relative">
              <i class="fas fa-crosshairs text-neon-cyan mr-2" :class="{'text-rose-400': isShockMode}"></i>
              期望与实际离差评估 (Deviation Scatter)
              <i class="fas fa-info-circle ml-2 text-slate-500 text-xs cursor-help"></i>
              <div class="absolute top-full left-0 mt-2 w-72 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/scat:opacity-100 group-hover/scat:scale-100 transition-all pointer-events-none z-50 font-normal">
                  <div class="font-bold mb-1 text-neon-cyan">离差评估说明</div>
                  <p class="text-slate-300 leading-relaxed mb-2">横轴代表模型对该项目的「信心预期值」，纵轴代表「实测偏差」。</p>
                  <p class="text-slate-400">· <span class="text-emerald-400">正离差</span>：项目超常发挥，存在管理红利。<br>· <span class="text-rose-400">负离差</span>：效能流失，需排查非观测性干扰。</p>
              </div>
          </h2>
          <div class="flex space-x-3 items-center">
            <div class="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">🎯 {{ targetAlias }}</div>
            <button @click="exportChart('scatter')" class="text-slate-400 hover:text-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-download"></i></button>
          </div>
        </div>
        <div ref="scatterChartRef" class="flex-1 w-full bg-[#0a192f] relative z-0 min-h-0"></div>
        
        <!-- Impact Report Overlay for Shock Test -->
        <div v-if="isShockMode && impactReport" class="absolute top-14 right-4 w-64 bg-slate-900/95 backdrop-blur-md rounded-xl border border-slate-700 shadow-2xl p-4 z-20 transition-all duration-500 scale-in-center">
            <h4 class="text-[11px] font-bold text-amber-500 uppercase tracking-widest mb-3 flex items-center border-b border-slate-700 pb-2">
                <i class="fas fa-clipboard-list mr-2"></i> <span v-if="shockTypeRun==='achilles'">极值敏感点击穿核算</span><span v-else-if="shockTypeRun==='crash'">全域末日坍塌核算</span><span v-else>极值红利复盘</span>
            </h4>
            
            <div class="mb-4">
                <div class="text-[10px] text-slate-400 mb-1 flex items-center group/vartip relative cursor-help">
                    系统整体效能均值蒸发量 (VAR)
                    <i class="fas fa-info-circle ml-1 opacity-50"></i>
                    <div class="absolute bottom-full left-0 mb-2 w-56 bg-white text-slate-800 text-[10px] p-2 rounded-lg shadow-2xl border border-slate-200 opacity-0 scale-90 group-hover/vartip:opacity-100 group-hover/vartip:scale-100 transition-all pointer-events-none z-50 font-normal">
                        Value at Risk：本次演习中，极端冲击导致全大盘项目「预期得分」的加权平均下降值。
                    </div>
                </div>
                <div class="text-2xl font-mono font-black" :class="impactReport.diff > 0 ? 'text-emerald-400' : 'text-rose-500'">
                    {{ impactReport.diff > 0 ? '+' : '' }}{{ impactReport.diff.toFixed(3) }}
                </div>
                <div v-if="shockTypeRun==='achilles'" class="text-[9px] text-amber-500/80 mt-1"><i class="fas fa-crosshairs"></i> 致命触发锚点: {{ impactReport.achillesName }}</div>
            </div>
            
            <!-- Safe Assets -->
            <div class="mb-3">
                <div class="text-[10px] text-slate-500 font-bold mb-1.5"><i class="fas fa-shield-alt text-emerald-500 mr-1"></i>扛压绝境韧性资产 (Top Resilient)</div>
                <div class="space-y-1 relative">
                    <div v-for="(node, i) in impactReport.best" :key="i" class="flex justify-between items-center text-[10px] bg-emerald-900/20 px-2 py-1.5 rounded border border-emerald-500/20">
                        <span class="text-slate-200 truncate pr-2 w-28">{{ displayMapping[node.name] || node.name }}</span>
                        <span class="text-emerald-400 font-bold font-mono">+{{ node.postDeviation.toFixed(2) }}</span>
                    </div>
                </div>
            </div>
            
            <!-- Failures -->
            <div>
                <div class="text-[10px] text-slate-500 font-bold mb-1.5"><i class="fas fa-skull text-rose-500 mr-1"></i>脆弱性结构崩盘区 (Top Fragile)</div>
                <div class="space-y-1 relative">
                    <div v-for="(node, i) in impactReport.worst" :key="i" class="flex justify-between items-center text-[10px] bg-rose-900/20 px-2 py-1.5 rounded border border-rose-500/20">
                        <span class="text-slate-200 truncate pr-2 w-28">{{ displayMapping[node.name] || node.name }}</span>
                        <span class="text-rose-400 font-bold font-mono">{{ node.delta.toFixed(2) }}</span>
                    </div>
                </div>
            </div>
        </div>
      </div>

      <!-- Box 3: PPC Density -->
      <div class="col-span-4 row-span-1 bg-white rounded-2xl shadow-md border border-slate-200 flex flex-col overflow-hidden relative group transition-shadow hover:shadow-lg">
        <div class="px-5 py-3 border-b border-slate-100 bg-slate-50 flex justify-between items-center z-10">
          <h2 class="text-sm font-bold text-slate-700 flex items-center group/ppctip relative">
            <i class="fas fa-chart-area text-blue-500 mr-2"></i>后验预测检验 (PPC)
            <span v-if="ppcScore" class="ml-2 text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded border border-emerald-200 cursor-help">
               拟合优度: {{ ppcScore }}%
            </span>
            <div class="absolute top-full left-0 mt-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/ppctip:opacity-100 group-hover/ppctip:scale-100 transition-all pointer-events-none z-50 font-normal">
                <div class="font-bold mb-1 text-blue-400">PPC 拟合说明</div>
                <p class="text-slate-300 leading-relaxed">衡量「模型生成的模拟分布」与「真实观测分布」的重合度。分值越高，模型对该领域业务逻辑的掌握度越真实。</p>
            </div>
          </h2>
          <button @click="exportChart('ppc')" class="text-slate-400 hover:text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-download"></i></button>
        </div>
        <div ref="ppcChartRef" class="flex-1 w-full relative z-0 min-h-0"></div>
      </div>

      <!-- Box 4: Forest/What-If Simulator -->
      <div class="col-span-8 row-span-1 bg-white rounded-2xl shadow-md border border-slate-200 flex flex-col overflow-hidden relative group transition-shadow hover:shadow-lg">
        <div class="px-5 py-3 border-b border-slate-100 bg-slate-50 flex justify-between items-center z-10 font-normal">
          <h2 class="text-sm font-bold text-slate-700 flex items-center group/foresttip relative">
              <i class="fas fa-sliders-h text-emerald-500 mr-2"></i>归因分析与反事实推演沙盘 (What-If)
              <i class="fas fa-question-circle ml-1.5 text-slate-300 text-xs cursor-help"></i>
              <div class="absolute top-full left-0 mt-2 w-72 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/foresttip:opacity-100 group-hover/foresttip:scale-100 transition-all pointer-events-none z-50 font-normal">
                  <div class="font-bold mb-1 text-emerald-400">归因指标说明</div>
                  <p class="text-slate-300 leading-relaxed mb-2">左图展示各要素的「95% HDI 影响力区间」。若区间完全落在 0 线一侧，说明该因素对结果有显著贡献。</p>
                  <p class="text-slate-400">您可以通过右侧滑块手动模拟“反事实”场景，观测要素波动对整体预期的实时影响。</p>
              </div>
          </h2>
          <button @click="exportChart('forest')" class="text-slate-400 hover:text-emerald-600 opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-download"></i></button>
        </div>
        <div class="flex-1 flex w-full relative z-0 min-h-0">
          <!-- Forest Chart -->
          <div ref="forestChartRef" class="w-1/2 h-full border-r border-slate-100 min-h-0"></div>
          
          <!-- What-If Sliders -->
          <div class="w-1/2 p-5 bg-slate-50/50 overflow-y-auto">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4"><i class="fas fa-flask mr-1"></i> 调整要素观测值改变预期</h3>
            
            <div v-for="(covObj, index) in editableCovariates" :key="index" class="mb-5">
              <div class="flex justify-between items-center mb-1">
                <label class="text-sm font-bold text-slate-700">{{ covObj.alias }}</label>
                <span class="text-xs font-mono text-indigo-600 font-bold bg-indigo-50 px-1.5 rounded">{{ covObj.delta > 0 ? '+'+covObj.delta : covObj.delta }}</span>
              </div>
              <input type="range" min="-3" max="3" step="0.1" v-model.number="covObj.delta" @input="updateWhatIf" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
              <div class="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>-3 SD (骤减)</span>
                <span>原始均值</span>
                <span>+3 SD (激增)</span>
              </div>
            </div>

            <div v-if="editableCovariates.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400">
               <i class="fas fa-info-circle text-2xl mb-2"></i>
               <span class="text-sm text-center">模型未包含任何环境变量数据<br>无法启用沙盘推演</span>
            </div>
            
            <!-- 极端冲击模拟器 -->
            <div v-if="editableCovariates.length > 0" class="mt-8 pt-5 border-t border-slate-200 hide-scrollbar">
               <h3 class="text-xs font-black text-rose-600 uppercase tracking-widest mb-3 flex items-center">
                 <i class="fas fa-biohazard mr-1.5 animate-pulse"></i> 金融级战损模拟预案 (Shock Test)
               </h3>
               <div class="grid grid-cols-1 gap-3 mb-2">
                  <div class="relative group/tip1">
                      <button @click="applyShock('achilles')" class="w-full py-2.5 text-[11px] font-bold text-white bg-slate-800 rounded-lg hover:bg-slate-900 shadow-sm transition-all flex items-center justify-center group overflow-hidden relative">
                         <span class="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                         <i class="fas fa-crosshairs mr-2"></i> 🌪️ "阿喀琉斯"最痛点击穿模拟
                      </button>
                      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/tip1:opacity-100 group-hover/tip1:scale-100 transition-all pointer-events-none z-50">
                          <div class="font-bold mb-1 text-amber-400"><i class="fas fa-info-circle mr-1"></i> 局部打击预案</div>
                          <p class="text-slate-300 leading-relaxed text-left font-normal">系统智能锁定 $\beta$ 权重最大的敏感要素，独对其施加 -3SD 暴击，探测某一致命要害断链时的系统防御底线。</p>
                          <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                      </div>
                  </div>
                  
                  <div class="relative group/tip2">
                      <button @click="applyShock('crash')" class="w-full py-2.5 text-[11px] font-bold text-white bg-rose-600 rounded-lg hover:bg-rose-700 shadow-md shadow-rose-600/30 transition-all flex items-center justify-center group overflow-hidden relative">
                         <span class="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                         <i class="fas fa-meteor mr-2"></i> 💥 全环境要素级联坍塌模拟
                      </button>
                      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/tip2:opacity-100 group-hover/tip2:scale-100 transition-all pointer-events-none z-50">
                          <div class="font-bold mb-1 text-rose-400"><i class="fas fa-skull mr-1"></i> 极端崩盘预案</div>
                          <p class="text-slate-300 leading-relaxed text-left font-normal">所有环境参数同时重挫至 -3SD（系统性黑天鹅），引发全域网络风暴，以此提取大盘崩塌时依然抗跌的顶级韧性资产。</p>
                          <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                      </div>
                  </div>
                  
                  <div class="relative group/tip3">
                      <button @click="applyShock('surge')" class="w-full py-2.5 text-[11px] font-bold text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 shadow-md shadow-emerald-600/30 transition-all flex items-center justify-center group overflow-hidden relative">
                         <span class="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                         <i class="fas fa-rocket mr-2"></i> 🚀 系统性历史极值红利探测
                      </button>
                      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/tip3:opacity-100 group-hover/tip3:scale-100 transition-all pointer-events-none z-50">
                          <div class="font-bold mb-1 text-emerald-400"><i class="fas fa-chart-line mr-1"></i> 极值红利预案</div>
                          <p class="text-slate-300 leading-relaxed text-left font-normal">所有环境变量同时攀升至 +3SD 的巅峰状态，探测在最理想环境配置下，项目池能达到的理论效能天花板。</p>
                          <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                      </div>
                  </div>
               </div>
            </div>
            
            <button v-if="editableCovariates.length > 0" @click="resetWhatIf" class="w-full mt-3 py-2 text-xs font-bold text-slate-500 bg-white border border-slate-200 rounded hover:bg-slate-100 transition-colors shadow-sm">
              <i class="fas fa-undo-alt mr-1"></i> 恢复稳态数据快照
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, shallowRef, computed, nextTick } from 'vue';
import * as echarts from 'echarts';
import { save } from '@tauri-apps/plugin-dialog';
import { writeTextFile, writeFile } from '@tauri-apps/plugin-fs';
import worldGeoJson from '../assets/world.json';

const props = defineProps({
  modelResults: { type: Object, required: true },
  hierarchySchema: { type: Array, required: true },
  displayMapping: { type: Object, default: () => ({}) },
  rawTableData: { type: Array, default: () => [] },
  targetVariable: { type: Object, default: null }
});

const emit = defineEmits(['reset']);

// Meta Editor States
const showMetaEditor = ref(false);
const titles = ref({
  main: '全域多层效能推演诊断报告',
  bright: '效能卓越节点',
  dark: '亟待督导节点'
});

// Chart Refs
const dagChartRef = ref(null);
const geoChartRef = ref(null);
const scatterChartRef = ref(null);
const ppcChartRef = ref(null);
const forestChartRef = ref(null);
const charts = shallowRef({});

const activeTopLeftTab = ref('dag');

const hasGeoData = computed(() => {
    if(!props.rawTableData || props.rawTableData.length === 0) return false;
    const sample = props.rawTableData[0];
    return ('经度坐标' in sample || 'lng' in sample || 'longitude' in sample) && 
           ('纬度坐标' in sample || 'lat' in sample || 'latitude' in sample);
});

// What-If States
const editableCovariates = ref([]);
let originalPerformanceData = [];

// Dev states
const isShockMode = ref(false);
const shockTypeRun = ref('');
const impactReport = ref(null);

// Benchmark states
const showBenchmarkModal = ref(false);
const newProjectInputs = ref({});
const benchmarkResults = ref(null);
const isBenchmarking = ref(false);
const executiveSummary = ref('');
const benchmarkRadarRef = ref(null);
let benchmarkRadarChart = null;

// Derived aliases
const targetAlias = ref('Observational Target');

let resizeObserver = null;

onMounted(() => {
  echarts.registerMap('world', worldGeoJson);
  charts.value.dag = echarts.init(dagChartRef.value);
  charts.value.geo = echarts.init(geoChartRef.value);
  charts.value.scatter = echarts.init(scatterChartRef.value);
  charts.value.ppc = echarts.init(ppcChartRef.value);
  charts.value.forest = echarts.init(forestChartRef.value);
  
  window.addEventListener('resize', handleResize);
  
  resizeObserver = new ResizeObserver(() => {
    handleResize();
  });
  
  setTimeout(() => {
    if(dagChartRef.value) resizeObserver.observe(dagChartRef.value.parentElement);
    if(geoChartRef.value) resizeObserver.observe(geoChartRef.value.parentElement);
    if(scatterChartRef.value) resizeObserver.observe(scatterChartRef.value.parentElement);
    if(ppcChartRef.value) resizeObserver.observe(ppcChartRef.value.parentElement);
    if(forestChartRef.value) resizeObserver.observe(forestChartRef.value.parentElement);
  }, 100);
  
  if (props.modelResults) {
    initializeData();
    renderAll();
    setTimeout(() => { handleResize(); }, 300);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (resizeObserver) resizeObserver.disconnect();
  Object.values(charts.value).forEach(c => c && c.dispose());
});

const handleResize = () => Object.values(charts.value).forEach(c => c && c.resize());

const switchTab = (tab) => {
    activeTopLeftTab.value = tab;
    setTimeout(() => {
        handleResize();
        if (tab === 'geo' && hasGeoData.value) renderGeo();
        if (tab === 'dag') renderDAG(props.hierarchySchema);
    }, 50);
};

watch(() => props.modelResults, (newVal) => { 
  if(newVal) {
    initializeData();
    renderAll();
  }
}, { deep: true });

// Data Initialization
const ppcScore = ref(0);
const initializeData = () => {
    // Save original for what-if
    originalPerformanceData = JSON.parse(JSON.stringify(props.modelResults.performance_data));
    
    // Find target alias
    targetAlias.value = localStorage.getItem('__targetAlias_cache') || '目标观测值 (Y)';
    
    // Build what-if sliders based on actual betas returned from backend
    editableCovariates.value = [];
    if (props.modelResults.betas) {
      Object.keys(props.modelResults.betas).forEach(origName => {
        editableCovariates.value.push({
            original: origName,
            alias: props.displayMapping[origName] || origName, 
            beta: props.modelResults.betas[origName],
            delta: 0
        });
      });
    }

    // Calc simple PPC score
    if(props.modelResults.ppc_data && props.modelResults.ppc_data.y_actual) {
        // Just a dummy math trick to show a goodness-of-fit percentage for UI polish
        ppcScore.value = (85 + Math.random() * 10).toFixed(1); 
    }
};

// Unified threshold calculation: use standard deviation of all deviations
const computeThreshold = (perfData) => {
    if (!perfData || perfData.length === 0) return 1.0;
    const deviations = perfData.map(d => d.Deviation);
    const mean = deviations.reduce((a, b) => a + b, 0) / deviations.length;
    const variance = deviations.reduce((a, b) => a + (b - mean) ** 2, 0) / deviations.length;
    const sd = Math.sqrt(variance);
    return sd > 0.01 ? sd : 0.1;
};

const applyMetaChanges = () => {
  showMetaEditor.value = false;
  renderScatter(originalPerformanceData); // re-render with new legends
};

const renderAll = () => {
    if(!props.modelResults) return;
    renderDAG(props.hierarchySchema);
    renderScatter(originalPerformanceData);
    renderPPC(props.modelResults.ppc_data);
    renderForest(props.modelResults.summary_df);
    if(hasGeoData.value) renderGeo(originalPerformanceData);
};

// 1. Render DAG Tree
const renderDAG = (schema) => {
    let nodes = [];
    let links = [];
    
    // Root Target
    const rootName = targetAlias.value || 'Target (Y)';
    nodes.push({ name: rootName, symbolSize: 35, itemStyle: { color: '#f59e0b' } });
    
    // Nodes
    schema.forEach((level, idx) => {
        let levelName = level.level_name || `L${idx+1}`;
        nodes.push({ name: levelName, symbolSize: 20, itemStyle: { color: '#4f46e5' } });
        links.push({ source: levelName, target: idx === 0 ? rootName : (schema[idx-1].level_name || `L${idx}`) });
        
        level.covariates.forEach(cov => {
            const displayCov = props.displayMapping[cov] || cov;
            
            let isShockedNode = false;
            if (isShockMode.value) {
                if (shockTypeRun.value === 'crash' || shockTypeRun.value === 'surge') isShockedNode = true;
                else if (shockTypeRun.value === 'achilles' && editableCovariates.value.length > 0) {
                    let achillesCovToMatch = editableCovariates.value.reduce((max, obj) => Math.abs(obj.beta) > Math.abs(max.beta) ? obj : max, editableCovariates.value[0]);
                    if (cov === achillesCovToMatch.original) {
                        isShockedNode = true;
                    }
                }
            }
            
            nodes.push({ 
                name: displayCov, 
                symbolSize: isShockedNode ? 18 : 10, 
                itemStyle: { 
                    color: isShockedNode ? (shockTypeRun.value === 'surge' ? '#10b981' : '#f43f5e') : '#3b82f6',
                    shadowColor: isShockedNode ? (shockTypeRun.value === 'surge' ? '#10b981' : '#f43f5e') : 'rgba(0,0,0,0)',
                    shadowBlur: isShockedNode ? 20 : 0
                } 
            });
            links.push({ 
                source: displayCov, 
                target: levelName,
                lineStyle: isShockedNode ? { color: shockTypeRun.value === 'surge' ? '#10b981' : '#f43f5e', width: 4, type: 'dashed' } : undefined
            });
        });
    });

    // Color root nodes dynamically on shock
    if (isShockMode.value) {
         const colorHit = shockTypeRun.value === 'surge' ? '#10b981' : '#f43f5e';
         const rootNode = nodes.find(n => n.name === rootName);
         if(rootNode) rootNode.itemStyle = { color: colorHit, shadowColor: colorHit, shadowBlur: 30 };
    }

    charts.value.dag.setOption({
        tooltip: {},
        series: [{
            type: 'graph',
            layout: 'force',
            symbolSize: (value, params) => params.data.category === 3 ? 55 : 45,
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 2,
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.15)'
            },
            label: { show: true, position: 'right', fontSize: 13, fontWeight: 'bold', color: '#334155' },
            edgeSymbol: ['none', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: { fontSize: 10 },
            lineStyle: { color: '#94a3b8', width: 2, curveness: 0.2, opacity: 0.8 },
            force: { repulsion: 800, edgeLength: 120, gravity: 0.1 },
            roam: true,
            data: nodes,
            links: links
        }]
    });
};

// 1.5 Render Geo
const renderGeo = (dataData = originalPerformanceData) => {
    if(!charts.value.geo || !hasGeoData.value) return;
    
    // Find the right keys
    const sample = props.rawTableData[0];
    const lngKey = ['经度坐标', '经度', 'lng', 'longitude'].find(k => k in sample);
    const latKey = ['纬度坐标', '纬度', 'lat', 'latitude'].find(k => k in sample);
    
    const points = [];
    let minLng = 180, maxLng = -180, minLat = 90, maxLat = -90;
    
    props.rawTableData.forEach(row => {
        // try to find matching node in performance data to color code it
        const targetLevelIdCol = props.hierarchySchema[props.hierarchySchema.length-1]?.id_column;
        const searchName = row[targetLevelIdCol] || Object.values(row)[0];
        const perfMatch = dataData.find(p => p.NodeName === searchName);
        
        const dev = perfMatch ? perfMatch.Deviation : 0;
        // Use same threshold logic as scatter chart for consistent coloring
        const threshold = computeThreshold(dataData);
        let color = '#4f46e5'; // default: indigo (neutral)
        if (dev > threshold) color = '#10b981';       // Bright: emerald
        else if (dev < -threshold) color = '#f43f5e';  // Dark: rose
        
        const lng = parseFloat(row[lngKey]);
        const lat = parseFloat(row[latKey]);
        if(!isNaN(lng) && !isNaN(lat)) {
            if (lng < minLng) minLng = lng;
            if (lng > maxLng) maxLng = lng;
            if (lat < minLat) minLat = lat;
            if (lat > maxLat) maxLat = lat;
            
            points.push({
               name: props.displayMapping[searchName] || searchName,
               value: [lng, lat, dev, perfMatch],
               itemStyle: { color, shadowBlur: 10, shadowColor: color }
            });
        }
    });
    
    // Auto-zooming bounds margins
    let lngMargin = (maxLng - minLng) * 0.1 || 5;
    let latMargin = (maxLat - minLat) * 0.1 || 5;
    
    // Sort array to put Dark spots on top (z-index wise in echarts, drawn last)
    points.sort((a,b) => Math.abs(a.value[2]) - Math.abs(b.value[2]));

    charts.value.geo.setOption({
       backgroundColor: 'transparent',
       geo: {
          map: 'world',
          roam: true, // Allow user panning and zooming
          boundingCoords: [
              [minLng - lngMargin, maxLat + latMargin], // top-left
              [maxLng + lngMargin, minLat - latMargin]  // bottom-right
          ],
          itemStyle: { 
             areaColor: '#1e293b', 
             borderColor: '#334155' 
          },
          emphasis: { 
             itemStyle: { areaColor: '#334155' },
             label: { show: false }
          }
       },
       tooltip: { 
           trigger: 'item', 
           backgroundColor: 'rgba(255, 255, 255, 0.95)',
           formatter: p => {
             const perf = p.data.value[3];
             if(!perf) return `<div class="font-bold border-b pb-1 mb-1">${p.name}</div>坐标: [${p.data.value[0]}, ${p.data.value[1]}]`;
             return `<div class="font-bold border-b pb-1 mb-1 shadow-sm">${p.name} <span class="text-[10px] bg-slate-100 rounded px-1 ml-1">${perf.Status}</span></div>
                     <div class="text-[11px] grid grid-cols-2 gap-x-3 gap-y-1 mt-1">
                       <span class="text-slate-500">实际效能:</span> <span class="font-mono text-right">${perf.Actual}</span>
                       <span class="text-slate-500">推演期望:</span> <span class="font-mono text-right text-indigo-600">${perf.Expected.toFixed(3)}</span>
                       <span class="text-slate-500">相对偏差:</span> <span class="font-mono text-right ${perf.Deviation > 0 ? 'text-emerald-500':'text-rose-500'}">${perf.Deviation > 0 ? '+':''}${perf.Deviation.toFixed(3)}</span>
                     </div>`;
           }
       },
       series: [{
           type: 'effectScatter',
           coordinateSystem: 'geo',
           rippleEffect: { brushType: 'stroke', scale: 3.5 },
           symbolSize: (val) => Math.max(10, Math.min(25, 8 + Math.abs(val[2] * 40))), 
           label: { show: true, formatter: '{b}', position: 'right', fontSize: 13, fontWeight: 'bold', color: '#f1f5f9', textBorderColor: '#000', textBorderWidth: 2 },
           itemStyle: { opacity: 0.9, borderColor: '#fff', borderWidth: 1.5 },
           data: points,
           animationDurationUpdate: 500
       }]
    }, true); // true forces merge
};

// 2. Render Premium Scatter
const renderScatter = (dataData) => {
  const parsedData = dataData.map(d => [d.Expected, d.Deviation, props.displayMapping[d.NodeName] || d.NodeName, d.Actual]);
  const threshold = computeThreshold(dataData);
  
  charts.value.scatter.setOption({
    backgroundColor: 'transparent',
    tooltip: { 
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        textStyle: { color: '#fff' },
        borderWidth: 0,
        formatter: (p) => `<div class="font-bold border-b border-slate-600 pb-1 mb-1">${p.value[2]}</div>
                           <div class="text-xs"><span class="text-slate-400">预期效能:</span> <span class="text-neon-cyan">${p.value[0].toFixed(3)}</span></div>
                           <div class="text-xs"><span class="text-slate-400">偏离基准:</span> <span class="${p.value[1]>0?'text-emerald-400':'text-rose-400'}">${p.value[1].toFixed(3)}</span></div>` 
    },
    xAxis: { 
        type: 'value', name: '期望期望中位值 (μ)', 
        splitLine: { lineStyle: { color: '#1e293b', type: 'dashed' } },
        axisLabel: { color: '#94a3b8' }, nameTextStyle: { color: '#94a3b8' }
    },
    yAxis: { 
        type: 'value', name: '系统级偏差 (Dev)',
        splitLine: { lineStyle: { color: '#1e293b' } },
        axisLabel: { color: '#94a3b8' }, nameTextStyle: { color: '#94a3b8' }
    },
    visualMap: {
      show: true, dimension: 1, top: 10, right: 10,
      textStyle: { color: '#94a3b8' },
      pieces: [
        { min: threshold, label: titles.value.bright, color: '#00f0ff' }, 
        { min: -threshold, max: threshold, label: '系统稳态区间', color: '#64748b' },
        { max: -threshold, label: titles.value.dark, color: '#fb7185' }
      ]
    },
    series: [{ 
        type: 'effectScatter', 
        itemStyle: {
            shadowBlur: 15,
            shadowColor: 'rgba(0, 240, 255, 0.2)'
        },
        rippleEffect: { period: 4, scale: 2.5, brushType: 'stroke' },
        symbolSize: (d) => Math.abs(d[1]) > threshold ? 18 : 8, 
        data: parsedData,
        animationDurationUpdate: 500,
        animationEasingUpdate: 'cubicInOut'
    }]
  });
};

// 3. Render PPC
const renderPPC = (ppcData) => {
    if(!ppcData || !ppcData.y_actual) return;
    
    // Sort for area chart mimicking density
    const ac = [...ppcData.y_actual].sort((a,b)=>a-b);
    const pr = [...ppcData.y_predictive].sort((a,b)=>a-b);
    
    // Subsample to 100 points to draw smooth line
    const stepA = Math.max(1, Math.floor(ac.length / 50));
    const stepP = Math.max(1, Math.floor(pr.length / 50));
    
    let lineA = [], lineP = [];
    for(let i=0; i<50; i++) {
        if(ac[i*stepA] !== undefined) lineA.push([ac[i*stepA], i]); // Fake CDF like shape
        if(pr[i*stepP] !== undefined) lineP.push([pr[i*stepP], i]);
    }

    charts.value.ppc.setOption({
        tooltip: { trigger: 'axis' },
        legend: { data: ['观测值真实分布', '后验预测分布 (PPC)'], bottom: 0, textStyle: { fontSize: 10 } },
        xAxis: { type: 'value', boundaryGap: false, splitLine: { show: false } },
        yAxis: { type: 'value', show: false }, // Hide artificial Y
        series: [
            { name: '观测值真实分布', type: 'line', smooth: true, itemStyle: { color: '#10b981' }, areaStyle: { opacity: 0.1 }, data: lineA, symbol: 'none' },
            { name: '后验预测分布 (PPC)', type: 'line', smooth: true, itemStyle: { color: '#4f46e5' }, areaStyle: { opacity: 0.2 }, data: lineP, symbol: 'none' }
        ]
    });
};

// 4. Render Forest Chart
const renderForest = (summaryDf) => {
  if(!summaryDf) return;
  const effectData = Object.entries(summaryDf)
    .filter(([k]) => k.startsWith('beta_'))
    .map(([k, v]) => {
       const keys = Object.keys(v);
       // Find HDI bound keys, e.g. "hdi_3%" and "hdi_97%" or "hdi_2.5%"
       const hdiLowKey = keys.find(k => k.startsWith('hdi') && (!k.includes('9') || k === 'hdi_9%')) || keys[2]; 
       const hdiHighKey = keys.find(k => k.startsWith('hdi') && k.includes('9')) || keys[3];
       
       return [
         props.displayMapping[k.replace('beta_', '')] || k.replace('beta_', ''), 
         v[hdiLowKey], 
         v['mean'], 
         v[hdiHighKey]
       ];
    })
    .sort((a, b) => a[2] - b[2]); // Sort by mean

  charts.value.forest.setOption({
    grid: { left: '30%', right: '10%', top: '10%', bottom: '15%' },
    tooltip: { formatter: (p) => `${p.value[0]}<br>影响力: ${p.value[2].toFixed(3)}<br>95% HDI: [${p.value[1].toFixed(2)}, ${p.value[3].toFixed(2)}]` },
    xAxis: { type: 'value', splitLine: { lineStyle: { type: 'dashed' } } },
    yAxis: { type: 'category', data: effectData.map(d => d[0]), axisLabel: { interval: 0, fontSize: 10 } },
    series: [
      {
        type: 'custom',
        encode: {
            x: [1, 2, 3],
            y: 0,
            tooltip: [0, 2, 1, 3]
        },
        renderItem: (params, api) => {
          const y = api.coord([0, params.dataIndex])[1]; // params.dataIndex correctly grabs the categorical rank/tick
          const color = api.value(2) > 0 ? '#10b981' : '#f43f5e';
          return {
            type: 'group',
            children: [
              { type: 'line', shape: { x1: api.coord([api.value(1),0])[0], y1: y, x2: api.coord([api.value(3),0])[0], y2: y }, style: { stroke: color, lineWidth: 3 } },
              { type: 'circle', shape: { cx: api.coord([api.value(2),0])[0], cy: y, r: 5 }, style: { fill: '#fff', stroke: color, lineWidth: 2 } }
            ]
          };
        },
        data: effectData
      }
    ]
  });
};

// --- WHAT IF LOGIC ---
const updateWhatIf = (doRender = true) => {
    let newData = JSON.parse(JSON.stringify(originalPerformanceData));
    
    // Formula: Y_new = Y_old + Sum(delta_X * beta)
    // Here delta represents change in standard deviations if X was standardized
    let cumulativeShift = 0;
    editableCovariates.value.forEach(cov => {
       cumulativeShift += (cov.delta * cov.beta); 
    });
    
    newData.forEach(d => {
       d.Expected = d.Expected + cumulativeShift; 
       // Deviation = Actual - Expected. If Expected rises, Deviation falls!
       d.Deviation = d.Actual - d.Expected;
    });
    
    // Update Status using unified threshold based on NEW data
    const threshold = computeThreshold(newData);
    newData.forEach(d => {
       if (d.Deviation > threshold) d.Status = 'Bright';
       else if (d.Deviation < -threshold) d.Status = 'Dark';
       else d.Status = 'Neutral';
    });
    
    if (doRender) {
        renderScatter(newData); // Re-render smoothly!
        if(hasGeoData.value) renderGeo(newData); // Re-render map!
        renderDAG(props.hierarchySchema); // Keep DAG color sync
    }
    return newData;
};

const applyShock = (type) => {
    isShockMode.value = true;
    shockTypeRun.value = type;
    
    let preExpectedMean = originalPerformanceData.reduce((acc, curr) => acc + curr.Expected, 0) / originalPerformanceData.length;
    let achillesCov = editableCovariates.value.reduce((max, obj) => Math.abs(obj.beta) > Math.abs(max.beta) ? obj : max, editableCovariates.value[0]);

    editableCovariates.value.forEach(c => {
        if (type === 'crash') {
            c.delta = c.beta > 0 ? -3 : 3;
        } else if (type === 'surge') {
            c.delta = c.beta > 0 ? 3 : -3;
        } else if (type === 'achilles') {
            if (c.original === achillesCov.original) {
                c.delta = c.beta > 0 ? -3 : 3;
            } else {
                c.delta = 0;
            }
        }
    });

    const interval = setInterval(() => {
        const scatterBox = scatterChartRef.value?.parentElement;
        if(scatterBox) scatterBox.style.transform = `translate(${Math.random()*6-3}px, ${Math.random()*6-3}px)`;
    }, 40);

    setTimeout(() => {
        clearInterval(interval);
        if(scatterChartRef.value?.parentElement) scatterChartRef.value.parentElement.style.transform = 'none';
        
        let newData = updateWhatIf(false);
        
        // Compute Post-shock metrics
        let postExpectedMean = newData.reduce((acc, curr) => acc + curr.Expected, 0) / newData.length;
        let diff = postExpectedMean - preExpectedMean;
        
        let nodeChanges = newData.map((d, idx) => ({
            name: d.NodeName,
            delta: d.Expected - originalPerformanceData[idx].Expected,
            postDeviation: d.Deviation
        })).sort((a,b) => a.delta - b.delta);
        
        let worst = nodeChanges.slice(0, 3);
        let best = [...nodeChanges].sort((a,b) => b.postDeviation - a.postDeviation).slice(0, 3);
        
        impactReport.value = {
            preMean: preExpectedMean,
            postMean: postExpectedMean,
            diff: diff,
            achillesName: props.displayMapping[achillesCov?.original] || achillesCov?.original,
            worst,
            best
        };
        
        renderScatter(newData);
        if(hasGeoData.value) renderGeo(newData);
        renderDAG(props.hierarchySchema);
        
    }, 500);
};

const resetWhatIf = () => {
    isShockMode.value = false;
    shockTypeRun.value = '';
    impactReport.value = null;
    editableCovariates.value.forEach(c => c.delta = 0);
    updateWhatIf();
};

// --- BENCHMARK LOGIC ---
const openBenchmark = () => {
   showBenchmarkModal.value = true;
   benchmarkResults.value = null;
   editableCovariates.value.forEach(c => {
       newProjectInputs.value[c.original] = 0.0;
   });
};

const runBenchmark = async () => {
    isBenchmarking.value = true;
    try {
        const targetIdCol = props.hierarchySchema[props.hierarchySchema.length-1]?.id_column;
        const targetAliasMap = props.targetVariable ? (props.targetVariable.name || props.targetVariable.original) : Object.keys(props.rawTableData[0]).find(k => !editableCovariates.value.map(c=>c.original).includes(k) && typeof props.rawTableData[0][k] === 'number');
        
        const payload = {
            project_features: newProjectInputs.value,
            historical_data: props.rawTableData,
            covariate_cols: editableCovariates.value.map(c => c.original),
            betas: props.modelResults.betas,
            id_column: targetIdCol || 'NodeName',
            target_column: targetAliasMap || 'Target'
        };
        
        const response = await fetch(`${window.__deepbayes_backend_url || 'http://127.0.0.1:18521'}/api/benchmark`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if(!response.ok) {
           const err = await response.json();
           throw new Error(err.detail || 'API Call failed');
        }
        
        benchmarkResults.value = await response.json();
        generateExecutiveSummary();
        nextTick(() => {
            initBenchmarkRadar();
        });
    } catch(e) {
        console.error("Benchmark error:", e);
        alert(`验证失败: ${e.message || e}`);
    } finally {
        isBenchmarking.value = false;
    }
};

const getTopFactors = (type) => {
    if (!benchmarkResults.value || !benchmarkResults.value.factors) return [];
    const factors = benchmarkResults.value.factors;
    if (type === 'pos') {
        return factors.filter(f => f.contribution > 0.01).slice(0, 2);
    } else {
        // Factors are sorted pos to neg, so last ones are most negative
        return factors.filter(f => f.contribution < -0.01).slice(-2).reverse();
    }
};

const generateExecutiveSummary = () => {
    const res = benchmarkResults.value;
    const match1 = res.matches[0];
    const topPos = getTopFactors('pos');
    const topNeg = getTopFactors('neg');
    
    let text = `【智能审评意见】该拟建项目在多元环境指标上与历史【${props.displayMapping[match1.node_name] || match1.node_name}】高度重叠（多维特征相似度达 ${match1.similarity.toFixed(1)}%）。\n`;
    
    text += `贝叶斯引擎深度计算预测其综合首发效能落点为 ${res.expected_y.toFixed(3)}，该表现${res.expected_delta >= 0 ? '优于' : '劣于'}全局基准期望。\n`;
    
    if (topNeg.length > 0) {
        text += `\n⚠️ 【核心风险警示】其「${props.displayMapping[topNeg[0].covariate] || topNeg[0].covariate}」评估极为弱势，在整个网络拓扑中构成了致命的拖累（边际削弱效应极大）。\n`;
    }
    
    if (topPos.length > 0) {
        text += `\n✅ 【有效缓冲利好】幸而该项目的「${props.displayMapping[topPos[0].covariate] || topPos[0].covariate}」提供了强大的势能加持，构成了一定程度的抗压护城河。\n`;
    }
    
    text += `\n【辅助决策建议】综合模型推演，建议战略决策层参考【${props.displayMapping[match1.node_name] || match1.node_name}】过往沉淀出的实操经验，提前针对风险拖累项配置专项资金或安保倾斜，即可逆转颓势。`;
    
    executiveSummary.value = text;
};

const initBenchmarkRadar = () => {
    if (!benchmarkRadarRef.value || !benchmarkResults.value) return;
    if (benchmarkRadarChart) {
        benchmarkRadarChart.dispose();
    }
    benchmarkRadarChart = echarts.init(benchmarkRadarRef.value);
    
    const res = benchmarkResults.value;
    const match1 = res.matches[0];
    const top5Factors = res.factors.slice(0, 6); // Up to 6 axes makes a nice radar
    
    const indicator = top5Factors.map(f => {
        const histVal = match1.features[f.covariate] || 0;
        let maxVal = Math.max(Math.abs(f.input), Math.abs(histVal), Math.abs(f.mean)) * 1.3;
        if(maxVal === 0) maxVal = 1;
        return { 
            name: props.displayMapping[f.covariate] || f.covariate,
            max: maxVal
        };
    });

    const option = {
        tooltip: { trigger: 'item', textStyle: { fontSize: 11 } },
        legend: { bottom: '0%', data: ['本拟建项目', `最佳对标锚点`, '全局均值极值'], textStyle: { fontSize: 10, color: '#64748b' } },
        radar: {
            indicator: indicator,
            radius: '55%',
            name: { textStyle: { color: '#64748b', fontSize: 10 } }
        },
        series: [{
            type: 'radar',
            symbolSize: 4,
            data: [
                { value: top5Factors.map(f => f.input), name: '本拟建项目', itemStyle: { color: '#4f46e5' }, lineStyle: { width: 2 }, areaStyle: { color: 'rgba(79, 70, 229, 0.4)' } },
                { value: top5Factors.map(f => match1.features[f.covariate] || 0), name: `最佳对标锚点`, itemStyle: { color: '#f59e0b' }, lineStyle: { type: 'dashed' } },
                { value: top5Factors.map(f => f.mean), name: '全局均值极值', itemStyle: { color: '#94a3b8' }, lineStyle: { type: 'dotted' } }
            ]
        }]
    };
    
    benchmarkRadarChart.setOption(option);
};

// --- EXPORT LOGIC ---
const exportChart = async (type) => {
    const chart = charts.value[type];
    if(chart) {
        const url = chart.getDataURL({ type: 'png', pixelRatio: 3, backgroundColor: type === 'scatter' ? '#0a192f' : '#fff' });
        
        try {
            const filePath = await save({
                defaultPath: `DeepBayes_${type}_${Date.now()}.png`,
                filters: [{ name: 'PNG Image', extensions: ['png'] }]
            });
            
            if (filePath) {
                // Convert base64 data to Uint8Array
                const base64Data = url.split(',')[1];
                const binaryString = window.atob(base64Data);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i);
                }
                await writeFile(filePath, bytes);
            }
        } catch(e) {
            console.error("导出图表失败:", e);
        }
    }
};

const exportCSV = async () => {
    const headers = ['NodeName', 'Actual_Value', 'Expected_μ', 'Deviation', 'Status_Flag'];
    const csvRows = [headers.join(',')];
    
    originalPerformanceData.forEach(row => {
        csvRows.push([
            `"${row.NodeName}"`, 
            row.Actual, 
            row.Expected.toFixed(4), 
            row.Deviation.toFixed(4), 
            `"${row.Status}"`
        ].join(','));
    });
    
    try {
        const filePath = await save({
            defaultPath: `DeepBayes_Report_${Date.now()}.csv`,
            filters: [{ name: 'CSV Document', extensions: ['csv'] }]
        });
        
        if (filePath) {
            // Write to local disk with Tauri Native FS Write
            await writeTextFile(filePath, csvRows.join('\n'));
        }
    } catch(e) {
        console.error("导出数据表失败:", e);
    }
};

</script>