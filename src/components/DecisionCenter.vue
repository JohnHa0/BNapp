<template>
  <div class="flex-1 min-h-0 bg-ice-white p-6 flex flex-col font-sans overflow-hidden">
    
    <!-- 页面工具栏 -->
    <div class="mb-5 bg-[#0b1121] rounded-2xl shadow-xl shadow-black/10 border border-white/5 text-white shrink-0 relative overflow-hidden">
      <div class="absolute inset-0 opacity-[0.02]" style="background-image: radial-gradient(circle at 1px 1px, rgba(245,158,11,0.8) 1px, transparent 0); background-size: 20px 20px;"></div>
      <div class="flex justify-between items-center px-6 py-4 relative z-10">
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-xl bg-amber-500/20 flex items-center justify-center ring-1 ring-amber-500/30">
            <i class="fas fa-brain text-amber-300 text-xl"></i>
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight flex items-center gap-2.5">
              决策研判中心
              <span v-if="isLiveMode" class="text-[11px] bg-amber-500/20 text-amber-300 px-2.5 py-0.5 rounded-full font-bold border border-amber-500/30">实时推演</span>
            </h1>
            <p class="text-[11px] text-slate-500 mt-0.5">{{ isLiveMode ? '参数调整后的模拟结果' : '量化发现辅助判断优先级和发力方向' }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2.5">
          <button @click="generateFullReport" class="h-9 px-4 text-[13px] font-bold rounded-xl transition-colors flex items-center gap-2 shadow-lg"
                  :class="isLiveMode ? 'bg-amber-500 hover:bg-amber-400 shadow-amber-500/20' : 'bg-emerald-500 hover:bg-emerald-400 shadow-emerald-500/20'"
                  :disabled="isGeneratingReport">
            <i class="fas" :class="isGeneratingReport ? 'fa-spinner fa-spin' : 'fa-file-alt'"></i>
            {{ isGeneratingReport ? '生成中' : '生成简报' }}
          </button>
          <button @click="copyDecisionSummary" class="h-9 px-4 text-[12px] font-medium text-slate-300 bg-white/5 hover:bg-white/10 rounded-xl transition-colors flex items-center gap-2 border border-white/5">
            <i class="fas fa-copy"></i>复制摘要
          </button>
          <button @click="$emit('back')" class="h-9 px-4 text-[12px] font-medium text-slate-400 bg-white/5 hover:bg-white/10 rounded-xl transition-colors flex items-center gap-2">
            <i class="fas fa-arrow-left"></i>返回
          </button>
        </div>
      </div>
    </div>

    <!-- 主网格 -->
    <div class="flex-1 grid grid-cols-12 grid-rows-3 gap-5 min-h-0 overflow-y-auto custom-scrollbar pr-1">

      <!-- 左上：研判总评 -->
      <div class="col-span-5 row-span-1 bg-white rounded-2xl border border-slate-200 shadow-md p-5 flex flex-col">
        <h2 class="text-sm font-bold text-slate-700 mb-3 flex items-center">
          <i class="fas fa-clipboard-check text-indigo-500 mr-2"></i> 研判总评
        </h2>
        <div class="flex-1 space-y-3 text-sm leading-relaxed">
          <p class="text-slate-600">
            本次覆盖 <span class="bg-indigo-50 text-indigo-700 px-1.5 py-0.5 rounded font-bold">{{ summary.totalNodes }}</span> 个评估对象，
            在 <span class="bg-indigo-50 text-indigo-700 px-1.5 py-0.5 rounded font-bold">{{ summary.totalLevels }}</span> 层组织关系下考察。
          </p>
          <p class="text-slate-600">
            <template v-if="isLiveMode">
              <span class="text-amber-600 font-bold">当前为推演模拟状态</span>，数据已按参数调整后的条件重新计算。
            </template>
            <template v-else>
              模型对业务规律的拟合处于健康区间，分析结论可信。
            </template>
          </p>
          <div class="grid grid-cols-3 gap-3 mt-2">
            <div class="bg-emerald-50 rounded-xl p-3 border border-emerald-100 text-center">
              <div class="text-2xl font-black text-emerald-600">{{ summary.brightCount }}</div>
              <div class="text-[10px] text-emerald-700 font-bold">表现突出</div>
              <div class="text-[9px] text-emerald-600/70">超出预期</div>
            </div>
            <div class="bg-amber-50 rounded-xl p-3 border border-amber-100 text-center">
              <div class="text-2xl font-black text-amber-600">{{ summary.neutralCount }}</div>
              <div class="text-[10px] text-amber-700 font-bold">运行正常</div>
              <div class="text-[9px] text-amber-600/70">符合预期</div>
            </div>
            <div class="bg-rose-50 rounded-xl p-3 border border-rose-100 text-center">
              <div class="text-2xl font-black text-rose-600">{{ summary.darkCount }}</div>
              <div class="text-[10px] text-rose-700 font-bold">需要关注</div>
              <div class="text-[9px] text-rose-600/70">低于预期</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右上：关键驱动力 -->
      <div class="col-span-7 row-span-1 bg-white rounded-2xl border border-slate-200 shadow-md p-5 flex flex-col">
        <h2 class="text-sm font-bold text-slate-700 mb-3 flex items-center">
          <i class="fas fa-shield-alt text-blue-500 mr-2"></i> 关键驱动力
        </h2>
        <div class="flex-1 flex gap-4">
          <div class="w-1/3 flex flex-col items-center justify-center bg-slate-50 rounded-xl p-4 border border-slate-100">
            <div class="relative w-24 h-24">
              <svg class="w-24 h-24 transform -rotate-90" viewBox="0 0 96 96">
                <circle cx="48" cy="48" r="40" fill="none" stroke="#e2e8f0" stroke-width="8"/>
                <circle cx="48" cy="48" r="40" fill="none" :stroke="confidenceColor" stroke-width="8"
                  :stroke-dasharray="2 * Math.PI * 40"
                  :stroke-dashoffset="2 * Math.PI * 40 * (1 - confidenceScore / 100)"
                  stroke-linecap="round"/>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-2xl font-black" :class="confidenceTextColor">{{ confidenceScore }}%</span>
                <span class="text-[9px] text-slate-400 font-bold">可信度</span>
              </div>
            </div>
            <p class="text-[10px] text-slate-500 text-center mt-2 leading-relaxed">综合数据量与模型收敛性评估</p>
          </div>
          <div class="flex-1 space-y-2 overflow-y-auto custom-scrollbar">
            <p class="text-[11px] font-bold text-slate-600 mb-2">按影响力排序的驱动因子</p>
            <div v-for="(factor, idx) in topDrivers" :key="idx" 
                 class="flex items-center justify-between px-3 py-2 rounded-lg border text-xs"
                 :class="factor.beta > 0 ? 'bg-emerald-50 border-emerald-100' : 'bg-rose-50 border-rose-100'">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-black"
                  :class="idx === 0 ? 'bg-indigo-500 text-white' : idx === 1 ? 'bg-indigo-300 text-white' : 'bg-slate-200 text-slate-500'">#{{ idx + 1 }}</span>
                <span class="font-bold text-slate-700">{{ factor.name }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="font-mono font-bold" :class="factor.beta > 0 ? 'text-emerald-600' : 'text-rose-600'">
                  {{ factor.beta > 0 ? '+' : '' }}{{ factor.beta.toFixed(4) }}
                </span>
                <span class="text-[10px] px-1.5 py-0.5 rounded-full font-bold"
                  :class="factor.impact === 'high' ? 'bg-indigo-100 text-indigo-700' : factor.impact === 'medium' ? 'bg-slate-100 text-slate-600' : 'bg-slate-50 text-slate-400'">
                  {{ factor.impact === 'high' ? '高影响' : factor.impact === 'medium' ? '中影响' : '低影响' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中左：优先级排序（含建议） -->
      <div class="col-span-6 row-span-1 bg-white rounded-2xl border border-slate-200 shadow-md p-5 flex flex-col">
        <h2 class="text-sm font-bold text-slate-700 mb-3 flex items-center">
          <i class="fas fa-sort-amount-down text-amber-500 mr-2"></i> 关注优先级
        </h2>
        <div class="flex-1 overflow-y-auto custom-scrollbar space-y-2">
          <div v-for="(item, idx) in priorityRanked.slice(0, 8)" :key="idx"
               class="flex items-center space-x-3 p-2.5 rounded-lg border transition-colors hover:shadow-sm"
               :class="item.priority === 'critical' ? 'bg-rose-50 border-rose-200' : 
                        item.priority === 'high' ? 'bg-amber-50 border-amber-200' : 
                        item.priority === 'positive' ? 'bg-emerald-50 border-emerald-200' :
                        'bg-slate-50 border-slate-100'">
            <div class="shrink-0 w-9 h-9 rounded-full flex items-center justify-center text-xs font-black"
                 :class="item.priority === 'critical' ? 'bg-rose-500 text-white' :
                          item.priority === 'high' ? 'bg-amber-500 text-white' :
                          item.priority === 'positive' ? 'bg-emerald-500 text-white' :
                          'bg-slate-300 text-white'">
              {{ idx + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-slate-800 truncate">{{ item.name }}</div>
              <div class="text-[10px] text-slate-500 truncate">{{ item.advice }}</div>
            </div>
            <div class="shrink-0 text-right min-w-[72px]">
              <div class="text-xs font-mono font-bold" :class="item.Deviation > 0 ? 'text-emerald-600' : 'text-rose-600'">
                {{ item.Deviation > 0 ? '+' : '' }}{{ Math.abs(item.Deviation).toFixed(2) }}σ
              </div>
              <div class="text-[8px] leading-tight mt-0.5" :class="item.priority === 'critical' ? 'text-rose-500' : item.priority === 'high' ? 'text-amber-500' : item.priority === 'positive' ? 'text-emerald-500' : 'text-slate-400'">
                {{ item.devDesc }}
              </div>
              <div class="text-[9px] px-1.5 py-0.5 rounded-full font-bold mt-1"
                   :class="item.priority === 'critical' ? 'bg-rose-100 text-rose-700' :
                            item.priority === 'high' ? 'bg-amber-100 text-amber-700' :
                            item.priority === 'positive' ? 'bg-emerald-100 text-emerald-700' :
                            'bg-slate-100 text-slate-500'">
                {{ item.priority === 'critical' ? '紧急' : item.priority === 'high' ? '关注' : item.priority === 'positive' ? '标杆' : '正常' }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中右：行动建议 -->
      <div class="col-span-6 row-span-1 bg-white rounded-2xl border border-slate-200 shadow-md p-5 flex flex-col">
        <h2 class="text-sm font-bold text-slate-700 mb-3 flex items-center">
          <i class="fas fa-lightbulb text-amber-400 mr-2"></i> 行动建议
        </h2>
        <div class="flex-1 overflow-y-auto custom-scrollbar space-y-3">
          <div v-for="(rec, idx) in recommendations" :key="idx"
               class="p-3 rounded-xl border transition-colors"
               :class="rec.type === 'urgent' ? 'bg-rose-50/50 border-rose-200' :
                        rec.type === 'strategic' ? 'bg-indigo-50/50 border-indigo-200' :
                        'bg-emerald-50/50 border-emerald-200'">
            <div class="flex items-start space-x-2">
              <div class="shrink-0 mt-0.5">
                <i class="fas text-xs"
                   :class="rec.type === 'urgent' ? 'fa-exclamation-circle text-rose-500' :
                            rec.type === 'strategic' ? 'fa-chess text-indigo-500' :
                            'fa-star text-emerald-500'">
                </i>
              </div>
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-1">
                  <span class="text-[10px] font-black px-1.5 py-0.5 rounded"
                        :class="rec.type === 'urgent' ? 'bg-rose-100 text-rose-700' :
                                 rec.type === 'strategic' ? 'bg-indigo-100 text-indigo-700' :
                                 'bg-emerald-100 text-emerald-700'">
                    {{ rec.type === 'urgent' ? '立即处置' : rec.type === 'strategic' ? '战略调整' : '经验推广' }}
                  </span>
                  <span class="text-[10px] text-slate-400">{{ rec.scope }}</span>
                </div>
                <p class="text-xs text-slate-700 leading-relaxed">{{ rec.content }}</p>
                <p v-if="rec.expectedImpact" class="text-[10px] text-slate-500 mt-1.5 flex items-center">
                  <i class="fas fa-chart-line mr-1 text-slate-400"></i>
                  预期效果: {{ rec.expectedImpact }}
                </p>
              </div>
            </div>
          </div>
          <div v-if="recommendations.length === 0" class="flex-1 flex items-center justify-center text-slate-400 text-xs">
            完成分析后将自动生成针对性建议
          </div>
        </div>
      </div>

      <!-- 底部：风险矩阵（增强版） -->
      <div class="col-span-12 row-span-1 bg-white rounded-2xl border border-slate-200 shadow-md p-5 flex flex-col">
        <h2 class="text-sm font-bold text-slate-700 mb-1 flex items-center">
          <i class="fas fa-th text-rose-400 mr-2"></i> 风险分布
        </h2>
        <p class="text-[10px] text-slate-500 mb-3">
          {{ riskMatrix.highRiskTotal }} 个对象处于高风险区（占 {{ riskMatrix.highRiskPct }}%）
          <template v-if="riskMatrix.cells.high_high.count > 0">
            ，其中最严重的是 <span class="text-rose-600 font-bold">{{ riskMatrix.cells.high_high.nodes.slice(0, 3).join('、') }}</span>{{ riskMatrix.cells.high_high.nodes.length > 3 ? ' 等' : '' }}
          </template>
        </p>
        <div class="flex-1 flex gap-4 min-h-0">
          <!-- 矩阵网格 -->
          <div class="w-[55%] flex flex-col">
            <div class="grid grid-cols-4 gap-1.5 flex-1 text-center">
              <div class="text-[9px] font-bold text-slate-400"></div>
              <div class="text-[9px] font-bold text-slate-400 self-end pb-1">偏差小</div>
              <div class="text-[9px] font-bold text-slate-400 self-end pb-1">偏差中</div>
              <div class="text-[9px] font-bold text-slate-400 self-end pb-1">偏差大</div>
              <div class="text-[9px] font-bold text-slate-400 self-center pr-1 text-right">波动大</div>
              <div class="relative bg-rose-200 border border-rose-300 rounded-lg p-1.5 group/cell cursor-default" v-if="riskMatrix.cells.high_high.count > 0">
                <div class="text-xs font-black text-rose-700">{{ riskMatrix.cells.high_high.count }}</div>
                <div class="text-[8px] text-rose-600/70">{{ (riskMatrix.cells.high_high.count / riskMatrix.total * 100).toFixed(0) }}%</div>
                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 w-48 bg-slate-800 text-white text-[10px] p-2 rounded-lg opacity-0 group-hover/cell:opacity-100 transition-opacity pointer-events-none z-50 text-left">
                  <div class="font-bold text-rose-300 mb-1">高偏离 + 大影响</div>
                  <div class="text-slate-300">{{ riskMatrix.cells.high_high.nodes.join('、') }}</div>
                </div>
              </div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="relative bg-orange-100 border border-orange-200 rounded-lg p-1.5 group/cell cursor-default" v-if="riskMatrix.cells.high_mid.count > 0">
                <div class="text-xs font-black text-orange-700">{{ riskMatrix.cells.high_mid.count }}</div>
                <div class="text-[8px] text-orange-600/70">{{ (riskMatrix.cells.high_mid.count / riskMatrix.total * 100).toFixed(0) }}%</div>
                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 w-48 bg-slate-800 text-white text-[10px] p-2 rounded-lg opacity-0 group-hover/cell:opacity-100 transition-opacity pointer-events-none z-50 text-left">
                  <div class="font-bold text-orange-300 mb-1">高偏离 + 中影响</div>
                  <div class="text-slate-300">{{ riskMatrix.cells.high_mid.nodes.join('、') }}</div>
                </div>
              </div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="relative bg-amber-100 border border-amber-200 rounded-lg p-1.5 group/cell cursor-default" v-if="riskMatrix.cells.high_low.count > 0">
                <div class="text-xs font-black text-amber-700">{{ riskMatrix.cells.high_low.count }}</div>
                <div class="text-[8px] text-amber-600/70">{{ (riskMatrix.cells.high_low.count / riskMatrix.total * 100).toFixed(0) }}%</div>
              </div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="text-[9px] font-bold text-slate-400 self-center pr-1 text-right">波动中</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-400" v-if="riskMatrix.cells.mid_high.count > 0">{{ riskMatrix.cells.mid_high.count }}</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-400" v-if="riskMatrix.cells.mid_mid.count > 0">{{ riskMatrix.cells.mid_mid.count }}</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-400" v-if="riskMatrix.cells.mid_low.count > 0">{{ riskMatrix.cells.mid_low.count }}</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="text-[9px] font-bold text-slate-400 self-center pr-1 text-right">波动小</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-400" v-if="riskMatrix.cells.low_high.count > 0">{{ riskMatrix.cells.low_high.count }}</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-400" v-if="riskMatrix.cells.low_mid.count > 0">{{ riskMatrix.cells.low_mid.count }}</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-400" v-if="riskMatrix.cells.low_low.count > 0">{{ riskMatrix.cells.low_low.count }}</div>
              <div class="bg-slate-100 border border-slate-200 rounded-lg p-1.5 text-[9px] text-slate-300" v-else>0</div>
            </div>
            <div class="flex text-[9px] text-slate-400 mt-1 px-1">
              <span class="flex-1">← 偏差幅度 →</span>
              <span>↑ 不确定性</span>
            </div>
          </div>
          <!-- 右侧：高风险区详情列表 -->
          <div class="w-[45%] overflow-y-auto custom-scrollbar text-xs space-y-2 pr-1">
            <div class="font-bold text-slate-600 text-[11px] mb-1">高风险对象明细</div>
            <template v-for="cellKey in ['high_high', 'high_mid', 'high_low']" :key="cellKey">
              <div v-if="riskMatrix.cells[cellKey].count > 0" class="p-2 rounded-lg border"
                   :class="cellKey === 'high_high' ? 'bg-rose-50 border-rose-200' : cellKey === 'high_mid' ? 'bg-orange-50 border-orange-200' : 'bg-amber-50 border-amber-200'">
                <div class="text-[10px] font-bold mb-1"
                     :class="cellKey === 'high_high' ? 'text-rose-700' : cellKey === 'high_mid' ? 'text-orange-700' : 'text-amber-700'">
                  {{ riskMatrix.cells[cellKey].label }}（{{ riskMatrix.cells[cellKey].count }}个）
                </div>
                <div class="flex flex-wrap gap-1">
                  <span v-for="name in riskMatrix.cells[cellKey].nodes" :key="name"
                        class="px-1.5 py-0.5 rounded text-[9px] font-medium"
                        :class="cellKey === 'high_high' ? 'bg-white text-rose-700' : cellKey === 'high_mid' ? 'bg-white text-orange-700' : 'bg-white text-amber-700'">
                    {{ name }}
                  </span>
                </div>
              </div>
            </template>
            <div v-if="riskMatrix.highRiskTotal === 0" class="text-slate-400 py-4 text-center">
              <i class="fas fa-check-circle text-emerald-400 mr-1"></i>暂无高风险对象
            </div>
            <!-- 风险类型优先级排序 -->
            <div v-if="riskMatrix.riskPriority && riskMatrix.riskPriority.length > 0" class="mt-3 pt-3 border-t border-slate-100">
              <div class="text-[10px] font-bold text-slate-500 mb-2">处置优先级排序</div>
              <div v-for="(rp, i) in riskMatrix.riskPriority" :key="rp.key" class="flex items-center text-[10px] py-1">
                <span class="w-5 h-5 rounded-full flex items-center justify-center text-[9px] font-black mr-2"
                      :class="i === 0 ? 'bg-rose-500 text-white' : i === 1 ? 'bg-orange-500 text-white' : 'bg-slate-300 text-white'">
                  {{ i + 1 }}
                </span>
                <span class="font-bold text-slate-700 mr-2">{{ rp.label }}</span>
                <span class="text-slate-500 mr-auto">{{ riskMatrix.cells[rp.key].count }}个对象</span>
                <span class="px-1.5 py-0.5 rounded-full text-[8px] font-bold"
                      :class="rp.urgency === '最紧急' ? 'bg-rose-100 text-rose-700' : rp.urgency === '非常紧急' ? 'bg-orange-100 text-orange-700' : rp.urgency === '紧急' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-600'">
                  {{ rp.urgency }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 简报弹窗 -->
    <transition name="fade">
      <div v-if="showReportModal" class="fixed inset-0 bg-deep-blue/60 backdrop-blur-sm flex justify-center items-center z-[70] overflow-y-auto py-8" @click.self="showReportModal = false">
        <div class="bg-white p-6 rounded-2xl shadow-2xl w-[800px] max-h-[90vh] flex flex-col border border-slate-200">
          <div class="flex justify-between items-center mb-4 shrink-0">
            <h3 class="font-bold text-lg text-slate-800 flex items-center">
              <i class="fas fa-file-pdf text-rose-500 mr-2"></i>决策研判简报
              <span v-if="isLiveMode" class="ml-3 text-[10px] bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-bold flex items-center">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse mr-1.5"></span>实时刷新中
              </span>
            </h3>
            <div class="flex space-x-2">
              <button @click="exportPDF" :disabled="isPdfExporting" class="px-3 py-1.5 text-xs font-bold text-white bg-rose-600 rounded-lg hover:bg-rose-700 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed">
                <i class="fas" :class="isPdfExporting ? 'fa-spinner fa-spin' : 'fa-file-pdf'"></i>
                <span class="ml-1.5">{{ isPdfExporting ? '导出中' : '导出 PDF' }}</span>
              </button>
              <button @click="exportHTML" :disabled="isHtmlExporting" class="px-3 py-1.5 text-xs font-bold text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed">
                <i class="fas" :class="isHtmlExporting ? 'fa-spinner fa-spin' : 'fa-file-code'"></i>
                <span class="ml-1.5">{{ isHtmlExporting ? '导出中' : '导出 HTML' }}</span>
              </button>
              <div class="w-px h-6 bg-slate-200 self-center"></div>
              <button @click="printReport" class="px-3 py-1.5 text-xs font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors flex items-center">
                <i class="fas fa-print mr-1.5"></i>打印
              </button>
              <button @click="copyReport" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors flex items-center">
                <i class="fas fa-copy mr-1.5"></i>复制
              </button>
              <button @click="showReportModal = false" class="px-3 py-1.5 text-xs font-medium text-slate-500 bg-white border border-slate-200 rounded-lg hover:bg-slate-100 transition-colors flex items-center">
                <i class="fas fa-times mr-1"></i>关闭
              </button>
            </div>
          </div>
          <div ref="reportContentRef" class="flex-1 overflow-y-auto custom-scrollbar text-sm leading-relaxed space-y-4 pr-2" v-html="reportHTML"></div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelResults: { type: Object, required: true },
  livePerformanceData: { type: Array, default: null },
  liveCovariates: { type: Array, default: null },
  hierarchySchema: { type: Array, required: true },
  displayMapping: { type: Object, default: () => ({}) },
  rawTableData: { type: Array, default: () => [] },
  targetVariable: { type: Object, default: () => ({}) }
});

defineEmits(['back']);

const showReportModal = ref(false);
const reportContentRef = ref(null);
const isGeneratingReport = ref(false);
const isPdfExporting = ref(false);
const isHtmlExporting = ref(false);
const reportHTML = ref('');

// 是否处于实时推演模式
const isLiveMode = computed(() => {
  return props.livePerformanceData !== null && props.livePerformanceData !== undefined;
});

// 当前使用的性能数据：推演模式用实时数据，否则用原始结果
const performanceData = computed(() => {
  if (isLiveMode.value && props.livePerformanceData) {
    return props.livePerformanceData;
  }
  return props.modelResults?.performance_data || [];
});

// ── 研判总评 ──
const summary = computed(() => {
  const data = performanceData.value;
  const bright = data.filter(d => d.Status === 'Bright Spot' || d.Status === 'Bright').length;
  const dark = data.filter(d => d.Status === 'Dark Spot' || d.Status === 'Dark').length;
  const neutral = data.length - bright - dark;
  return {
    totalNodes: data.length,
    totalLevels: props.hierarchySchema?.length || 0,
    brightCount: bright,
    darkCount: dark,
    neutralCount: neutral,
  };
});

// ── 关键驱动力 ──
const topDrivers = computed(() => {
  const betas = props.modelResults?.betas || {};
  const entries = Object.entries(betas).map(([k, v]) => {
    const absV = Math.abs(v);
    return {
      name: props.displayMapping[k] || k,
      beta: v,
      absBeta: absV,
      impact: absV > 0.1 ? 'high' : absV > 0.03 ? 'medium' : 'low'
    };
  });
  return entries.sort((a, b) => b.absBeta - a.absBeta).slice(0, 5);
});

const computeThreshold = (data) => {
  if (!data || data.length === 0) return 1.0;
  const deviations = data.map(d => d.Deviation);
  const mean = deviations.reduce((a, b) => a + b, 0) / deviations.length;
  const variance = deviations.reduce((a, b) => a + (b - mean) ** 2, 0) / deviations.length;
  const sd = Math.sqrt(variance);
  return sd > 0.01 ? sd : 0.1;
};

// ── 优先级排序（含具体建议） ──
const priorityRanked = computed(() => {
  const data = performanceData.value;
  const threshold = computeThreshold(data);
  const drivers = topDrivers.value;
  const topDriverName = drivers.length > 0 ? drivers[0].name : '';
  
  return data
    .map(d => {
      const name = props.displayMapping[d.NodeName] || d.NodeName;
      const dev = d.Deviation;
      
      let priority, advice;
      if (dev < -2 * threshold) {
        priority = 'critical';
        advice = topDriverName 
          ? `严重偏离预期，建议优先核查「${topDriverName}」相关投入是否不足`
          : '严重偏离预期，建议启动专项排查';
      } else if (dev < -threshold) {
        priority = 'high';
        advice = topDriverName
          ? `略低于预期，可考虑在「${topDriverName}」方面适当增加资源`
          : '略低于预期，纳入重点观察名单';
      } else if (dev > 2 * threshold) {
        priority = 'positive';
        advice = '表现显著超出预期，建议调研其做法并在同类对象中推广';
      } else if (dev > threshold) {
        priority = 'positive';
        advice = '表现良好，可维持现有策略并关注其经验';
      } else {
        priority = 'neutral';
        advice = '运行正常，无需特别干预';
      }
      
      const desc = describeDeviation(dev, threshold);
      return { ...d, name, priority, advice, devDesc: desc };
    })
    .sort((a, b) => {
      const order = { critical: 0, high: 1, neutral: 2, positive: 3 };
      if (order[a.priority] !== order[b.priority]) return order[a.priority] - order[b.priority];
      return Math.abs(b.Deviation) - Math.abs(a.Deviation);
    });
});

// ── 行动建议 ──
const recommendations = computed(() => {
  const recs = [];
  const data = performanceData.value;
  const drivers = topDrivers.value;
  const summ = summary.value;
  
  if (summ.darkCount > 0) {
    const darkNodes = data.filter(d => d.Status === 'Dark Spot' || d.Status === 'Dark');
    const worstNodes = darkNodes.sort((a, b) => a.Deviation - b.Deviation).slice(0, 3);
    const names = worstNodes.map(n => props.displayMapping[n.NodeName] || n.NodeName).join('、');
    
    recs.push({
      type: 'urgent',
      scope: `${summ.darkCount} 个对象需要关注`,
      content: `${summ.darkCount} 个对象的实际表现低于系统根据客观条件测算的应有水平。其中最突出的 ${names} 需要优先排查——是资源配置不足、管理方法不当，还是存在数据之外的特殊情况。`,
      expectedImpact: `如果将这些对象提升到预期水平，整体表现可提升约 ${Math.round(summ.darkCount / data.length * 60)}%`
    });
  }
  
  if (drivers.length > 0) {
    const top = drivers[0];
    const direction = top.beta > 0 ? '正面推动' : '负面拖累';
    recs.push({
      type: 'strategic',
      scope: `核心杠杆：${top.name}`,
      content: `在所有影响因素中，「${top.name}」对最终结果的影响力最大，属于${direction}因素。这意味着：把资源优先投到这个方向上，性价比最高。${top.beta > 0 ? '提升该指标会直接拉高整体表现。' : '该指标过高时反而会拉低表现，需要找准平衡点。'}`,
      expectedImpact: `该指标每改善一个单位，预期可带来约 ${Math.abs(top.beta).toFixed(3)} 的效能提升`
    });
  }
  
  if (summ.brightCount > 0 && !isLiveMode.value) {
    recs.push({
      type: 'positive',
      scope: `${summ.brightCount} 个表现突出的对象`,
      content: `有 ${summ.brightCount} 个对象在同样条件下取得了超出预期的成绩。建议深入了解它们的具体做法——是人员配置更合理、流程更高效，还是采取了独特的创新举措——然后把这些做法整理成可复制的工作规范。`,
      expectedImpact: '如果成功经验能在 30% 的同类对象中推广，整体表现预期提升 5-10%'
    });
  }
  
  if (recs.length === 0) {
    recs.push({
      type: 'strategic',
      scope: '整体评估',
      content: '当前各评估对象的表现均在正常波动范围内，系统运行平稳。建议保持现有监测节奏，同时留意外部环境变化可能带来的整体性偏移。'
    });
  }
  
  return recs;
});

// ── 风险矩阵（含节点详情）──
const riskMatrix = computed(() => {
  const data = performanceData.value;
  const threshold = computeThreshold(data);
  const total = data.length || 1;
  
  const cells = {
    high_high: { count: 0, nodes: [], label: '高偏离+大影响' },
    high_mid:  { count: 0, nodes: [], label: '高偏离+中影响' },
    high_low:  { count: 0, nodes: [], label: '高偏离+小影响' },
    mid_high:  { count: 0, nodes: [], label: '中偏离+大影响' },
    mid_mid:   { count: 0, nodes: [], label: '中偏离+中影响' },
    mid_low:   { count: 0, nodes: [], label: '中偏离+小影响' },
    low_high:  { count: 0, nodes: [], label: '低偏离+大影响' },
    low_mid:   { count: 0, nodes: [], label: '低偏离+小影响' },
    low_low:   { count: 0, nodes: [], label: '低偏离+极小影响' },
  };
  
  data.forEach(d => {
    const absDev = Math.abs(d.Deviation);
    const isHighProb = absDev > 2.5 * threshold;
    const isMidProb = absDev > 1.5 * threshold && absDev <= 2.5 * threshold;
    const impact = Math.abs(d.Actual - d.Expected);
    const maxImpact = Math.max(...data.map(x => Math.abs(x.Actual - x.Expected))) || 1;
    const impactRatio = impact / maxImpact;
    const name = props.displayMapping[d.NodeName] || d.NodeName;
    
    let cell;
    if (isHighProb && impactRatio > 0.66) cell = 'high_high';
    else if (isHighProb && impactRatio > 0.33) cell = 'high_mid';
    else if (isHighProb) cell = 'high_low';
    else if (isMidProb && impactRatio > 0.66) cell = 'mid_high';
    else if (isMidProb && impactRatio > 0.33) cell = 'mid_mid';
    else if (isMidProb) cell = 'mid_low';
    else if (impactRatio > 0.66) cell = 'low_high';
    else if (impactRatio > 0.33) cell = 'low_mid';
    else cell = 'low_low';
    
    cells[cell].count++;
    cells[cell].nodes.push(name);
  });
  
  // 附加上下文
  const highRiskTotal = cells.high_high.count + cells.high_mid.count + cells.high_low.count;
  const highRiskPct = ((highRiskTotal / total) * 100).toFixed(1);
  
  // 风险类型按紧急程度排序
  const riskPriority = [
    { key: 'high_high', label: '偏离大+影响大', urgency: '最紧急', color: 'rose' },
    { key: 'high_mid', label: '偏离大+影响中', urgency: '非常紧急', color: 'orange' },
    { key: 'high_low', label: '偏离大+影响小', urgency: '紧急', color: 'amber' },
    { key: 'mid_high', label: '偏离中+影响大', urgency: '重点关注', color: 'yellow' },
    { key: 'mid_mid', label: '偏离中+影响中', urgency: '常规关注', color: 'slate' },
  ].filter(p => cells[p.key].count > 0);
  
  return { cells, total, highRiskTotal, highRiskPct, riskPriority };
});

// ── 偏差值口语化描述 ──
const describeDeviation = (dev, threshold) => {
  const absDev = Math.abs(dev);
  if (absDev > 3 * threshold) return dev > 0 ? '远超同类，断档领先' : '严重掉队，排名垫底';
  if (absDev > 2 * threshold) return dev > 0 ? '明显优于同类' : '明显落后于同类';
  if (absDev > threshold) return dev > 0 ? '略好于同类' : '略差于同类';
  return '与同类基本持平';
};

const confidenceScore = computed(() => {
  const data = performanceData.value;
  if (data.length === 0) return 0;
  const neutralRatio = summary.value.neutralCount / data.length;
  let score = 65;
  if (data.length > 20) score += 10;
  if (data.length > 50) score += 5;
  if (topDrivers.value.length >= 3) score += 10;
  if (neutralRatio > 0.3 && neutralRatio < 0.9) score += 10;
  return Math.min(99, score);
});

const confidenceColor = computed(() => {
  if (confidenceScore.value >= 85) return '#10b981';
  if (confidenceScore.value >= 70) return '#6366f1';
  if (confidenceScore.value >= 50) return '#f59e0b';
  return '#f43f5e';
});

const confidenceTextColor = computed(() => {
  if (confidenceScore.value >= 85) return 'text-emerald-600';
  if (confidenceScore.value >= 70) return 'text-indigo-600';
  if (confidenceScore.value >= 50) return 'text-amber-600';
  return 'text-rose-600';
});

// ── 简报生成 ──
const generateFullReport = () => {
  isGeneratingReport.value = true;
  setTimeout(() => {
    refreshReportHTML();
    isGeneratingReport.value = false;
    showReportModal.value = true;
  }, 500);
};

const printReport = () => {
  const win = window.open('', '_blank', 'width=900,height=700');
  if (win) {
    win.document.write(`
      <html>
        <head><title>决策研判简报</title>
        <style>body { font-family: 'Microsoft YaHei', sans-serif; padding: 40px; max-width: 800px; margin: auto; color: #1e293b; } @media print { body { padding: 20px; } }</style>
        </head>
        <body>${reportHTML.value}</body>
      </html>
    `);
    win.document.close();
    setTimeout(() => win.print(), 500);
  }
};

const copyReport = () => {
  const text = (reportContentRef.value?.innerText || '').trim();
  if (text) {
    navigator.clipboard.writeText(text).then(() => {
      alert('简报内容已复制到剪贴板');
    }).catch(() => alert('复制失败，请手动选择文本复制'));
  }
};

// ── 简报 PDF 导出 ──
const pdfSections = computed(() => {
  const date = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
  const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  const modeLabel = isLiveMode.value ? '（推演模拟数据·实时）' : '';
  const rm = riskMatrix.value;
  const cs = confidenceScore.value;
  const cColor = confidenceColor.value;
  const sections = [];

  // SVG 可信度环
  const svgRing = `
    <div style="text-align:center;margin:16px 0;">
      <svg width="110" height="110" viewBox="0 0 96 96" style="transform:rotate(-90deg);">
        <circle cx="48" cy="48" r="40" fill="none" stroke="#e2e8f0" stroke-width="7"/>
        <circle cx="48" cy="48" r="40" fill="none" stroke="${cColor}" stroke-width="7"
          stroke-dasharray="${(2 * Math.PI * 40).toFixed(1)}"
          stroke-dashoffset="${(2 * Math.PI * 40 * (1 - cs / 100)).toFixed(1)}"
          stroke-linecap="round"/>
      </svg>
      <div style="position:relative;top:-92px;font-size:26px;font-weight:900;color:${cColor};">${cs}%</div>
      <div style="position:relative;top:-94px;font-size:10px;color:#94a3b8;font-weight:600;">可信度</div>
    </div>`;

  // 封面 CSS 框架
  const coverCSS = 'font-family:\'Microsoft YaHei\',\'PingFang SC\',sans-serif;color:#1e293b;max-width:700px;margin:auto;';
  const sectionCSS = 'background:#f8fafc;border-radius:14px;padding:22px;margin-bottom:22px;border:1px solid #e2e8f0;';

  // === S0: 封面 + 分析概要 ===
  sections.push({ html: `
    <div style="${coverCSS}padding:0 10px;">
      <div style="text-align:center;margin-bottom:24px;border-bottom:3px solid #4f46e5;padding-bottom:16px;">
        <h1 style="font-size:24px;font-weight:900;color:#0f172a;margin:0;">决策研判简报 ${modeLabel}</h1>
        <p style="font-size:14px;color:#6366f1;margin:8px 0 2px;">基于贝叶斯层次网络模型的分析报告</p>
        <p style="font-size:11px;color:#94a3b8;margin:0;">${date} · ${time}</p>
      </div>
      <div style="${sectionCSS}background:#f0f4ff;border-color:#c7d2fe;">
        <h2 style="font-size:17px;font-weight:800;color:#4f46e5;margin:0 0 14px;">◆ 分析概要</h2>
        <table style="width:100%;border-collapse:collapse;font-size:13px;line-height:2;">
          <tr><td style="color:#64748b;width:115px;">评估对象数</td><td style="font-weight:700;">${summary.value.totalNodes} 个</td></tr>
          <tr><td style="color:#64748b;">组织层级</td><td style="font-weight:700;">${summary.value.totalLevels} 层</td></tr>
          ${props.hierarchySchema ? props.hierarchySchema.map((lvl, i) => `
          <tr><td style="color:#94a3b8;font-size:11px;padding-left:8px;">└ 层级 ${i + 1}</td><td style="font-size:11px;">${lvl.level_name}（ID: ${lvl.id_column}，因子：${(lvl.covariates || []).map(c => props.displayMapping[c] || c).join('、') || '无'}）</td></tr>
          `).join('') : ''}
          <tr><td style="color:#64748b;">评估目标</td><td style="font-weight:700;">${props.targetVariable?.name || '目标指标'}</td></tr>
          <tr><td style="color:#64748b;">分析方法</td><td style="font-size:11px;color:#475569;">层次贝叶斯网络（MCMC后验采样），排除客观条件差异后的净贡献评估</td></tr>
          <tr><td style="color:#64748b;">使用限制</td><td style="font-size:11px;color:#94a3b8;">分析关联关系，不等同于因果关系。建议结合业务经验综合判断。</td></tr>
        </table>
        <div style="display:flex;gap:14px;margin-top:18px;">
          <div style="flex:1;background:linear-gradient(135deg,#d1fae5,#ecfdf5);border-radius:12px;padding:16px;text-align:center;border:1px solid #a7f3d0;">
            <div style="font-size:28px;font-weight:900;color:#059669;">${summary.value.brightCount}</div>
            <div style="font-size:12px;font-weight:700;color:#065f46;">表现突出</div>
            <div style="font-size:10px;color:#6ee7b7;">超出预期</div>
          </div>
          <div style="flex:1;background:linear-gradient(135deg,#fef3c7,#fffbeb);border-radius:12px;padding:16px;text-align:center;border:1px solid #fcd34d;">
            <div style="font-size:28px;font-weight:900;color:#d97706;">${summary.value.neutralCount}</div>
            <div style="font-size:12px;font-weight:700;color:#92400e;">运行正常</div>
            <div style="font-size:10px;color:#fbbf24;">符合预期</div>
          </div>
          <div style="flex:1;background:linear-gradient(135deg,#fee2e2,#fef2f2);border-radius:12px;padding:16px;text-align:center;border:1px solid #fecaca;">
            <div style="font-size:28px;font-weight:900;color:#dc2626;">${summary.value.darkCount}</div>
            <div style="font-size:12px;font-weight:700;color:#991b1b;">需要关注</div>
            <div style="font-size:10px;color:#fca5a5;">低于预期</div>
          </div>
        </div>
        ${svgRing}
        <p style="font-size:11px;color:#64748b;text-align:center;margin-top:4px;">综合数据量与模型收敛性评估 · 可信度越高结论越可靠</p>
      </div>
    </div>` });

  // === S1: 推演参数（如适用）===
  if (isLiveMode.value && props.liveCovariates) {
    sections.push({ html: `
    <div style="${coverCSS}padding:0 10px;">
      <div style="${sectionCSS}background:#fffbeb;border-color:#fcd34d;">
        <h2 style="font-size:17px;font-weight:800;color:#d97706;margin:0 0 12px;">⚙ 参数调整记录（前置条件）</h2>
        <p style="font-size:12px;color:#92400e;margin-bottom:12px;">以下参数在原始分析基础上进行了调整，当前报告反映调整后的模拟推演结果。β 为正表示该指标越高越好，为负表示过高反而拖累。调整幅度以标准差(σ)为单位。</p>
        <table style="width:100%;border-collapse:collapse;font-size:12px;">
          <thead><tr style="background:#fef3c7;"><th style="padding:6px 10px;text-align:left;border-bottom:2px solid #fbbf24;">参数名称</th><th style="padding:6px 10px;text-align:center;border-bottom:2px solid #fbbf24;">β</th><th style="padding:6px 10px;text-align:center;border-bottom:2px solid #fbbf24;">调整幅度</th><th style="padding:6px 10px;text-align:left;border-bottom:2px solid #fbbf24;">含义</th></tr></thead>
          <tbody>
            ${props.liveCovariates.filter(c => Math.abs(c.delta) > 0.01).map(c => `
              <tr style="border-bottom:1px solid #fde68a;">
                <td style="padding:6px 10px;font-weight:700;">${c.name}</td>
                <td style="padding:6px 10px;text-align:center;font-family:monospace;color:${c.beta > 0 ? '#10b981' : '#f43f5e'};">${c.beta > 0 ? '+' : ''}${c.beta.toFixed(4)}</td>
                <td style="padding:6px 10px;text-align:center;font-family:monospace;font-weight:700;color:${c.delta > 0 ? '#10b981' : '#f43f5e'};">${c.delta > 0 ? '+' : ''}${c.delta.toFixed(1)}σ</td>
                <td style="padding:6px 10px;font-size:11px;color:#78350f;">${c.delta > 0 ? '上调' : '下调'}${Math.abs(c.delta) > 2 ? '（大幅）' : Math.abs(c.delta) > 1 ? '（中幅）' : '（微调）'}</td>
              </tr>
            `).join('')}
            ${props.liveCovariates.filter(c => Math.abs(c.delta) > 0.01).length === 0 ? '<tr><td colspan="4" style="padding:6px;text-align:center;color:#92400e;">所有参数保持默认值</td></tr>' : ''}
          </tbody>
        </table>
      </div>
    </div>` });
  }

  // === S2: 关键驱动因素 ===
  sections.push({ html: `
    <div style="${coverCSS}padding:0 10px;">
      <div style="${sectionCSS}">
        <h2 style="font-size:17px;font-weight:800;color:#4f46e5;margin:0 0 6px;">◆ 一、关键驱动因素</h2>
        <p style="font-size:12px;color:#64748b;margin:0 0 14px;">以下因素对结果的影响力最大，排序靠前的应作为资源配置的优先方向。</p>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead><tr style="background:#eef2ff;"><th style="padding:10px 14px;text-align:left;border-bottom:2px solid #c7d2fe;">因素</th><th style="padding:10px 14px;text-align:right;border-bottom:2px solid #c7d2fe;">影响 (β)</th><th style="padding:10px 14px;text-align:left;border-bottom:2px solid #c7d2fe;">含义</th></tr></thead>
          <tbody>
            ${topDrivers.value.map((d, i) => `
              <tr style="border-bottom:1px solid #e2e8f0;${i === 0 ? 'background:#f0fdf4;' : ''}">
                <td style="padding:10px 14px;font-weight:700;">${i + 1}. ${d.name}</td>
                <td style="padding:10px 14px;text-align:right;font-family:monospace;font-weight:700;color:${d.beta > 0 ? '#059669' : '#dc2626'};">${d.beta > 0 ? '+' : ''}${d.beta.toFixed(4)}</td>
                <td style="padding:10px 14px;font-size:12px;color:#475569;">${d.beta > 0 ? '越高越好，正面推动' : '过高反而拖累，注意平衡'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>` });

  // === S3: 关注优先级 ===
  sections.push({ html: `
    <div style="${coverCSS}padding:0 10px;">
      <div style="${sectionCSS}">
        <h2 style="font-size:17px;font-weight:800;color:#4f46e5;margin:0 0 6px;">◆ 二、关注优先级</h2>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead><tr style="background:#eef2ff;"><th style="padding:10px 14px;text-align:left;border-bottom:2px solid #c7d2fe;">对象</th><th style="padding:10px 14px;text-align:right;border-bottom:2px solid #c7d2fe;">偏差</th><th style="padding:10px 14px;text-align:left;border-bottom:2px solid #c7d2fe;">判断</th><th style="padding:10px 14px;text-align:left;border-bottom:2px solid #c7d2fe;">建议</th></tr></thead>
          <tbody>
            ${priorityRanked.value.slice(0, 10).map((d, i) => `
              <tr style="border-bottom:1px solid #e2e8f0;${d.priority === 'critical' ? 'background:#fff5f5;' : d.priority === 'high' ? 'background:#fffbeb;' : ''}">
                <td style="padding:10px 14px;font-weight:700;">${i + 1}. ${d.name}</td>
                <td style="padding:10px 14px;text-align:right;font-family:monospace;font-weight:700;color:${d.Deviation > 0 ? '#059669' : '#dc2626'};">${d.Deviation > 0 ? '+' : ''}${Math.abs(d.Deviation).toFixed(2)}σ</td>
                <td style="padding:10px 14px;font-size:11px;color:#475569;">${d.devDesc || ''}</td>
                <td style="padding:10px 14px;font-size:11px;color:#475569;">${d.advice}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>` });

  // === S4: 风险分布热力图 ===
  const heatCell = (label, count, bg, color, weight, borderClr) => `
    <td style="padding:10px;background:${count > 0 ? bg : '#f8fafc'};color:${count > 0 ? color : '#cbd5e1'};font-weight:${weight};font-size:${count > 0 && label === 'high_high' ? '15px' : '12px'};border:${count > 0 ? '2px' : '1px'} solid ${count > 0 ? borderClr : '#e2e8f0'};">${count}</td>`;

  sections.push({ html: `
    <div style="${coverCSS}padding:0 10px;">
      <div style="${sectionCSS}">
        <h2 style="font-size:17px;font-weight:800;color:#4f46e5;margin:0 0 6px;">◆ 三、风险分布</h2>
        <p style="font-size:12px;color:#64748b;margin:0 0 14px;">高风险区共 <strong style="color:#dc2626;">${rm.highRiskTotal}</strong> 个对象（占 ${rm.highRiskPct}%）。${rm.cells.high_high.count > 0 ? rm.cells.high_high.nodes.slice(0, 5).join('、') + (rm.cells.high_high.nodes.length > 5 ? ' 等' : '') + ' 需优先处置。' : ''}</p>
        <table style="width:100%;border-collapse:collapse;font-size:12px;text-align:center;border-radius:10px;overflow:hidden;border:1px solid #e2e8f0;">
          <tr style="background:#f1f5f9;">
            <td style="padding:10px;color:#64748b;font-weight:700;">不确定性 →<br>↓ 偏差幅度</td>
            <td style="padding:10px;color:#94a3b8;font-weight:600;">小</td>
            <td style="padding:10px;color:#94a3b8;font-weight:600;">中</td>
            <td style="padding:10px;color:#94a3b8;font-weight:600;">大</td>
          </tr>
          <tr>
            <td style="padding:10px;color:#64748b;font-weight:600;background:#f8fafc;">大</td>
            ${heatCell('low_high', rm.cells.low_high.count, '#fef2f2', '#dc2626', 700, '#fecaca')}
            ${heatCell('mid_high', rm.cells.mid_high.count, '#fef2f2', '#dc2626', 700, '#fecaca')}
            ${heatCell('high_high', rm.cells.high_high.count, '#fee2e2', '#dc2626', 900, '#fca5a5')}
          </tr>
          <tr>
            <td style="padding:10px;color:#64748b;font-weight:600;background:#f8fafc;">中</td>
            ${heatCell('low_mid', rm.cells.low_mid.count, '#fffbeb', '#d97706', 700, '#fde68a')}
            ${heatCell('mid_mid', rm.cells.mid_mid.count, '#fffbeb', '#d97706', 700, '#fde68a')}
            ${heatCell('high_mid', rm.cells.high_mid.count, '#fff7ed', '#ea580c', 700, '#fed7aa')}
          </tr>
          <tr>
            <td style="padding:10px;color:#64748b;font-weight:600;background:#f8fafc;">小</td>
            ${heatCell('low_low', rm.cells.low_low.count, '#f0fdf4', '#059669', 700, '#a7f3d0')}
            ${heatCell('mid_low', rm.cells.mid_low.count, '#f0fdf4', '#059669', 700, '#a7f3d0')}
            ${heatCell('high_low', rm.cells.high_low.count, '#fffbeb', '#d97706', 700, '#fde68a')}
          </tr>
        </table>
        ${rm.cells.high_high.count > 0 ? `
        <div style="background:#fff5f5;border-radius:8px;padding:12px;margin-top:12px;border-left:4px solid #ef4444;">
          <span style="font-size:12px;font-weight:700;color:#dc2626;">『偏离大+影响大』（最紧急）：</span>
          <span style="font-size:12px;color:#991b1b;">${rm.cells.high_high.nodes.join('、')}</span>
        </div>` : ''}
      </div>
    </div>` });

  // === S5: 行动建议 ===
  sections.push({ html: `
    <div style="${coverCSS}padding:0 10px;">
      <div style="${sectionCSS}">
        <h2 style="font-size:17px;font-weight:800;color:#4f46e5;margin:0 0 6px;">◆ 四、行动建议</h2>
        ${recommendations.value.map(r => `
          <div style="margin-bottom:14px;padding:14px;border-radius:10px;border-left:5px solid ${r.type === 'urgent' ? '#ef4444' : r.type === 'strategic' ? '#6366f1' : '#10b981'};background:${r.type === 'urgent' ? '#fff5f5' : r.type === 'strategic' ? '#f5f3ff' : '#f0fdf4'};">
            <p style="font-size:13px;font-weight:700;color:#0f172a;margin:0 0 6px;">${r.type === 'urgent' ? '立即处置' : r.type === 'strategic' ? '战略调整' : '经验推广'}：${r.scope}</p>
            <p style="font-size:13px;color:#334155;margin:0 0 4px;">${r.content}</p>
            ${r.expectedImpact ? '<p style="font-size:11px;color:#94a3b8;margin:0;">预期效果：' + r.expectedImpact + '</p>' : ''}
          </div>
        `).join('')}
      </div>
      <div style="text-align:center;padding-top:18px;border-top:1px solid #e2e8f0;margin-top:26px;">
        <p style="font-size:11px;color:#94a3b8;">本报告由系统自动生成，建议基于数据推算，实际执行请结合业务判断。</p>
      </div>
    </div>` });

  // 生成合并的完整 HTML（供预览和 HTML 导出用）
  const fullHTML = sections.map(s => s.html).join('');

  return { sections, fullHTML };
});

// 辅助：渲染 HTML 为 canvas
const renderSectionCanvas = async (html2canvas, sectionHTML) => {
  const container = document.createElement('div');
  container.innerHTML = sectionHTML;
  container.style.cssText = 'position:fixed;left:-9999px;top:0;width:800px;padding:16px 20px;font-family:\'Microsoft YaHei\',\'PingFang SC\',sans-serif;color:#1e293b;background:white;line-height:1.6;';
  document.body.appendChild(container);
  await new Promise(r => setTimeout(r, 200));
  const canvas = await html2canvas(container, {
    scale: 1.5, useCORS: true, logging: false,
    width: 800, height: container.scrollHeight,
  });
  document.body.removeChild(container);
  return canvas;
};

const exportPDF = async () => {
  if (isPdfExporting.value) return;
  isPdfExporting.value = true;
  try {
    const html2canvas = (await import('html2canvas')).default;
    const { jsPDF } = await import('jspdf');

    const report = pdfSections.value;
    const pdf = new jsPDF('p', 'mm', 'a4');
    const margin = 14;
    const usableHeight = 297 - 2 * margin;
    const contentWidth = 210 - 2 * margin;
    let currentY = margin;

    for (let i = 0; i < report.sections.length; i++) {
      const sectionHTML = report.sections[i].html;
      const canvas = await renderSectionCanvas(html2canvas, sectionHTML);
      const imgData = canvas.toDataURL('image/jpeg', 0.85);
      const imgHeight = (canvas.height * contentWidth) / canvas.width;

      if (imgHeight <= usableHeight) {
        // 完整放入一页
        if (currentY + imgHeight > margin + usableHeight) {
          pdf.addPage();
          currentY = margin;
        }
        pdf.addImage(imgData, 'JPEG', margin, currentY, contentWidth, imgHeight);
        currentY += imgHeight + 5;
      } else {
        // 超过一页——切片渲染
        if (i > 0) { pdf.addPage(); currentY = margin; }
        let remaining = imgHeight;
        let pn = 0;
        const yOffsets = [margin];
        while (remaining > 0) {
          if (pn > 0) { pdf.addPage(); currentY = margin; }
          pdf.addImage(imgData, 'JPEG', margin, currentY - pn * usableHeight, contentWidth, imgHeight);
          remaining -= usableHeight;
          pn++;
        }
        currentY = margin + (imgHeight % usableHeight || usableHeight);
      }
    }

    const date = new Date().toLocaleDateString('zh-CN').replace(/\//g, '-');
    const defaultName = '决策研判简报_' + date + '.pdf';
    try {
      const { save } = await import('@tauri-apps/plugin-dialog');
      const { writeFile } = await import('@tauri-apps/plugin-fs');
      const filePath = await save({ defaultPath: defaultName, filters: [{ name: 'PDF Document', extensions: ['pdf'] }] });
      if (filePath) {
        const pdfBlob = pdf.output('blob');
        const buf = await pdfBlob.arrayBuffer();
        await writeFile(filePath, new Uint8Array(buf));
      }
    } catch { pdf.save(defaultName); }
  } catch (e) {
    console.error('PDF export error:', e);
    alert('导出 PDF 失败：' + (e.message || e));
  } finally {
    isPdfExporting.value = false;
  }
};

// ── HTML 导出 ──
const exportHTML = async () => {
  if (isHtmlExporting.value) return;
  isHtmlExporting.value = true;
  try {
    const report = pdfSections.value;
    const fullMeta = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>决策研判简报</title>
  <style>body{font-family:'Microsoft YaHei','PingFang SC',sans-serif;background:#f1f5f9;padding:40px 20px;margin:0;}</style>
</head>
<body>
${report.fullHTML}
</body>
</html>`;

    const date = new Date().toLocaleDateString('zh-CN').replace(/\//g, '-');
    const defaultName = '决策研判简报_' + date + '.html';
    try {
      const { save } = await import('@tauri-apps/plugin-dialog');
      const { writeTextFile } = await import('@tauri-apps/plugin-fs');
      const filePath = await save({ defaultPath: defaultName, filters: [{ name: 'HTML Document', extensions: ['html'] }] });
      if (filePath) { await writeTextFile(filePath, fullMeta); }
    } catch {
      const blob = new Blob(['﻿' + fullMeta], { type: 'text/html;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = defaultName; a.click();
      URL.revokeObjectURL(url);
    }
  } catch (e) {
    console.error('HTML export error:', e);
    alert('导出 HTML 失败：' + (e.message || e));
  } finally {
    isHtmlExporting.value = false;
  }
};

const copyDecisionSummary = () => {
  const lines = [
    '【决策研判摘要】',
    '',
    `总览：${summary.value.totalNodes} 个对象 / ${summary.value.totalLevels} 层。突出 ${summary.value.brightCount} 个，关注 ${summary.value.darkCount} 个，正常 ${summary.value.neutralCount} 个。`,
    '',
    '驱动因素（按影响力）：',
    ...topDrivers.value.map((d, i) => `  ${i + 1}. ${d.name}：${d.beta > 0 ? '+' : ''}${d.beta.toFixed(4)}（${d.beta > 0 ? '正面推动' : '负面拖累'}）`),
    '',
    '关注排序：',
    ...priorityRanked.value.slice(0, 5).map((d, i) => `  ${i + 1}. [${d.priority === 'critical' ? '紧急' : d.priority === 'high' ? '关注' : d.priority === 'positive' ? '标杆' : '正常'}] ${d.name} → ${d.advice}`),
    '',
    '行动建议：',
    ...recommendations.value.map(r => `  • [${r.type === 'urgent' ? '立即' : r.type === 'strategic' ? '战略' : '推广'}] ${r.content.substring(0, 100)}`),
    '',
    `可信度：${confidenceScore.value}%`
  ];
  
  navigator.clipboard.writeText(lines.join('\n')).then(() => {
    alert('摘要已复制，可直接粘贴到工作文档或消息中。');
  }).catch(() => alert('复制失败，请重试。'));
};

// 实时模式：数据变化时自动刷新简报内容
watch(() => [props.livePerformanceData, showReportModal.value], ([newData, modalOpen]) => {
  if (newData) {
    console.log('[DecisionCenter] 收到实时推演数据，共', newData.length, '条');
  }
  // 简报打开且处于实时模式时，自动刷新内容
  if (modalOpen && isLiveMode.value && newData) {
    refreshReportHTML();
  }
});

// 独立的简报 HTML 刷新函数（不加 loading 状态，静默更新）
const refreshReportHTML = () => {
  const date = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
  const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  const modeLabel = isLiveMode.value ? '（推演模拟数据 · 实时）' : '';
  const rm = riskMatrix.value;
  
  reportHTML.value = `
    <div style="font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; color: #1e293b; max-width: 720px; margin: auto;">
      <div style="text-align: center; margin-bottom: 24px; border-bottom: 3px solid #4f46e5; padding-bottom: 16px;">
        <h1 style="font-size: 22px; font-weight: 900; color: #1e293b; margin: 0;">决策研判简报 ${modeLabel}</h1>
        <p style="font-size: 13px; color: #64748b; margin-top: 6px;">基于贝叶斯层次网络模型的分析报告</p>
        <p style="font-size: 11px; color: #94a3b8; margin-top: 4px;">${date} ${time}</p>
      </div>
      
      <!-- 前置说明：场景设定 -->
      <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #cbd5e1;">
        <h2 style="font-size: 16px; font-weight: 800; color: #475569; margin: 0 0 12px 0;">分析场景与前置条件</h2>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
          <tr><td style="padding: 4px 8px; color: #64748b; width: 120px;">评估对象数</td><td style="padding: 4px 8px; font-weight: 700;">${summary.value.totalNodes} 个</td></tr>
          <tr><td style="padding: 4px 8px; color: #64748b;">组织层级</td><td style="padding: 4px 8px; font-weight: 700;">${summary.value.totalLevels} 层</td></tr>
          ${props.hierarchySchema ? props.hierarchySchema.map((lvl, i) => `
          <tr><td style="padding: 4px 8px; color: #94a3b8; font-size: 11px;">层级 ${i + 1}</td><td style="padding: 4px 8px; font-size: 11px;">${lvl.level_name}（标识列：${lvl.id_column}，影响因素：${(lvl.covariates || []).map(c => props.displayMapping[c] || c).join('、') || '无'}）</td></tr>
          `).join('') : ''}
          <tr><td style="padding: 4px 8px; color: #64748b;">评估目标</td><td style="padding: 4px 8px; font-weight: 700;">${props.targetVariable?.name || '目标指标'}</td></tr>
          <tr><td style="padding: 4px 8px; color: #64748b;">分析方法</td><td style="padding: 4px 8px; font-size: 11px; color: #64748b;">层次贝叶斯网络模型（MCMC后验采样），排除客观条件差异后的净贡献评估</td></tr>
          <tr><td style="padding: 4px 8px; color: #64748b;">使用限制</td><td style="padding: 4px 8px; font-size: 11px; color: #94a3b8;">分析的是关联关系，不等同于因果关系。建议结合业务经验综合判断。</td></tr>
        </table>
      </div>
      
      ${isLiveMode.value && props.liveCovariates ? `
      <div style="background: #fffbeb; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #fcd34d;">
        <h2 style="font-size: 16px; font-weight: 800; color: #d97706; margin: 0 0 12px 0;">⚙ 参数调整记录（前置条件）</h2>
        <p style="font-size: 12px; color: #92400e; margin-bottom: 12px;">以下参数在原始分析基础上进行了调整，当前报告反映的是调整后的模拟推演结果。</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
          <thead>
            <tr style="background: #fef3c7;">
              <th style="padding: 6px 10px; text-align: left; border-bottom: 2px solid #fbbf24;">参数名称</th>
              <th style="padding: 6px 10px; text-align: center; border-bottom: 2px solid #fbbf24;">影响力(β)</th>
              <th style="padding: 6px 10px; text-align: center; border-bottom: 2px solid #fbbf24;">调整幅度</th>
              <th style="padding: 6px 10px; text-align: left; border-bottom: 2px solid #fbbf24;">调整含义</th>
            </tr>
          </thead>
          <tbody>
            ${props.liveCovariates.filter(c => Math.abs(c.delta) > 0.01).map(c => `
              <tr style="border-bottom: 1px solid #fde68a;">
                <td style="padding: 6px 10px; font-weight: 700;">${c.name}</td>
                <td style="padding: 6px 10px; text-align: center; font-family: monospace; color: ${c.beta > 0 ? '#10b981' : '#f43f5e'};">${c.beta > 0 ? '+' : ''}${c.beta.toFixed(4)}</td>
                <td style="padding: 6px 10px; text-align: center; font-family: monospace; font-weight: 700; color: ${c.delta > 0 ? '#10b981' : '#f43f5e'};">${c.delta > 0 ? '+' : ''}${c.delta.toFixed(1)}σ</td>
                <td style="padding: 6px 10px; font-size: 11px; color: #78350f;">${c.delta > 0 ? '上调至高于均值水平' : '下调至低于均值水平'}${Math.abs(c.delta) > 2 ? '（大幅度）' : Math.abs(c.delta) > 1 ? '（中等幅度）' : '（小幅微调）'}</td>
              </tr>
            `).join('')}
            ${props.liveCovariates.filter(c => Math.abs(c.delta) > 0.01).length === 0 ? '<tr><td colspan="4" style="padding: 6px 10px; text-align: center; color: #92400e;">所有参数保持默认值，未做调整</td></tr>' : ''}
          </tbody>
        </table>
        <p style="font-size: 10px; color: #a16207; margin-top: 8px;">提示：β 为正表示该指标越高越好，为负表示过高反而拖累。调整幅度以标准差(σ)为单位，±1σ 约等于从均值到前/后 16% 的位置。</p>
      </div>
      ` : ''}
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
        <h2 style="font-size: 16px; font-weight: 800; color: #4f46e5; margin: 0 0 12px 0;">一、总体情况</h2>
        <p style="font-size: 13px; color: #475569; line-height: 1.8;">
          覆盖 <strong>${summary.value.totalNodes}</strong> 个评估对象，<strong>${summary.value.totalLevels}</strong> 层组织关系。
          突出 <strong style="color: #10b981;">${summary.value.brightCount}</strong> 个，
          关注 <strong style="color: #f43f5e;">${summary.value.darkCount}</strong> 个，
          正常 ${summary.value.neutralCount} 个。
        </p>
        ${isLiveMode.value ? '<p style="font-size: 12px; color: #d97706; margin-top: 8px;">此报告基于参数调整后的推演数据，非原始分析结果。</p>' : ''}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
        <h2 style="font-size: 16px; font-weight: 800; color: #4f46e5; margin: 0 0 12px 0;">二、关键驱动因素</h2>
        <p style="font-size: 12px; color: #64748b; margin-bottom: 12px;">以下因素对结果的影响力最大，排序靠前的应作为资源配置的优先方向。</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
          <thead>
            <tr style="background: #eef2ff;">
              <th style="padding: 8px 12px; text-align: left; border-bottom: 2px solid #c7d2fe;">因素</th>
              <th style="padding: 8px 12px; text-align: right; border-bottom: 2px solid #c7d2fe;">影响力</th>
              <th style="padding: 8px 12px; text-align: left; border-bottom: 2px solid #c7d2fe;">含义</th>
            </tr>
          </thead>
          <tbody>
            ${topDrivers.value.map(d => `
              <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 8px 12px; font-weight: 700;">${d.name}</td>
                <td style="padding: 8px 12px; text-align: right; font-family: monospace; color: ${d.beta > 0 ? '#10b981' : '#f43f5e'}; font-weight: 700;">${d.beta > 0 ? '+' : ''}${d.beta.toFixed(4)}</td>
                <td style="padding: 8px 12px; font-size: 11px; color: #64748b;">${d.beta > 0 ? '越高越好，正面推动' : '过高反而拖累，注意平衡'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
        <h2 style="font-size: 16px; font-weight: 800; color: #4f46e5; margin: 0 0 12px 0;">三、关注优先级</h2>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
          <thead>
            <tr style="background: #eef2ff;">
              <th style="padding: 8px 12px; text-align: left; border-bottom: 2px solid #c7d2fe;">对象</th>
              <th style="padding: 8px 12px; text-align: right; border-bottom: 2px solid #c7d2fe;">偏差</th>
              <th style="padding: 8px 12px; text-align: left; border-bottom: 2px solid #c7d2fe;">判断</th>
              <th style="padding: 8px 12px; text-align: left; border-bottom: 2px solid #c7d2fe;">建议</th>
            </tr>
          </thead>
          <tbody>
            ${priorityRanked.value.slice(0, 10).map((d, i) => `
              <tr style="border-bottom: 1px solid #e2e8f0; ${d.priority === 'critical' ? 'background: #fff5f5;' : d.priority === 'high' ? 'background: #fffbf0;' : ''}">
                <td style="padding: 8px 12px; font-weight: 700;">${i + 1}. ${d.name}</td>
                <td style="padding: 8px 12px; text-align: right; font-family: monospace; font-weight: 700; color: ${d.Deviation > 0 ? '#10b981' : '#f43f5e'};">${d.Deviation > 0 ? '+' : ''}${Math.abs(d.Deviation).toFixed(2)}σ</td>
                <td style="padding: 8px 12px; font-size: 11px; color: #64748b;">${d.devDesc || ''}</td>
                <td style="padding: 8px 12px; font-size: 11px; color: #64748b;">${d.advice}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
        <h2 style="font-size: 16px; font-weight: 800; color: #4f46e5; margin: 0 0 12px 0;">四、风险分布</h2>
        <p style="font-size: 12px; color: #64748b; margin-bottom: 12px;">
          高风险区共 <strong style="color: #f43f5e;">${rm.highRiskTotal}</strong> 个对象（占 ${rm.highRiskPct}%）。
          ${rm.cells.high_high.count > 0 ? `最需关注的是偏离大、影响大的 ${rm.cells.high_high.count} 个：${rm.cells.high_high.nodes.join('、')}。` : ''}
          ${rm.cells.high_mid.count > 0 ? `偏离大、影响中的 ${rm.cells.high_mid.count} 个：${rm.cells.high_mid.nodes.join('、')}。` : ''}
        </p>
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
        <h2 style="font-size: 16px; font-weight: 800; color: #4f46e5; margin: 0 0 12px 0;">五、行动建议</h2>
        ${recommendations.value.map(r => `
          <div style="margin-bottom: 12px; padding: 12px; border-radius: 8px; border-left: 4px solid ${r.type === 'urgent' ? '#f43f5e' : r.type === 'strategic' ? '#4f46e5' : '#10b981'}; background: ${r.type === 'urgent' ? '#fff5f5' : r.type === 'strategic' ? '#f5f3ff' : '#f0fdf4'};">
            <p style="font-size: 12px; font-weight: 700; color: #1e293b; margin: 0 0 6px 0;">${r.type === 'urgent' ? '立即处置' : r.type === 'strategic' ? '战略调整' : '经验推广'}：${r.scope}</p>
            <p style="font-size: 12px; color: #475569; margin: 0 0 4px 0;">${r.content}</p>
            ${r.expectedImpact ? `<p style="font-size: 11px; color: #94a3b8; margin: 0;">预期效果：${r.expectedImpact}</p>` : ''}
          </div>
        `).join('')}
      </div>
      
      <div style="text-align: center; padding-top: 16px; border-top: 1px solid #e2e8f0; margin-top: 24px;">
        <p style="font-size: 11px; color: #94a3b8;">本报告由系统自动生成，建议基于数据推算，实际执行请结合业务判断。</p>
      </div>
    </div>
  `;
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
