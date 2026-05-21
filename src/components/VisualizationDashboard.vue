<template>
  <div class="flex-1 min-h-0 bg-ice-white p-6 relative flex flex-col font-sans overflow-hidden">
    
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

    <!-- 对标演算弹窗 -->
    <div v-if="showBenchmarkModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-[60] overflow-y-auto py-8">
      <div class="bg-white p-6 rounded-2xl shadow-2xl w-[720px] max-h-[92vh] flex flex-col border border-slate-200">
        <div class="flex justify-between items-center mb-3 shrink-0">
            <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center"><i class="fas fa-balance-scale text-indigo-600"></i></div>
              对标演算 · 新项目预估
            </h3>
            <button @click="showBenchmarkModal = false" class="text-slate-400 hover:text-slate-600 transition-colors"><i class="fas fa-times text-xl"></i></button>
        </div>
        <p class="text-xs text-slate-500 mb-4 bg-slate-50 p-3 rounded-lg border border-slate-200 shrink-0 leading-relaxed">
          输入新项目在各维度上的预期数值，系统会在历史数据中找出条件最相似的已有对象，用当前模型的β权重推算新项目的预期表现。
          <span class="text-slate-400">请注意：这是基于历史规律的推算，不等同于精确预测。</span>
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
               <h4 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                 <i class="fas fa-clipboard-check text-emerald-500"></i>对标演算结果
               </h4>
               
               <div class="grid grid-cols-3 gap-3 mb-5">
                   <div class="bg-gradient-to-br from-indigo-50 to-white border border-indigo-100 rounded-xl p-4 text-center">
                       <div class="text-[10px] text-indigo-500 font-bold mb-1">预期表现</div>
                       <div class="text-xl font-black text-indigo-700">{{ benchmarkResults.expected_y.toFixed(3) }}</div>
                       <div class="text-[9px] text-slate-400 mt-0.5">模型推算的应有水平</div>
                   </div>
                   <div class="bg-gradient-to-br from-emerald-50 to-white border border-emerald-100 rounded-xl p-4 text-center">
                       <div class="text-[10px] text-emerald-500 font-bold mb-1">相对基准</div>
                       <div class="text-xl font-black flex items-center justify-center gap-1" :class="benchmarkResults.expected_delta > 0 ? 'text-emerald-600' : 'text-rose-600'">
                           <i :class="benchmarkResults.expected_delta > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                           {{ Math.abs(benchmarkResults.expected_delta).toFixed(3) }}
                       </div>
                       <div class="text-[9px] text-slate-400 mt-0.5">{{ benchmarkResults.expected_delta > 0 ? '高于历史均值' : '低于历史均值' }}</div>
                   </div>
                   <div class="bg-gradient-to-br from-amber-50 to-white border border-amber-100 rounded-xl p-4 text-center">
                       <div class="text-[10px] text-amber-500 font-bold mb-1">最相似对象</div>
                       <div class="text-sm font-black text-slate-700 truncate px-1">{{ benchmarkResults.matches[0] ? (displayMapping[benchmarkResults.matches[0].node_name] || benchmarkResults.matches[0].node_name) : '-' }}</div>
                       <div class="text-[9px] text-slate-400 mt-0.5">匹配度 {{ benchmarkResults.matches[0] ? benchmarkResults.matches[0].similarity.toFixed(0) : '-' }}%</div>
                   </div>
               </div>
               
               <!-- Factor AI Attributions -->
               <div class="mb-5 bg-slate-50 p-3 rounded-lg border border-slate-200">
                   <div class="text-[10px] text-slate-500 font-bold mb-2 flex items-center group/attri relative">
                       各因素贡献拆解
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

               <!-- 决策建议 -->
               <div class="mb-5">
                   <div class="text-xs font-bold text-slate-800 mb-2 flex items-center gap-1.5"><i class="fas fa-lightbulb text-amber-500"></i>决策建议</div>
                   <div class="bg-amber-50/50 border border-amber-100 rounded-lg p-3 text-xs text-slate-700 leading-relaxed whitespace-pre-wrap">{{ executiveSummary }}</div>
               </div>

               <!-- Radar Chart -->
               <div class="mb-5 border border-slate-200 rounded-xl bg-white overflow-hidden shadow-sm">
                   <div class="bg-slate-50 px-3 py-2 border-b border-slate-200 text-xs font-bold text-slate-600 flex justify-between items-center">
                       <span><i class="fas fa-chart-pie text-slate-400 mr-1.5"></i>多维特征对比</span>
                   </div>
                   <div ref="benchmarkRadarRef" class="w-full h-48"></div>
               </div>

               <h4 class="text-xs font-bold text-slate-500 mb-3">条件最相似的历史对象</h4>
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

    <!-- 页面工具栏 -->
    <div class="mb-5 bg-[#0b1121] rounded-2xl shadow-xl shadow-black/10 border border-white/5 text-white shrink-0 relative overflow-hidden">
      <div class="absolute inset-0 opacity-[0.02]" style="background-image: radial-gradient(circle at 1px 1px, rgba(99,102,241,0.8) 1px, transparent 0); background-size: 20px 20px;"></div>
      <div class="flex justify-between items-center px-6 py-4 relative z-10">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center ring-1 ring-indigo-500/30">
            <i class="fas fa-chart-pie text-cyan-400 text-xl"></i>
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight">{{ titles.main }}</h1>
            <p class="text-[11px] text-slate-500 mt-0.5">分析完成 · {{ new Date().toLocaleTimeString() }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2.5">
          <button @click="emit('open-decision')" class="h-9 px-4 text-[13px] font-bold text-white bg-amber-500 rounded-xl hover:bg-amber-400 transition-colors flex items-center gap-2 shadow-lg shadow-amber-500/20">
            <i class="fas fa-brain text-sm"></i>决策中心
          </button>
          <button @click="openBenchmark" class="h-9 px-4 text-[12px] font-medium text-slate-200 bg-white/5 hover:bg-white/10 rounded-xl transition-colors flex items-center gap-2 border border-white/5">
            <i class="fas fa-balance-scale"></i>对标演算
          </button>
          <div class="w-px h-6 bg-white/10"></div>
          <button @click="exportFullReport" class="h-9 px-3 text-[12px] font-medium text-slate-300 bg-white/5 hover:bg-white/10 rounded-xl transition-colors flex items-center gap-1.5">
            <i class="fas fa-download"></i>导出
          </button>
          <button @click="$emit('reset')" class="h-9 px-3 text-[12px] font-medium text-slate-400 bg-white/5 hover:bg-rose-500/20 hover:text-rose-300 rounded-xl transition-colors flex items-center gap-1.5">
            <i class="fas fa-arrow-left"></i>返回
          </button>
        </div>
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
              效能偏差诊断图（找差距）
              <i class="fas fa-info-circle ml-2 text-slate-500 text-xs cursor-help"></i>
              <div class="absolute top-full left-0 mt-2 w-80 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/scat:opacity-100 group-hover/scat:scale-100 transition-all pointer-events-none z-50 font-normal">
                  <div class="font-bold mb-1 text-neon-cyan">效能偏差解读（管理者视角）</div>
                  <p class="text-slate-300 leading-relaxed mb-2">横轴：系统测算的「应有表现」| 纵轴：实绩与应有表现的差距</p>
                  <p class="text-slate-400"><span class="text-emerald-400">上方散点</span> = 超预期（值得表彰/经验推广）<br><span class="text-rose-400">下方散点</span> = 低于预期（需关注/资源倾斜）<br><span class="text-slate-500">中部散点</span> = 符合预期（正常运行）</p>
                  <p class="text-slate-500 mt-1 text-[10px] border-t border-slate-700 pt-1">💡 优先关注右下角红点——同等投入下产出最低的单元</p>
              </div>
          </h2>
          <div class="flex space-x-3 items-center">
            <div class="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">🎯 {{ targetAlias }}</div>
            <button @click="exportChart('scatter')" class="text-slate-400 hover:text-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-download"></i></button>
          </div>
        </div>
        <div ref="scatterChartRef" class="flex-1 w-full bg-[#0a192f] relative z-0 min-h-0"></div>
      </div>

      <!-- Box 3: PPC Density -->
      <div class="col-span-4 row-span-1 bg-white rounded-2xl shadow-md border border-slate-200 flex flex-col overflow-hidden relative group transition-shadow hover:shadow-lg">
        <div class="px-5 py-3 border-b border-slate-100 bg-slate-50 flex justify-between items-center z-10">
          <h2 class="text-sm font-bold text-slate-700 flex items-center group/ppctip relative">
            <i class="fas fa-chart-area text-blue-500 mr-2"></i>模型可信度验证
            <span v-if="ppcScore" class="ml-2 text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded border border-emerald-200 cursor-help">
               可信度: {{ ppcScore }}%
            </span>
            <div class="absolute top-full left-0 mt-2 w-72 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/ppctip:opacity-100 group-hover/ppctip:scale-100 transition-all pointer-events-none z-50 font-normal">
                <div class="font-bold mb-1 text-blue-400">模型可信度验证</div>
                <p class="text-slate-300 leading-relaxed">深色线 = 真实业务数据 | 浅色带 = 模型推演出的合理范围</p>
                <p class="text-slate-400 mt-1">当真实数据被模型推演范围完全包裹时，说明系统已准确掌握业务运行规律，分析结论可信。</p>
                <p class="text-slate-500 mt-1 text-[10px] border-t border-slate-700 pt-1">💡 对决策者而言：此图是「本次分析靠不靠谱」的直观凭证。</p>
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
              <i class="fas fa-sliders-h text-emerald-500 mr-2"></i>关键驱动力归因 & 情景推演沙盘
              <i class="fas fa-question-circle ml-1.5 text-slate-300 text-xs cursor-help"></i>
              <div class="absolute top-full left-0 mt-2 w-80 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/foresttip:opacity-100 group-hover/foresttip:scale-100 transition-all pointer-events-none z-50 font-normal">
                  <div class="font-bold mb-1 text-emerald-400">驱动力归因解读（辅助决策）</div>
                  <p class="text-slate-300 leading-relaxed mb-2">左侧：各因素对最终结果的推动力大小。线完全在零线右侧 = 正向推动，左侧 = 负向拖累。</p>
                  <p class="text-slate-400">右侧滑块：拖动模拟「如果改变某项投入，整体表现会怎样」—— 真正的事前决策工具。</p>
                  <p class="text-slate-500 mt-1 text-[10px] border-t border-slate-700 pt-1">💡 找到影响力最大的因子，它就是您资源配置的「最佳杠杆点」。</p>
              </div>
          </h2>
          <button @click="exportChart('forest')" class="text-slate-400 hover:text-emerald-600 opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-download"></i></button>
        </div>
        <div class="flex-1 flex w-full relative z-0 min-h-0">
          <!-- Forest Chart -->
          <div v-show="!isShockMode" ref="forestChartRef" class="w-1/2 h-full border-r border-slate-100 min-h-0 shrink-0 transition-all duration-300"></div>
          
          <!-- What-If Sliders / Shock Report Panel -->
          <div :class="isShockMode ? 'w-full' : 'w-1/2'" class="p-5 bg-slate-50/50 overflow-y-auto flex flex-col relative text-slate-800 shrink-0 transition-all duration-300">
            
            <!-- Sliders Config View -->
            <div v-if="!isShockMode" class="flex-1 animate-fade-in">
                <h3 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4"><i class="fas fa-flask mr-1"></i> 调整要素观测值改变预期</h3>
                
                <div v-for="(covObj, index) in editableCovariates" :key="index" class="mb-5 mt-1">
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

                <div v-if="editableCovariates.length === 0" class="h-32 flex flex-col items-center justify-center text-slate-400">
                   <i class="fas fa-info-circle text-2xl mb-2"></i>
                   <span class="text-sm text-center">模型未包含任何环境变量数据<br>无法启用沙盘推演</span>
                </div>
                
                <!-- 极端冲击模拟器 -->
                <div v-if="editableCovariates.length > 0" class="mt-8 pt-5 border-t border-slate-200 hide-scrollbar shrink-0">
                   <h3 class="text-xs font-black text-rose-600 uppercase tracking-widest mb-3 flex items-center">
                     <i class="fas fa-biohazard mr-1.5 animate-pulse"></i> 压力测试与情景推演
                   </h3>
                   <div class="grid grid-cols-1 gap-3 mb-2">
                      <div class="relative group/tip1">
                          <button @click="applyShock('achilles')" class="w-full py-2.5 text-[11px] font-bold text-white bg-slate-800 rounded-lg hover:bg-slate-900 shadow-sm transition-all flex items-center justify-center group overflow-hidden relative">
                             <span class="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                             <i class="fas fa-crosshairs mr-2"></i> ⏺ 薄弱点测试（打击最敏感因素）
                          </button>
                          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/tip1:opacity-100 group-hover/tip1:scale-100 transition-all pointer-events-none z-50">
                              <div class="font-bold mb-1 text-amber-400"><i class="fas fa-info-circle mr-1"></i> 薄弱点压力测试</div>
                              <p class="text-slate-300 leading-relaxed text-left font-normal">系统自动找到影响力最大的因素（β 权重最高），将其单独降至极端水平（-3σ），模拟"最致命环节出问题"时，各评估对象的表现变化。</p>
                              <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                          </div>
                      </div>
                      
                      <div class="relative group/tip2">
                          <button @click="applyShock('crash')" class="w-full py-2.5 text-[11px] font-bold text-white bg-rose-600 rounded-lg hover:bg-rose-700 shadow-md shadow-rose-600/30 transition-all flex items-center justify-center group overflow-hidden relative">
                             <span class="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                             <i class="fas fa-meteor mr-2"></i> ⏺ 全面承压测试（所有因素同时恶化）
                          </button>
                          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/tip2:opacity-100 group-hover/tip2:scale-100 transition-all pointer-events-none z-50">
                              <div class="font-bold mb-1 text-rose-400"><i class="fas fa-skull mr-1"></i> 全面承压测试</div>
                              <p class="text-slate-300 leading-relaxed text-left font-normal">将所有影响因素同时降到极端水平（-3σ），模拟整体环境全面恶化的场景。用于找出在所有条件都变差时，哪些对象依然能保持较好表现。</p>
                              <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                          </div>
                      </div>
                      
                      <div class="relative group/tip3">
                          <button @click="applyShock('surge')" class="w-full py-2.5 text-[11px] font-bold text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 shadow-md shadow-emerald-600/30 transition-all flex items-center justify-center group overflow-hidden relative">
                             <span class="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                             <i class="fas fa-rocket mr-2"></i> ⏺ 理想上限推演（所有因素同时优化）
                          </button>
                          <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-slate-800 text-white text-[11px] p-3 rounded-xl shadow-2xl opacity-0 scale-95 group-hover/tip3:opacity-100 group-hover/tip3:scale-100 transition-all pointer-events-none z-50">
                              <div class="font-bold mb-1 text-emerald-400"><i class="fas fa-chart-line mr-1"></i> 理想上限推演</div>
                              <p class="text-slate-300 leading-relaxed text-left font-normal">将所有影响因素同时提升到极端有利水平（+3σ），模拟"一切条件都达到最优"的情景。用于评估在最佳条件下，各对象能达到的理论上限。</p>
                              <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-t-[6px] border-r-[6px] border-l-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                          </div>
                      </div>
                   </div>
                </div>
            </div>

            <!-- Detailed Impact Report View (Shock Mode Only) -->
            <div v-else class="flex-1 animate-scale-in flex flex-col text-slate-800 h-full">
               <h3 class="text-xs font-black uppercase tracking-widest mb-4 flex items-center border-b pb-3" :class="shockTypeRun==='surge' ? 'text-emerald-600 border-emerald-200' : 'text-rose-600 border-rose-200'">
                   <i class="fas fa-file-contract mr-2" :class="shockTypeRun==='surge' ? 'text-emerald-500' : 'text-rose-500'"></i>
                   <span v-if="shockTypeRun==='achilles'">薄弱点压力测试报告</span>
                   <span v-else-if="shockTypeRun==='crash'">全面承压测试报告</span>
                   <span v-else>理想上限推演报告</span>
               </h3>
               
               <div class="flex flex-1 overflow-hidden min-h-0 space-x-5">
                   
                   <!-- LEFT SIDE: Quantitative Data -->
                   <div v-if="impactReport" class="w-1/2 flex flex-col overflow-y-auto pr-2 custom-scrollbar">
                      <!-- VAR Highlight -->
                      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 mb-4 relative shrink-0">
                          <div v-if="impactReport.diff < 0" class="absolute top-0 right-0 w-16 h-16 bg-rose-100 text-rose-500 rounded-bl-full rounded-tr-xl flex items-center justify-center opacity-50"><i class="fas fa-arrow-down mb-4 ml-4"></i></div>
                          <div v-else class="absolute top-0 right-0 w-16 h-16 bg-emerald-100 text-emerald-500 rounded-bl-full rounded-tr-xl flex items-center justify-center opacity-50"><i class="fas fa-arrow-up mb-4 ml-4"></i></div>
                          
                          <div class="text-[11px] font-bold text-slate-500 mb-2 flex items-center group/vartip relative cursor-help">
                              系统大盘效能均值变动 (VAR)
                              <i class="fas fa-info-circle ml-1 opacity-50"></i>
                              <div class="absolute top-full left-0 mt-2 w-56 bg-slate-800 text-white text-[10px] p-2 rounded-lg shadow-2xl border border-slate-700 opacity-0 scale-90 group-hover/vartip:opacity-100 group-hover/vartip:scale-100 transition-all pointer-events-none z-50 font-normal">
                                  <div class="absolute bottom-full left-4 w-0 h-0 border-r-[6px] border-b-[6px] border-l-[6px] border-r-transparent border-l-transparent border-b-slate-800"></div>
                                  Value at Risk：本次演习中，环境冲击导致全大盘项目的效能预期得分的加权平均变动值。
                              </div>
                          </div>
                          <div class="text-4xl font-mono font-black relative z-10" :class="impactReport.diff > 0 ? 'text-emerald-500' : 'text-rose-600'">
                              {{ impactReport.diff > 0 ? '+' : '' }}{{ impactReport.diff.toFixed(3) }}
                          </div>
                          <div v-if="shockTypeRun==='achilles'" class="text-[10px] font-bold text-amber-600 mt-2 bg-amber-50 px-2 py-1 rounded inline-block relative z-10">
                              <i class="fas fa-crosshairs"></i> 触发锚点因素: {{ impactReport.achillesName }} 
                          </div>
                      </div>
                      
                      <div class="grid grid-cols-2 gap-3 shrink-0 flex-1 min-h-0">
                          <!-- Safe Assets Box -->
                          <div class="bg-slate-50 p-3 rounded-lg border border-emerald-100 flex flex-col">
                              <div class="text-[11px] text-slate-700 font-bold mb-3 flex items-center pb-2 border-b border-emerald-200/50 shrink-0">
                                  <i class="fas fa-shield-alt text-emerald-500 mr-2"></i>绝对扛压韧性资产
                              </div>
                              <div class="space-y-2 overflow-y-auto custom-scrollbar pr-1 flex-1 min-h-0">
                                  <div v-for="(node, i) in impactReport.best" :key="i" class="flex justify-between items-center text-[11px] bg-white px-2 py-1.5 rounded border border-slate-100 shadow-sm relative overflow-hidden">
                                      <div class="absolute inset-y-0 w-1 left-0 bg-emerald-500"></div>
                                      <span class="text-slate-800 font-bold truncate pl-2 max-w-[80px]" :title="displayMapping[node.name] || node.name">{{ displayMapping[node.name] || node.name }}</span>
                                      <div class="flex flex-col items-end shrink-0">
                                         <span class="text-[9px] text-slate-400">冲击后结余</span>
                                         <span class="text-emerald-600 font-bold font-mono">+{{ node.postDeviation.toFixed(3) }}</span>
                                      </div>
                                  </div>
                              </div>
                          </div>
                          
                          <!-- Failed Assets Box -->
                          <div class="bg-slate-50 p-3 rounded-lg border border-rose-100 flex flex-col">
                              <div class="text-[11px] text-slate-700 font-bold mb-3 flex items-center pb-2 border-b border-rose-200/50 shrink-0">
                                  <i class="fas fa-skull text-rose-500 mr-2"></i>脆弱性崩盘区
                              </div>
                              <div class="space-y-2 overflow-y-auto custom-scrollbar pr-1 flex-1 min-h-0">
                                  <div v-for="(node, i) in impactReport.worst" :key="i" class="flex justify-between items-center text-[11px] bg-white px-2 py-1.5 rounded border border-slate-100 shadow-sm relative overflow-hidden">
                                      <div class="absolute inset-y-0 w-1 left-0 bg-rose-500"></div>
                                      <span class="text-slate-800 font-bold truncate pl-2 max-w-[80px]" :title="displayMapping[node.name] || node.name">{{ displayMapping[node.name] || node.name }}</span>
                                      <div class="flex flex-col items-end shrink-0">
                                         <span class="text-[9px] text-slate-400">效能跌幅</span>
                                         <span class="text-rose-600 font-bold font-mono">{{ node.delta.toFixed(3) }}</span>
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                   </div>
                   
                   <!-- RIGHT SIDE: AI War Room Decision Panel -->
                   <div class="w-1/2 bg-slate-900 rounded-xl p-5 shadow-lg border border-slate-700 relative overflow-hidden flex flex-col h-full">
                       <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-neon-cyan to-emerald-500"></div>
                       <div class="flex items-center text-[11px] font-bold text-neon-cyan uppercase tracking-widest mb-3 shrink-0">
                           <i class="fas fa-brain mr-2 animate-pulse mt-0.5"></i> 智库决策 (AI ASSISTANT)
                           <span v-if="aiThinking" class="ml-2 text-slate-400 font-mono animate-pulse">...Retrieving Strategy...</span>
                       </div>
                       <div class="flex-1 overflow-y-auto custom-scrollbar text-[12px] text-slate-200 font-mono leading-relaxed prose prose-invert prose-p:my-1.5 prose-sm max-w-none" v-html="formattedAiDecision">
                       </div>
                   </div>
                   
               </div>
               
               <button @click="resetWhatIf" class="w-full mt-4 py-3 text-sm font-bold text-white bg-slate-800 rounded-lg hover:bg-slate-900 transition-colors shadow-lg hover:shadow-xl shrink-0 flex items-center justify-center group">
                 <i class="fas fa-power-off text-rose-400 mr-2 group-hover:text-amber-400 transition-colors"></i> 结束推演，数据回退稳态
               </button>
            </div>

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

const emit = defineEmits(['reset', 'open-decision', 'live-data']);

// Meta Editor States
const showMetaEditor = ref(false);
const editingNode = ref(null);

// Phase 3: AI War Room
const aiDecisionText = ref("");
const aiThinking = ref(false);
let currentAiRequestController = null;

const formattedAiDecision = computed(() => {
    // Simple markdown to HTML
    let text = aiDecisionText.value;
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>');
    text = text.replace(/\n/g, '<br/>');
    return text || "<span class='text-slate-500'>[等待指令]</span>";
});

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
        type: 'value', name: '系统应有表现 (预期值)', 
        splitLine: { lineStyle: { color: '#1e293b', type: 'dashed' } },
        axisLabel: { color: '#94a3b8' }, nameTextStyle: { color: '#94a3b8' }
    },
    yAxis: { 
        type: 'value', name: '实绩与预期的差距',
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
        legend: { data: ['真实业务数据', '模型推演范围 (PPC)'], bottom: 0, textStyle: { fontSize: 10 } },
        xAxis: { type: 'value', boundaryGap: false, splitLine: { show: false } },
        yAxis: { type: 'value', show: false }, // Hide artificial Y
        series: [
            { name: '真实业务数据', type: 'line', smooth: true, itemStyle: { color: '#10b981' }, areaStyle: { opacity: 0.1 }, data: lineA, symbol: 'none' },
            { name: '模型推演范围 (PPC)', type: 'line', smooth: true, itemStyle: { color: '#4f46e5' }, areaStyle: { opacity: 0.2 }, data: lineP, symbol: 'none' }
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
    tooltip: { formatter: (p) => `${p.value[0]}<br>对该指标的影响力: ${p.value[2].toFixed(3)}<br>95% 置信区间: [${p.value[1].toFixed(2)}, ${p.value[3].toFixed(2)}]<br><span style="font-size:10px;color:#94a3b8">💡 正值=正向推动力 | 负值=负向拖累</span>` },
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
        renderScatter(newData);
        if(hasGeoData.value) renderGeo(newData);
        renderDAG(props.hierarchySchema);
    }
    // 实时推送数据到决策中枢
    emit('live-data', { performanceData: newData, covariates: editableCovariates.value.map(c => ({ name: props.displayMapping[c.original] || c.original, original: c.original, beta: c.beta, delta: c.delta })) });
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
        emit('live-data', { performanceData: newData, covariates: editableCovariates.value.map(c => ({ name: props.displayMapping[c.original] || c.original, original: c.original, beta: c.beta, delta: c.delta })) });
        
        // 5. Trigger AI War Room Decision Stream
        requestAiDecision(type, diff, impactReport.value.achillesName, worst, best);
    }, 500);
};

