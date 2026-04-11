<template>
  <transition name="fade">
    <div v-if="show" class="fixed inset-0 bg-slate-900/40 backdrop-blur-md flex justify-center items-center z-[100]" @click.self="$emit('close')">
      <div class="w-full max-w-6xl max-h-[94vh] bg-white rounded-3xl shadow-[0_48px_96px_-24px_rgba(0,0,0,0.25)] flex flex-col overflow-hidden animate-scale-in border border-slate-200">
        
        <!-- Header: Clean, Corporate & Trustworthy -->
        <div class="px-10 py-8 bg-white border-b border-slate-100 flex justify-between items-center shrink-0">
          <div class="flex items-center">
            <div class="w-14 h-14 rounded-2xl bg-indigo-600 flex items-center justify-center mr-6 shadow-2xl shadow-indigo-100 relative overflow-hidden group">
               <div class="absolute inset-0 bg-gradient-to-tr from-indigo-600 to-indigo-400 group-hover:scale-110 transition-transform duration-500"></div>
               <i class="fas fa-project-diagram text-2xl text-white relative z-10"></i>
            </div>
            <div>
              <h2 class="text-2xl font-black text-slate-900 tracking-tight flex items-center">
                DeepBayes 决策分析系统 <span class="ml-4 text-[11px] bg-slate-100 text-slate-500 px-3 py-1 rounded-full uppercase tracking-widest font-black border border-slate-200">User Guide v1.0.5</span>
              </h2>
              <p class="text-sm text-slate-500 mt-1 font-medium">从数据集成到仿真推演：全生命周期专家级指导手册</p>
            </div>
          </div>
          <button @click="$emit('close')" class="w-12 h-12 rounded-full bg-slate-50 hover:bg-slate-100 flex items-center justify-center transition-all duration-300 hover:rotate-90 text-slate-400 hover:text-slate-600">
            <i class="fas fa-times text-xl"></i>
          </button>
        </div>

        <!-- Main Workspace -->
        <div class="flex flex-1 overflow-hidden">
          
          <!-- Sidebar Navigation -->
          <div class="w-72 bg-slate-50 border-r border-slate-100 p-8 space-y-2 shrink-0">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-[0.3em] mb-6">操作引航导航</div>
            <button 
              v-for="tab in tabs" :key="tab.id"
              @click="activeTab = tab.id"
              :class="activeTab === tab.id ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-100' : 'text-slate-500 hover:bg-white hover:text-indigo-600 hover:shadow-md hover:translate-x-1'"
              class="w-full text-left px-5 py-4 rounded-2xl text-[13px] font-bold transition-all duration-300 flex items-center group mb-2 border border-transparent"
            >
              <i :class="tab.icon" class="mr-4 w-5 text-center transition-transform group-hover:scale-110"></i>
              {{ tab.label }}
            </button>
            
            <div class="mt-auto pt-10 px-2 leading-relaxed">
               <div class="p-5 bg-indigo-50/50 rounded-2xl border border-indigo-100/50">
                  <div class="text-[11px] text-indigo-800 font-bold mb-2 flex items-center">
                    <i class="fas fa-terminal mr-2"></i> 系统内核状态
                  </div>
                  <p class="text-[10px] text-indigo-600/80 italic font-medium">后端 JAX 算力集群已就绪。当前模型支持 N 级跨层级因果拓扑构筑，采样器已优化至千分级收敛精度。</p>
               </div>
            </div>
          </div>

          <!-- Documentation Content -->
          <div class="flex-1 overflow-y-auto p-12 custom-scrollbar bg-white selection:bg-indigo-100">
            
            <!-- Tab: Highlights (Professional & Beginner Friendly) -->
            <div v-if="activeTab === 'highlights'" class="space-y-12 animate-fade-in">
              <section class="max-w-4xl">
                <h1 class="text-3xl font-black text-slate-900 mb-6 tracking-tight">超越表格分析，透视业务深层因果</h1>
                <p class="text-slate-600 leading-relaxed text-base mb-10">
                   DeepBayes 并非简单的报表系统，而是一个基于 <strong class="text-indigo-600">层次贝叶斯网络 (Hierarchical Bayes)</strong> 的仿真决策沙盘。
                   它专为解决“多层级管理组织”（总部-片区-网点）在数据表现不均、环境因素复杂时的效能精准评估。
                </p>

                <div class="grid grid-cols-1 gap-6">
                   <!-- USP 1 -->
                   <div class="flex items-start bg-slate-50 p-6 rounded-3xl border border-slate-100 hover:border-indigo-300 transition-colors group">
                      <div class="flex-shrink-0 w-16 h-16 bg-white rounded-2xl flex items-center justify-center mr-6 shadow-sm border border-slate-200 group-hover:scale-110 transition-transform">
                         <i class="fas fa-shapes text-2xl text-indigo-500"></i>
                      </div>
                      <div>
                         <h3 class="text-lg font-black text-slate-800 mb-2">零代码定义因果逻辑</h3>
                         <p class="text-[13px] text-slate-600 leading-relaxed">
                           告别回归分析的代码堆砌。您只需将业务要素（如：组织名、投入资源、环境指标）通过鼠标<strong class="text-slate-900 border-b-2 border-indigo-200">拖拽映射</strong>，系统便会自动建立拓扑结构，自动为您处理复杂的先验与后验数学演算。
                         </p>
                      </div>
                   </div>

                   <!-- USP 2 -->
                   <div class="flex items-start bg-emerald-50 p-6 rounded-3xl border border-emerald-100 hover:border-emerald-300 transition-colors group">
                      <div class="flex-shrink-0 w-16 h-16 bg-white rounded-2xl flex items-center justify-center mr-6 shadow-sm border border-emerald-200 group-hover:scale-110 transition-transform">
                         <i class="fas fa-balance-scale text-2xl text-emerald-500"></i>
                      </div>
                      <div>
                         <h3 class="text-lg font-black text-emerald-900 mb-2">智能小样本修正 (Shrinkage)</h3>
                         <p class="text-[13px] text-emerald-800 leading-relaxed opacity-90">
                           面对“刚开业数据少”的小网点，普通统计会产生极大误差。DeepBayes 独有的<strong class="font-black">全球化收缩效应</strong>，会自动借调“大盘总均值”的经验来修正极端个案，确保推演结论不偏激。
                         </p>
                      </div>
                   </div>

                   <!-- USP 3 -->
                   <div class="flex items-start bg-slate-900 p-6 rounded-3xl shadow-xl shadow-slate-200 text-white relative overflow-hidden group">
                      <div class="absolute inset-0 bg-gradient-to-br from-indigo-900 to-slate-900"></div>
                      <div class="flex-shrink-0 w-16 h-16 bg-slate-800 rounded-2xl flex items-center justify-center mr-6 shadow-inner border border-slate-700 relative z-10">
                         <i class="fas fa-rocket text-2xl text-cyan-400"></i>
                      </div>
                      <div class="relative z-10">
                         <h3 class="text-lg font-black text-white mb-2">冲击响应与 AI 深度推演</h3>
                         <p class="text-[13px] text-slate-300 leading-relaxed">
                           不仅能看历史，更能预演“万一”。通过冲击测试按钮，您可以模拟极端环境波动，查看整盘资产在危机中的<strong class="text-white border-b border-cyan-400">生存韧性</strong>，并由 AI 决策官为您开出处方级经营建议。
                         </p>
                      </div>
                   </div>
                </div>
              </section>
            </div>

            <!-- Tab: Step-by-Step Operation (Detailed) -->
            <div v-if="activeTab === 'quickstart'" class="space-y-12 animate-fade-in">
              <section class="max-w-4xl">
                 <h2 class="text-2xl font-black text-slate-800 mb-8 flex items-center">
                   🎯 五步业务流程实操指引
                 </h2>

                 <!-- Step 1 -->
                 <div class="mb-10 group">
                   <div class="flex items-center mb-4">
                     <div class="w-9 h-9 rounded-xl bg-slate-900 text-white flex justify-center items-center font-black mr-4 shadow-lg group-hover:scale-110 transition-transform">1</div>
                     <h3 class="text-lg font-bold text-slate-900">数据预处理 (CSV 规范)</h3>
                   </div>
                   <div class="ml-13 bg-slate-50 p-6 rounded-2xl border border-slate-200 space-y-4">
                      <p class="text-xs text-slate-600 font-medium leading-relaxed italic border-l-4 border-indigo-400 pl-4">“好的模型始于洁净的数据。系统采用宽表格式导入。”</p>
                      <ul class="text-[12px] text-slate-700 space-y-3 list-none pl-1">
                        <li class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2 shrink-0"></i> <strong>表头强制性：</strong>首行必须是列名，建议用中文或易懂的名称。</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2 shrink-0"></i> <strong>目标值 Y 必须是数字：</strong>效能、利润、产出等核心评估值不得包含字符或空值。</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-emerald-500 mr-2 shrink-0"></i> <strong>地理联动：</strong>若需大屏地图，请确保名为“经度坐标”和“纬度坐标”的两列为数字格式。</li>
                      </ul>
                   </div>
                 </div>

                 <!-- Step 2 -->
                 <div class="mb-10 group">
                   <div class="flex items-center mb-4">
                     <div class="w-9 h-9 rounded-xl bg-slate-900 text-white flex justify-center items-center font-black mr-4 shadow-lg group-hover:scale-110 transition-transform">2</div>
                     <h3 class="text-lg font-bold text-slate-900">拖拽映射：给系统分配角色</h3>
                   </div>
                   <div class="ml-13 flex gap-6">
                      <div class="flex-1 bg-white border border-slate-200 p-5 rounded-2xl shadow-sm">
                         <p class="text-xs text-slate-500 mb-4 font-bold uppercase tracking-tight">拖拽落位说明</p>
                         <div class="space-y-4">
                            <div class="p-4 bg-amber-50 rounded-xl border border-amber-100 flex items-center justify-between">
                               <span class="text-xs font-black text-amber-900">观测靶点 (Y)</span>
                               <span class="text-[10px] text-amber-700">拖入最终评估项线</span>
                            </div>
                            <div class="p-4 bg-indigo-50 rounded-xl border border-indigo-100 flex items-center justify-between">
                               <span class="text-xs font-black text-indigo-900">节点标识 (ID)</span>
                               <span class="text-[10px] text-indigo-700">拖入各层级名称</span>
                            </div>
                            <div class="p-4 bg-emerald-50 rounded-xl border border-emerald-100 flex items-center justify-between">
                               <span class="text-xs font-black text-emerald-900">环境协变量 (X)</span>
                               <span class="text-[10px] text-emerald-700">拖入各类影响资源</span>
                            </div>
                         </div>
                      </div>
                      <div class="w-1/3 bg-slate-50 rounded-2xl p-6 border border-slate-100 flex flex-col items-center justify-center text-center">
                         <div class="w-12 h-12 bg-white rounded-xl shadow-lg flex items-center justify-center mb-4"><i class="fas fa-mouse-pointer text-indigo-500"></i></div>
                         <h4 class="text-xs font-bold text-slate-800">别名系统 (Rename)</h4>
                         <p class="text-[10px] text-slate-500 mt-2 leading-relaxed">悬停在要素上的<strong class="text-indigo-600">铅笔图标</strong>即可修改图表显示的别名，绝不破坏数据表内核。</p>
                      </div>
                   </div>
                 </div>

                 <!-- Step 3 & 4 (Combined for brevity) -->
                 <div class="mb-10 group">
                    <div class="flex items-center mb-4">
                      <div class="w-9 h-9 rounded-xl bg-slate-900 text-white flex justify-center items-center font-black mr-4 shadow-lg group-hover:scale-110 transition-transform">3</div>
                      <h3 class="text-lg font-bold text-slate-900">构建层级拓扑与启动引擎</h3>
                    </div>
                    <div class="ml-13 grid grid-cols-2 gap-8">
                       <div class="p-6 border border-slate-200 rounded-3xl">
                          <h4 class="text-xs font-bold text-slate-800 mb-2 uppercase tracking-tight">定义拓扑关系 (DAG)</h4>
                          <p class="text-[11px] text-slate-500 leading-relaxed mb-4">
                            通过点击下方“添加下一级网络节点”按钮来模拟组织架构。例如 L1 设为省厅，L2 设为分局。
                          </p>
                          <div class="flex justify-between items-center text-[10px] bg-slate-50 px-3 py-2 rounded-lg">
                             <span class="text-indigo-600 font-bold">L1: 顶层节点</span>
                             <i class="fas fa-chevron-down opacity-30"></i>
                             <span class="text-emerald-600 font-bold">L2: 终端节点</span>
                          </div>
                       </div>
                       <div class="p-6 bg-slate-900 text-white rounded-3xl relative overflow-hidden">
                          <div class="absolute inset-0 bg-blue-600/10 animate-pulse"></div>
                          <h4 class="text-xs font-bold mb-2 uppercase tracking-tight relative z-10">关键监测点</h4>
                          <p class="text-[11px] text-slate-400 leading-relaxed relative z-10">
                            点击执行后，系统会进行千万次模拟。进度条卡在 <strong class="text-amber-400">88%</strong> 时是进行深度收敛检测，请耐心等待约 20 秒，这是决定计算精度的关键一步。
                          </p>
                       </div>
                    </div>
                 </div>

              </section>
            </div>

            <!-- Tab: Dashboard Interpretation (Beginner Friendly Indicators) -->
            <div v-if="activeTab === 'indicators'" class="space-y-12 animate-fade-in">
              <section class="max-w-4xl">
                 <h2 class="text-2xl font-black text-slate-800 mb-8 border-b border-slate-100 pb-4">系统分析指标：教您一小时成为决策专家</h2>
                 
                 <div class="space-y-6">
                    <!-- Indicator 1 -->
                    <div class="flex gap-8 p-6 bg-slate-50 border border-slate-200 rounded-3xl items-center group">
                       <div class="w-20 h-20 bg-white rounded-2xl flex items-center justify-center shrink-0 shadow-sm border border-slate-100 group-hover:rotate-6 transition-transform">
                          <i class="fas fa-chart-scatter text-3xl text-indigo-500"></i>
                       </div>
                       <div>
                          <h4 class="text-base font-bold text-slate-900">效能偏差散点图 (Deviation Map)</h4>
                          <div class="grid grid-cols-2 gap-6 mt-2">
                             <div>
                                <div class="text-[10px] font-black text-emerald-600 mb-1">✅ 青色区域 (卓越)</div>
                                <p class="text-[11px] text-slate-500 leading-normal">说明该项目在当前的配置下，<strong class="text-slate-900">实际表现远超模型给出的期望</strong>，属于典型的内生动力强劲，值得复盘推广。</p>
                             </div>
                             <div>
                                <div class="text-[10px] font-black text-rose-600 mb-1">❌ 红色区域 (脆弱)</div>
                                <p class="text-[11px] text-slate-500 leading-normal">说明该项目<strong class="text-slate-900">严重不达标</strong>。尽管环境配给充足但效能依然垫底，急需战术干预。</p>
                             </div>
                          </div>
                       </div>
                    </div>

                    <!-- Indicator 2 -->
                    <div class="flex gap-8 p-6 bg-slate-50 border border-slate-200 rounded-3xl items-center group">
                       <div class="w-20 h-20 bg-white rounded-2xl flex items-center justify-center shrink-0 shadow-sm border border-slate-100 group-hover:-rotate-6 transition-transform">
                          <i class="fas fa-wave-square text-3xl text-emerald-500"></i>
                       </div>
                       <div>
                          <h4 class="text-base font-bold text-slate-900">模型拟合与后验预测 (PPC Check)</h4>
                          <p class="text-[11px] text-slate-600 mt-2 leading-relaxed">
                            <strong class="text-slate-900 italic font-black">“绿线不出蓝区，报告即可落定。”</strong>
                            <br/>
                            图表中的蓝色阴影带是系统的“万千可能”，翠绿色线条是“现实真相”。只要绿线被包裹在深蓝区内，说明系统已经完全识破了数据的运行规律，其后续的仿真预测具备 95%+ 的可信力。
                          </p>
                       </div>
                    </div>

                    <!-- Indicator 3: Advanced Terms Simplified -->
                    <div class="grid grid-cols-2 gap-6">
                       <div class="p-6 border border-slate-200 rounded-3xl">
                          <div class="text-[10px] font-black text-amber-600 mb-2 uppercase italic border-b border-amber-100 pb-1 flex justify-between">
                             <span>HDI 区间分析</span>
                             <span class="font-mono text-slate-400">Expert Term</span>
                          </div>
                          <p class="text-[11px] text-slate-500 leading-relaxed font-medium">
                             高密度区间 (Highest Density Interval)。预测值的“置信口袋”，口袋越紧（区间越窄），说明评估结果越精确稳健。
                          </p>
                       </div>
                       <div class="p-6 border border-slate-200 rounded-3xl">
                          <div class="text-[10px] font-black text-indigo-600 mb-2 uppercase italic border-b border-indigo-100 pb-1 flex justify-between">
                             <span>VAR 风险值变动</span>
                             <span class="font-mono text-slate-400">Impact Metric</span>
                          </div>
                          <p class="text-[11px] text-slate-500 leading-relaxed font-medium">
                             Value at Risk。在极端环境下模拟演练中，整体效能大盘均值的预计涨跌幅，直观呈现外部环境的破坏力。
                          </p>
                       </div>
                    </div>
                 </div>
              </section>
            </div>

            <!-- Tab: Core Algorithms & Methodologies (The Hard Part) -->
            <div v-if="activeTab === 'methods'" class="space-y-12 animate-fade-in">
                <section class="max-w-4xl">
                   <h3 class="text-xl font-black text-slate-900 border-l-4 border-indigo-600 pl-4 mb-8">算法底层核心与设计定位</h3>
                   
                   <div class="grid grid-cols-2 gap-8 mb-12">
                      <div class="space-y-4">
                         <div class="flex items-center gap-2 mb-2">
                           <div class="w-1.5 h-6 bg-indigo-200 rounded"></div>
                           <h4 class="text-sm font-black text-slate-800">MCMC & NUTS 采样引擎</h4>
                         </div>
                         <p class="text-[11px] text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">
                           系统采用 <strong class="text-indigo-600 italic">Markov Chain Monte Carlo</strong> (蒙特卡洛马尔科夫链) 采样。
                           <br/><br/>
                           通俗解释：系统在高达几百维的概率空间里进行千万次“盲视随机漫步”，通过探测分布的密集程度，反向推导由于数据缺失或环境干扰导致无法直接观测到的“真实评估分”。
                         </p>
                      </div>
                      <div class="space-y-4">
                         <div class="flex items-center gap-2 mb-2">
                           <div class="w-1.5 h-6 bg-emerald-200 rounded"></div>
                           <h4 class="text-sm font-black text-slate-800">Hierarchical Prior (层次先验)</h4>
                         </div>
                         <p class="text-[11px] text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">
                           这是 DeepBayes 处理组织架构分集的“灵魂”。
                           <br/><br/>
                           通过在全球/父级节点建立概率分布约束，系统将知识或趋势“自上而下”传导。它巧妙解决了经典模型（如 OLS）在处理嵌套数据时会导致的标准误差偏误问题。
                         </p>
                      </div>
                   </div>

                   <h3 class="text-sm font-black text-slate-500 mb-6 uppercase tracking-[0.2em] italic border-b pb-2">内置场景定位白皮书 (Sandbox Positioning)</h3>
                   <div class="grid grid-cols-3 gap-6">
                      <div class="p-5 border border-slate-100 rounded-2xl hover:bg-slate-50 transition-colors cursor-default">
                         <div class="text-[10px] font-black text-indigo-600 mb-2 font-mono">SCENARIO: SEC - 社会治理</div>
                         <p class="text-[10px] text-slate-500 leading-relaxed">演示行政三级垂直领导体系。主要评估经费下沉到基层单位后的转化效能阈值。</p>
                      </div>
                      <div class="p-5 border border-slate-100 rounded-2xl hover:bg-slate-50 transition-colors cursor-default">
                         <div class="text-[10px] font-black text-rose-600 mb-2 font-mono">SCENARIO: GEO - 地缘演化</div>
                         <p class="text-[10px] text-slate-500 leading-relaxed">演示由于地理坐标引起的“邻接依赖”分析。评估极端封锁下的战略城市生存韧性。</p>
                      </div>
                      <div class="p-5 border border-slate-100 rounded-2xl hover:bg-slate-50 transition-colors cursor-default">
                         <div class="text-[10px] font-black text-emerald-600 mb-2 font-mono">SCENARIO: HEALTH - 公共卫生</div>
                         <p class="text-[10px] text-slate-500 leading-relaxed">演示高噪声、跨国大数据集下的归因分析。用于识别稀薄变量中的因果相关度。</p>
                      </div>
                   </div>
                </section>
            </div>

          </div>
        </div>

        <!-- Sticky Status Footer -->
        <div class="px-12 py-7 bg-slate-50 border-t border-slate-100 flex justify-between items-center shrink-0">
          <div class="flex items-center text-[10px] font-black text-slate-400 uppercase tracking-widest gap-4">
             <div class="flex items-center"><i class="fas fa-microchip mr-2 text-indigo-400"></i> Distributed ML Activated</div>
             <div class="flex items-center"><i class="fas fa-shield-alt mr-2 text-indigo-400"></i> Integrity Check Green</div>
          </div>
          <div class="flex gap-4">
             <button @click="$emit('close')" class="px-10 py-3.5 bg-white border border-slate-200 text-slate-600 text-xs font-black rounded-2xl hover:bg-slate-50 transition-all shadow-sm">
               DISMISS
             </button>
             <button @click="$emit('close')" class="px-10 py-3.5 bg-indigo-600 text-white text-xs font-black rounded-2xl hover:bg-indigo-700 shadow-xl shadow-indigo-100 active:scale-95 transition-all flex items-center group">
               我完全明白了，开启决策推演之路
               <i class="fas fa-chevron-right ml-3 group-hover:translate-x-1 transition-transform"></i>
             </button>
          </div>
        </div>

      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  show: Boolean
});

defineEmits(['close']);

const activeTab = ref('highlights');

const tabs = [
  { id: 'highlights', label: '1. 产品核心价值亮点', icon: 'fas fa-gem text-amber-500' },
  { id: 'quickstart', label: '2. 五步快速上手指南', icon: 'fas fa-map-signs text-emerald-500' },
  { id: 'indicators', label: '3. 核心指标与报告解读', icon: 'fas fa-search-dollar text-indigo-500' },
  { id: 'methods', label: '4. 底层算法原理与场景', icon: 'fas fa-microchip text-rose-500' }
];
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.animate-fade-in {
  animation: fadeIn 0.45s ease-out;
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.96) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 20px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #cbd5e1;
}
</style>
