<template>
  <transition name="fade">
    <div v-if="show" class="fixed inset-0 bg-slate-900/40 backdrop-blur-md flex justify-center items-center z-[100]" @click.self="$emit('close')">
      <div class="w-full max-w-6xl max-h-[92vh] bg-white rounded-3xl shadow-[0_40px_80px_-20px_rgba(0,0,0,0.25)] flex flex-col overflow-hidden animate-scale-in border border-slate-200">
        <div class="px-10 py-7 bg-white border-b border-slate-100 flex justify-between items-center shrink-0">
          <div class="flex items-center">
            <div class="w-14 h-14 rounded-2xl bg-indigo-600 flex items-center justify-center mr-6 shadow-xl shadow-indigo-100">
               <i class="fas fa-book-open text-2xl text-white"></i>
            </div>
            <div>
              <h2 class="text-2xl font-black text-slate-900 tracking-tight">使用手册与决策指南</h2>
              <p class="text-xs text-slate-500 mt-1.5 font-medium">理解算法逻辑 → 掌握操作流程 → 读懂分析结果 → 应用到决策</p>
            </div>
          </div>
          <button @click="$emit('close')" class="w-12 h-12 rounded-full bg-slate-50 hover:bg-slate-100 flex items-center justify-center transition-all text-slate-400 hover:text-slate-600">
            <i class="fas fa-times text-xl"></i>
          </button>
        </div>

        <div class="flex flex-1 overflow-hidden">
          <div class="w-64 bg-slate-50 border-r border-slate-100 p-6 space-y-1.5 shrink-0">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-[0.25em] mb-4">目录</div>
            <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
              :class="activeTab === tab.id ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100' : 'text-slate-500 hover:bg-slate-200'"
              class="w-full text-left px-4 py-3 rounded-xl text-[12px] font-bold transition-all flex items-center group mb-1.5">
              <i :class="tab.icon" class="mr-3 w-4 text-center"></i>{{ tab.label }}
            </button>
          </div>

          <div class="flex-1 overflow-y-auto p-10 custom-scrollbar bg-white selection:bg-indigo-100">

            <!-- Tab: 系统概述 -->
            <div v-if="activeTab === 'overview'" class="space-y-10 animate-fade-in max-w-4xl">
              <section>
                <h2 class="text-xl font-black text-slate-800 mb-4">这个系统做什么</h2>
                <p class="text-sm text-slate-600 leading-relaxed mb-6">
                  管理者面临一个常见问题：下属单位表现不同，但它们的客观条件也不同。简单按业绩排名不公平，因为条件好的单位"理应"做得更好。
                  这个系统的核心任务是：<strong>排除客观条件差异，算出每个单位的"净贡献"，然后告诉您谁值得表彰、谁需要帮助、资源投向哪里最划算。</strong>
                </p>
                <div class="bg-indigo-50 p-5 rounded-2xl border border-indigo-100">
                  <p class="text-sm text-indigo-800 font-bold mb-2">四步工作流程</p>
                  <div class="grid grid-cols-4 gap-3 text-xs">
                    <div class="bg-white p-3 rounded-lg text-center"><div class="font-black text-indigo-600 mb-1">① 建网</div><div class="text-slate-500">根据组织层级搭建影响关系网</div></div>
                    <div class="bg-white p-3 rounded-lg text-center"><div class="font-black text-indigo-600 mb-1">② 测算</div><div class="text-slate-500">数千次模拟算出应有水平</div></div>
                    <div class="bg-white p-3 rounded-lg text-center"><div class="font-black text-indigo-600 mb-1">③ 对标</div><div class="text-slate-500">实际表现与应有水平对比</div></div>
                    <div class="bg-white p-3 rounded-lg text-center"><div class="font-black text-indigo-600 mb-1">④ 归因</div><div class="text-slate-500">找出关键影响因素</div></div>
                  </div>
                </div>
              </section>

              <section>
                <h2 class="text-xl font-black text-slate-800 mb-4">适用场景与使用限制</h2>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div class="bg-emerald-50 p-4 rounded-xl border border-emerald-100">
                    <div class="text-xs font-bold text-emerald-700 mb-2">适合</div>
                    <ul class="text-xs text-emerald-800 space-y-1.5">
                      <li>• 多层级的组织效能公平评估</li>
                      <li>• 排除客观条件差异的比较排名</li>
                      <li>• 多因素综合影响分析</li>
                      <li>• 数据量 30-500 条效果最好</li>
                      <li>• "如果改变XX会怎样"的推演</li>
                    </ul>
                  </div>
                  <div class="bg-amber-50 p-4 rounded-xl border border-amber-100">
                    <div class="text-xs font-bold text-amber-700 mb-2">限制</div>
                    <ul class="text-xs text-amber-800 space-y-1.5">
                      <li>• 数据少于 10 条时结果不可靠</li>
                      <li>• 参与计算的列必须是数值</li>
                      <li>• 分析的是关联关系，不等同于因果关系</li>
                      <li>• 假设层级是嵌套的（上层包含下层）</li>
                      <li>• 极端离群值可能影响结果</li>
                    </ul>
                  </div>
                </div>
              </section>
            </div>

            <!-- Tab: 操作指南 -->
            <div v-if="activeTab === 'quickstart'" class="space-y-8 animate-fade-in max-w-4xl">
              <h2 class="text-xl font-black text-slate-800 mb-2">三步完成分析</h2>
              <p class="text-sm text-slate-500 mb-6">从数据到洞察只需三步，每步都有明确的目标。</p>

              <div class="flex"><div class="shrink-0 w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-black mr-5 mt-1">1</div>
                <div class="flex-1"><h3 class="font-black text-slate-800 mb-2">接入数据</h3>
                  <p class="text-sm text-slate-600 mb-3">上传 CSV、手动粘贴、或加载内置场景体验。第一行是列名，每行一个评估对象。</p>
              </div></div>

              <div class="flex"><div class="shrink-0 w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-black mr-5 mt-1">2</div>
                <div class="flex-1"><h3 class="font-black text-slate-800 mb-2">搭建网络</h3>
                  <p class="text-sm text-slate-600 mb-3">拖拽列名到对应位置：靶心放评估指标，层级放组织名称，协变量放影响因素。</p>
                  <div class="flex gap-3 text-xs">
                    <span class="bg-amber-100 text-amber-800 px-2 py-1 rounded font-bold">目标</span>
                    <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded font-bold">层级ID</span>
                    <span class="bg-emerald-100 text-emerald-800 px-2 py-1 rounded font-bold">影响因素</span>
                  </div>
              </div></div>

              <div class="flex"><div class="shrink-0 w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-black mr-5 mt-1">3</div>
                <div class="flex-1"><h3 class="font-black text-slate-800 mb-2">运行并查看结果</h3>
                  <p class="text-sm text-slate-600">点击「启动推演」，系统自动校验数据、运行分析。结果包括：效能偏差图、驱动力图、可信度验证、情景推演沙盘、决策研判中心。</p>
              </div></div>
            </div>

            <!-- Tab: 结果解读 -->
            <div v-if="activeTab === 'results'" class="space-y-8 animate-fade-in max-w-4xl">
              <h2 class="text-xl font-black text-slate-800 mb-6">如何读懂分析结果</h2>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><span class="text-emerald-500 mr-2">1.</span>模型可信度验证</h3>
                <p class="text-sm text-slate-600 mb-1"><strong>先看这个——确认分析是否靠谱。</strong></p>
                <p class="text-xs text-slate-500">深色线 = 真实数据，浅色带 = 模型推演范围。深色被浅色完全包裹 = 模型理解了业务规律。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><span class="text-indigo-500 mr-2">2.</span>效能偏差图</h3>
                <p class="text-sm text-slate-600 mb-1"><strong>回答：谁该表彰、谁要督战。</strong></p>
                <p class="text-xs text-slate-500">上方绿点 = 超出预期 | 下方红点 = 低于预期 | 中间灰点 = 正常。优先关注右下角的红点。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><span class="text-blue-500 mr-2">3.</span>关键驱动力图</h3>
                <p class="text-sm text-slate-600 mb-1"><strong>回答：资源投到哪里最划算。</strong></p>
                <p class="text-xs text-slate-500">线在零线右侧 = 越高越好 | 线在左侧 = 过高会拖累。右侧滑块可模拟"如果改变条件会怎样"。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><span class="text-amber-500 mr-2">4.</span>决策研判中心</h3>
                <p class="text-sm text-slate-600 mb-1"><strong>回答：现在应该做什么。</strong></p>
                <p class="text-xs text-slate-500">含优先级排序、行动建议、风险矩阵、一键简报。调参数后内容实时刷新。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><span class="text-emerald-500 mr-2">5.</span>导出报告</h3>
                <p class="text-sm text-slate-600 mb-1"><strong>回答：怎么带走分析结果。</strong></p>
                <p class="text-xs text-slate-500">点击「导出报告」生成结构化CSV文件，包含四部分：场景设定（层级、参数）、关键影响因素、逐对象详细结果（含解读和建议）、统计摘要。可用Excel直接打开。</p>
              </div>
            </div>

            <!-- Tab: 决策应用 -->
            <div v-if="activeTab === 'application'" class="space-y-6 animate-fade-in max-w-4xl">
              <h2 class="text-xl font-black text-slate-800 mb-6">如何应用到实际决策</h2>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><i class="fas fa-coins text-indigo-500 mr-2"></i>资源分配</h3>
                <p class="text-sm text-slate-600">看「关键驱动力图」找到影响力最大的因素，它就是资源投入的"最佳杠杆点"。再用「情景推演」模拟不同投入力度下的效果变化，找到最优区间。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><i class="fas fa-trophy text-emerald-500 mr-2"></i>绩效考核</h3>
                <p class="text-sm text-slate-600">看「优先级列表」中标记为"标杆"的对象。它们在同等条件下超预期，比简单按绝对数值排名更公平。简报中"经验推广"建议给出了具体的推广方向。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><i class="fas fa-search text-rose-500 mr-2"></i>问题整改</h3>
                <p class="text-sm text-slate-600">看「风险矩阵」中"高偏离+大影响"区的对象——最紧急。优先级列表中标记"紧急"的给出了具体排查方向。情景推演可模拟补救效果。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><i class="fas fa-file-alt text-blue-500 mr-2"></i>汇报沟通</h3>
                <p class="text-sm text-slate-600">「生成简报」可打印或复制，含场景设定、关键因素、优先级、建议。复制摘要可快速分享到工作群。</p>
              </div>

              <div class="border border-slate-200 rounded-2xl p-5">
                <h3 class="font-black text-slate-800 mb-2"><i class="fas fa-balance-scale text-purple-500 mr-2"></i>新项目预估（对标演算）</h3>
                <p class="text-sm text-slate-600">在结果页点击「对标演算」，输入新项目在各维度上的预期数值。系统会找到条件最相似的历史对象，用模型权重推算新项目的预期表现。输出包括：预期值、各因素贡献、雷达图对比、决策建议。</p>
              </div>
            </div>

            <!-- Tab: 内置场景 -->
            <div v-if="activeTab === 'scenarios'" class="space-y-6 animate-fade-in max-w-4xl">
              <h2 class="text-xl font-black text-slate-800 mb-6">内置行业场景说明</h2>
              <p class="text-sm text-slate-500 mb-6">每个场景都包含完整的层级、指标和因素。加载后自动搭建网络，您可以快速看到完整分析流程。</p>

              <div class="grid grid-cols-2 gap-4">
                <div v-for="scene in scenarioCards" :key="scene.id" class="border border-slate-200 rounded-2xl overflow-hidden hover:border-indigo-300 transition-colors">
                  <div class="px-5 py-3 border-b border-slate-100 font-black text-sm" :class="scene.headerClass">
                    <i :class="scene.icon + ' mr-2'"></i>{{ scene.title }}
                  </div>
                  <div class="p-4 space-y-2">
                    <p class="text-xs text-slate-600">{{ scene.desc }}</p>
                    <div class="text-[10px] text-slate-400 space-y-0.5">
                      <div><span class="font-bold text-slate-500">层级：</span>{{ scene.levels }}</div>
                      <div><span class="font-bold text-slate-500">目标：</span>{{ scene.target }}</div>
                      <div><span class="font-bold text-slate-500">因素：</span>{{ scene.factors }}</div>
                    </div>
                    <p class="text-[10px] text-indigo-500 mt-2">
                      <i class="fas fa-exchange-alt mr-1"></i>适配：将"{{ scene.adaptFrom }}"替换为您的对应列
                    </p>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        <div class="px-12 py-6 bg-slate-50 border-t border-slate-100 flex justify-end items-center shrink-0">
          <button @click="$emit('close')" class="px-8 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 active:scale-95 transition-all">开始使用</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue';