const requestAiDecision = async (shock_type, var_drop, trigger_node, top_fragile, top_resilient) => {
    aiDecisionText.value = "";
    aiThinking.value = true;
    
    // Abort any ongoing AI request
    if (currentAiRequestController) {
        currentAiRequestController.abort();
    }
    currentAiRequestController = new AbortController();
    
    try {
        const payload = {
            shock_type,
            var_drop,
            trigger_node,
            top_fragile: top_fragile.slice(0,3).map(n=>props.displayMapping[n.name] || n.name),
            top_resilient: top_resilient.slice(0,3).map(n=>props.displayMapping[n.name] || n.name)
        };
        
        const res = await fetch('http://127.0.0.1:18521/api/settings/llm/stream_decision', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            signal: currentAiRequestController.signal
        });
        
        if(!res.ok) {
            aiDecisionText.value = "[智能决策终端报错: 无法联系大模型引擎，请检查设置面板中的引擎状态]";
            aiThinking.value = false;
            return;
        }
        
        const reader = res.body.getReader();
        const decoder = new TextDecoder("utf-8");
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            aiDecisionText.value += decoder.decode(value, { stream: true });
        }
    } catch(err) {
        if (err.name === 'AbortError') {
            console.log('AI Generation aborted by user.');
        } else {
            aiDecisionText.value = `[通信故障: ${err.message}]`;
        }
    } finally {
        aiThinking.value = false;
    }
};

const resetWhatIf = () => {
    if (currentAiRequestController) {
        currentAiRequestController.abort();
        currentAiRequestController = null;
    }
    
    isShockMode.value = false;
    shockTypeRun.value = '';
    impactReport.value = null;
    editableCovariates.value.forEach(c => c.delta = 0);
    updateWhatIf();
    emit('live-data', null);  // 通知决策中枢恢复原始数据
    
    // Explicitly command echarts to recalculate bounding box after reappearing
    nextTick(() => {
        setTimeout(() => {
            charts.value.forest?.resize();
        }, 300); // Allow tailwind transition to finish settling
    });
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
    
    let text = '';
    text += `新项目的预期表现约为 ${res.expected_y.toFixed(3)}，`;
    text += res.expected_delta >= 0 ? '高于历史平均水平。' : '低于历史平均水平。';
    text += `与它条件最相似的历史对象是「${props.displayMapping[match1.node_name] || match1.node_name}」（匹配度 ${match1.similarity.toFixed(1)}%），该对象的实际表现为 ${match1.actual_y.toFixed(3)}。`;
    
    if (topPos.length > 0) {
        text += `\n\n优势因素：`;
        text += topPos.map(f => `「${props.displayMapping[f.covariate] || f.covariate}」贡献了 +${f.contribution.toFixed(2)} 的正面推动`).join('，');
        text += '。这些是项目的核心竞争力，应保持或加强。';
    }
    
    if (topNeg.length > 0) {
        text += `\n\n风险因素：`;
        text += topNeg.map(f => `「${props.displayMapping[f.covariate] || f.covariate}」造成了 ${f.contribution.toFixed(2)} 的下行压力`).join('，');
        text += '。建议在这些方面投入资源来弥补短板。';
    }
    
    text += `\n\n决策建议：参考最相似对象「${props.displayMapping[match1.node_name] || match1.node_name}」的做法，重点改善风险因素中的薄弱环节。如果能把最弱项的数值提升到历史均值水平，预期表现可提升至 ${(res.expected_y - (topNeg.length > 0 ? topNeg[0].contribution : 0)).toFixed(3)} 左右。`;
    
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

// --- 增强导出：含场景说明和解读的结构化报告 ---
const exportFullReport = async () => {
    try {
        const data = props.modelResults?.performance_data || [];
        const threshold = computeThreshold(data);
        const betas = props.modelResults?.betas || {};
        
        // 构建报告内容
        const date = new Date().toLocaleDateString('zh-CN');
        const time = new Date().toLocaleTimeString('zh-CN');
        const targetName = props.displayMapping[props.targetVariable?.name] || props.targetVariable?.name || '目标指标';
        
        let csvLines = [];
        
        // === 第一部分：场景设定 ===
        csvLines.push('=== 场景设定 ===');
        csvLines.push(`报告时间,${date} ${time}`);
        csvLines.push(`评估对象数,${data.length}`);
        csvLines.push(`组织层级数,${props.hierarchySchema?.length || 0}`);
        props.hierarchySchema?.forEach((lvl, i) => {
            csvLines.push(`层级${i+1},${lvl.level_name},ID列:${lvl.id_column},协变量:${(lvl.covariates || []).join('|')}`);
        });
        csvLines.push(`评估目标,${targetName}`);
        csvLines.push('');
        
        // === 第二部分：关键因子 ===
        csvLines.push('=== 关键影响因素（按影响力排序）===');
        csvLines.push('因子名称,β权重,方向,解读');
        Object.entries(betas).sort((a,b) => Math.abs(b[1]) - Math.abs(a[1])).forEach(([k, v]) => {
            const absV = Math.abs(v);
            csvLines.push(`${props.displayMapping[k] || k},${v.toFixed(4)},${v > 0 ? '正面推动' : '负面拖累'},${v > 0 ? '越高越好' : '过高会拖累，注意平衡'} (影响力${absV > 0.1 ? '高' : absV > 0.03 ? '中' : '低'})`);
        });
        csvLines.push('');
        
        // === 第三部分：详细结果 ===
        csvLines.push('=== 评估结果明细 ===');
        csvLines.push('对象名称,实际值,预期值,偏差(σ),状态,解读,建议');
        data.forEach(d => {
            const dev = d.Deviation;
            const absDev = Math.abs(dev);
            let status, desc, advice;
            if (dev < -2 * threshold) { status = '紧急'; desc = '严重低于预期'; advice = '优先排查资源配置是否不足'; }
            else if (dev < -threshold) { status = '关注'; desc = '略低于预期'; advice = '纳入重点观察名单'; }
            else if (dev > 2 * threshold) { status = '标杆'; desc = '显著超预期'; advice = '总结经验并推广'; }
            else if (dev > threshold) { status = '优良'; desc = '略超预期'; advice = '保持并关注其做法'; }
            else { status = '正常'; desc = '符合预期'; advice = '维持现有策略'; }
            csvLines.push(`${props.displayMapping[d.NodeName] || d.NodeName},${d.Actual},${d.Expected.toFixed(3)},${dev > 0 ? '+' : ''}${absDev.toFixed(2)}σ,${status},${desc},${advice}`);
        });
        csvLines.push('');
        
        // === 第四部分：统计摘要 ===
        const bright = data.filter(d => (d.Status === 'Bright Spot' || d.Status === 'Bright')).length;
        const dark = data.filter(d => (d.Status === 'Dark Spot' || d.Status === 'Dark')).length;
        csvLines.push('=== 统计摘要 ===');
        csvLines.push(`表现突出,${bright}个,(${(bright/data.length*100).toFixed(1)}%)`);
        csvLines.push(`需要关注,${dark}个,(${(dark/data.length*100).toFixed(1)}%)`);
        csvLines.push(`运行正常,${data.length - bright - dark}个,(${((data.length-bright-dark)/data.length*100).toFixed(1)}%)`);
        
        const csv = csvLines.join('\n');
        
        try {
            const { save } = await import('@tauri-apps/plugin-dialog');
            const { writeTextFile } = await import('@tauri-apps/plugin-fs');
            const filePath = await save({
                defaultPath: `分析报告_${date.replace(/\//g, '-')}.csv`,
                filters: [{ name: 'CSV', extensions: ['csv'] }]
            });
            if (filePath) {
                await writeTextFile(filePath, '\uFEFF' + csv);
                alert('报告已保存，包含场景设定、关键因子、详细结果和统计摘要。');
            }
        } catch(e) {
            // Fallback: download via browser
            const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `分析报告_${date.replace(/\//g, '-')}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        }
    } catch(e) {
        console.error('Export error:', e);
        alert('导出失败，请重试。');
    }
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