defineProps({ show: Boolean });
defineEmits(['close']);
const activeTab = ref('overview');
const tabs = [
  { id: 'overview', label: '系统概述与原理', icon: 'fas fa-lightbulb text-amber-500' },
  { id: 'quickstart', label: '操作指南', icon: 'fas fa-play text-emerald-500' },
  { id: 'results', label: '结果解读', icon: 'fas fa-chart-bar text-indigo-500' },
  { id: 'application', label: '决策应用', icon: 'fas fa-bullseye text-rose-500' },
  { id: 'scenarios', label: '内置场景说明', icon: 'fas fa-box-open text-blue-500' }
];
const scenarioCards = [
  { id:'public_security', title:'社会治理', headerClass:'bg-indigo-50 text-indigo-800', icon:'fas fa-shield-alt', desc:'省→市→分局三级警务效能评估。', levels:'省级 → 市局 → 分局', target:'综合打防转化率', factors:'经费投入、巡防密度、监控覆盖', adaptFrom:'综合打防转化率' },
  { id:'geopolitics', title:'地缘政治', headerClass:'bg-rose-50 text-rose-800', icon:'fas fa-globe-asia', desc:'联盟→战区→国家→城市四层地缘分析，含GPS坐标。', levels:'联盟 → 战区 → 国家 → 城市', target:'区域维稳指数', factors:'制裁压力、经济韧性、军事部署', adaptFrom:'区域维稳指数' },
  { id:'health', title:'公共卫生', headerClass:'bg-emerald-50 text-emerald-800', icon:'fas fa-heartbeat', desc:'全球大区→国家两层健康评估。', levels:'大区 → 国家', target:'重症致死率', factors:'人均医疗支出、床位数', adaptFrom:'重症致死率' },
  { id:'retail', title:'商业零售', headerClass:'bg-blue-50 text-blue-800', icon:'fas fa-store-alt', desc:'总部→大区→国家→城市四级零售网络。', levels:'总部 → 大区 → 国家 → 城市', target:'市场销量', factors:'广告预算、门店密度', adaptFrom:'市场销量' },
  { id:'coral_reef', title:'生态保护', headerClass:'bg-teal-50 text-teal-800', icon:'fas fa-tree', desc:'海洋区域→礁群→观测站三级生态评估。', levels:'区域 → 礁群 → 观测站', target:'珊瑚覆盖率', factors:'水温、污染指数', adaptFrom:'珊瑚覆盖率' },
  { id:'overseas_resilience', title:'海外利益', headerClass:'bg-slate-100 text-slate-800', icon:'fas fa-flag', desc:'大洲→国家→城市三级韧性评估。', levels:'大洲 → 国家 → 城市', target:'韧性指数', factors:'政治稳定度、经济依存度、安保投入', adaptFrom:'韧性指数' }
];
</script>

<style scoped>
.animate-scale-in { animation: scaleIn 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
.animate-fade-in { animation: fadeIn 0.45s ease-out; }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.96) translateY(20px); } to { opacity: 1; transform: scale(1) translateY(0); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 20px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }
</style>
