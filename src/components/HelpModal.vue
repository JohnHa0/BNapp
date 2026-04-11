<template>
  <transition name="fade">
    <div v-if="show" class="fixed inset-0 bg-slate-900/40 backdrop-blur-md flex justify-center items-center z-[100]" @click.self="$emit('close')">
      <div class="w-full max-w-6xl max-h-[92vh] bg-white rounded-3xl shadow-[0_40px_80px_-20px_rgba(0,0,0,0.25)] flex flex-col overflow-hidden animate-scale-in border border-slate-200">
        
        <!-- Header: Friendly yet Professional -->
        <div class="px-10 py-7 bg-white border-b border-slate-100 flex justify-between items-center shrink-0">
          <div class="flex items-center">
            <div class="w-14 h-14 rounded-2xl bg-indigo-600 flex items-center justify-center mr-6 shadow-xl shadow-indigo-100 relative overflow-hidden group">
               <div class="absolute inset-0 bg-gradient-to-tr from-indigo-600 to-indigo-400 group-hover:scale-110 transition-transform"></div>
               <i class="fas fa-magic text-2xl text-white relative z-10"></i>
            </div>
            <div>
              <h2 class="text-2xl font-black text-slate-900 tracking-tight flex items-center">
                欢迎开启 DeepBayes 智能推演之旅 <span class="ml-4 text-[10px] bg-emerald-50 text-emerald-600 px-3 py-1 rounded-full uppercase tracking-widest font-black border border-emerald-100">新手引航 v1.0.6</span>
              </h2>
              <p class="text-xs text-slate-500 mt-1.5 font-medium">无需敲代码，只需五分钟，让您的业务表格变身具有“预测未来的大脑”。</p>
            </div>
          </div>
          <button @click="$emit('close')" class="w-12 h-12 rounded-full bg-slate-50 hover:bg-slate-100 flex items-center justify-center transition-all duration-300 hover:rotate-90 text-slate-400 hover:text-slate-600">
            <i class="fas fa-times text-xl"></i>
          </button>
        </div>

        <!-- Main Content Area -->
        <div class="flex flex-1 overflow-hidden">
          
          <!-- Sidebar Navigation -->
          <div class="w-72 bg-slate-50 border-r border-slate-100 p-8 space-y-2 shrink-0">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-[0.25em] mb-6">操作导航目录</div>
            <button 
              v-for="tab in tabs" :key="tab.id"
              @click="activeTab = tab.id"
              :class="activeTab === tab.id ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-100' : 'text-slate-500 hover:bg-slate-200 hover:translate-x-1'"
              class="w-full text-left px-5 py-4 rounded-2xl text-[13px] font-bold transition-all flex items-center group mb-2"
            >
              <i :class="tab.icon" class="mr-4 w-5 text-center transition-transform group-hover:scale-110"></i>
              {{ tab.label }}
            </button>
            
            <div class="mt-auto pt-12">
               <div class="p-5 bg-blue-50 rounded-2xl border border-blue-100 cursor-default">
                  <div class="text-[11px] text-blue-800 font-bold mb-1 flex items-center">
                    <i class="fas fa-lightbulb text-amber-500 mr-2 animate-pulse"></i> 核心思想提示
                  </div>
                  <p class="text-[10px] text-blue-600 leading-relaxed">不必害怕复杂的图表。<strong class="font-black">您的主要工作就是告诉系统：谁归谁管，并且评估的标准是什么。</strong> 剩下的数学难题全部交给 DeepBayes 后台处理。</p>
               </div>
            </div>
          </div>

          <!-- Documentation Body -->
          <div class="flex-1 overflow-y-auto p-12 custom-scrollbar bg-white selection:bg-indigo-100">
            
            <!-- Tab: Highlights (Why DeepBayes) -->
            <div v-if="activeTab === 'highlights'" class="space-y-12 animate-fade-in">
              <section>
                <h1 class="text-3xl font-black text-slate-900 mb-6">超越表格，洞悉因果。</h1>
                <p class="text-slate-600 leading-relaxed max-w-3xl text-sm mb-10">
                   您可能已经习惯了用 Excel 画柱状图，或是看传统大屏展示“过去发生了什么”。
                   <strong class="text-indigo-600">DeepBayes 则不同，它不仅能告诉您现在，更能为您预演未来。</strong> 它是专为解决“多层级管理组织”（比如：总部负责片区，片区下面有分局）痛点设计的推演沙盘。
                </p>

                <div class="grid grid-cols-1 gap-6">
                   <!-- Highlight 1 -->
                   <div class="flex items-start bg-slate-50 p-6 rounded-3xl border border-slate-100">
                      <div class="flex-shrink-0 w-16 h-16 bg-white rounded-2xl flex items-center justify-center mr-6 shadow-sm border border-slate-200">
                         <i class="fas fa-project-diagram text-2xl text-indigo-500"></i>
                      </div>
                      <div>
                         <h3 class="text-lg font-black text-slate-800 mb-2">亮点一：像搭积木一样，零代码描绘业务层级</h3>
                         <p class="text-xs text-slate-600 leading-relaxed">
                           就算毫无编程经验也没有关系。只要您的表格里有组织架构的名字（如：全球、地区、城市），您只需要用鼠标将它们<strong class="text-slate-900">“拽”</strong>到画布上，系统就会自动搭建出严密的从上到下的业务影响关系网（系统内部叫做有向无环图 DAG）。
                         </p>
                      </div>
                   </div>

                   <!-- Highlight 2 -->
                   <div class="flex items-start bg-emerald-50 p-6 rounded-3xl border border-emerald-100">
                      <div class="flex-shrink-0 w-16 h-16 bg-white rounded-2xl flex items-center justify-center mr-6 shadow-sm border border-emerald-200">
                         <i class="fas fa-compress-arrows-alt text-2xl text-emerald-500"></i>
                      </div>
                      <div>
                         <h3 class="text-lg font-black text-emerald-900 mb-2">亮点二：“小节点”抗压法宝（贝叶斯修正网络）</h3>
                         <p class="text-xs text-emerald-800 leading-relaxed opacity-90">
                           有些基层分局刚挂牌，能评估的数据少得可怜，用普通统计去算是偏颇的。DeepBayes 采用了一种叫<strong class="text-emerald-900 border-b border-emerald-900">层次贝叶斯收缩</strong>的技术：当一个小局数据不够时，系统会自动“借调”整个市局甚至是全国大盘的经验数据来修正它，确保推断结果不被极端偶然性拖垮。
                         </p>
                      </div>
                   </div>

                   <!-- Highlight 3 -->
                   <div class="flex items-start bg-indigo-900 p-6 rounded-3xl shadow-xl shadow-indigo-900/20 text-white relative overflow-hidden">
                      <div class="absolute right-0 top-0 w-64 h-64 bg-indigo-500 rounded-full mix-blend-screen opacity-20 blur-3xl transform translate-x-1/2 -translate-y-1/2"></div>
                      <div class="flex-shrink-0 w-16 h-16 bg-indigo-800 rounded-2xl flex items-center justify-center mr-6 shadow-inner border border-indigo-700 relative z-10">
                         <i class="fas fa-bolt text-2xl text-amber-400"></i>
                      </div>
                      <div class="relative z-10">
                         <h3 class="text-lg font-black text-white mb-2">亮点三：一键释放“平行宇宙”灾难模拟测试</h3>
                         <p class="text-xs text-indigo-200 leading-relaxed">
                           算完了基础报告还不够。系统里有一个叫做 <strong class="text-white">“冲击响应分析”</strong> 的超级按钮！点下去，系统会假设全盘资金或环境因素瞬间跌入谷底（最坏情况），并在几秒钟内推算出：在这样一场风暴中，谁会粉身碎骨，到底哪个据点才是您最坚如磐石的核心资产。
                         </p>
                      </div>
                   </div>
                </div>
              </section>
            </div>

            <!-- Tab: Step-by-step Quickstart -->
            <div v-if="activeTab === 'quickstart'" class="space-y-10 animate-fade-in">
              <section>
                 <div class="flex items-center gap-4 mb-8">
                   <h2 class="text-2xl font-black text-slate-800 tracking-tight">🎯 保姆级实操指导：让你的数据跑起来</h2>
                 </div>

                 <!-- Step 1 -->
                 <div class="mb-8">
                   <div class="flex items-center mb-3">
                     <div class="w-8 h-8 rounded-full bg-slate-900 text-white flex justify-center items-center font-black mr-3 shadow">1</div>
                     <h3 class="text-lg font-bold text-slate-800">打理您的源数据 (准备 Excel/CSV)</h3>
                   </div>
                   <div class="ml-11 bg-slate-50 p-5 rounded-2xl border border-slate-200">
                     <p class="text-[12px] text-slate-600 mb-3">系统支持上传 CSV 逗号分隔的宽表格式，您的表格必须遵守这几个简单的规矩：</p>
                     <ul class="text-[12px] text-slate-700 space-y-2 list-disc pl-5 font-medium">
                       <li><strong class="text-indigo-600">第一行必须全都是标题</strong>（比如：省份、城市、资金投入、绩效得分）。</li>
                       <li><strong class="text-indigo-600">必须有一个“目标列 (Y)”</strong>，必须全是数字，它是您最后想评估的那个大结果。不能有空着的格子！</li>
                       <li><strong class="text-indigo-600">如果想用地图</strong>，必须包含名为“经度坐标”和“纬度坐标”的两列数字。</li>
                       <li><strong class="text-indigo-600">您可以下载样例模板或者预置行业数据查看数据结构格式。</li>
                     </ul>
                   </div>
                 </div>

                 <!-- Step 2 -->
                 <div class="mb-8">
                   <div class="flex items-center mb-3">
                     <div class="w-8 h-8 rounded-full bg-slate-900 text-white flex justify-center items-center font-black mr-3 shadow">2</div>
                     <h3 class="text-lg font-bold text-slate-800">将字段“拖”入系统 (拖拽操作)</h3>
                   </div>
                   <div class="ml-11 border border-slate-200 rounded-3xl p-6 shadow-sm overflow-hidden flex divide-x divide-slate-100">
                      <div class="w-1/2 pr-6">
                         <p class="text-[12px] text-slate-600 mb-4 leading-relaxed">
                            进入主页面后，您的表格列名会全部出现在左侧的**“数据要素池”**中。用鼠标按住它们不松开，然后拖拽到右侧的坑位里：
                         </p>
                         <div class="space-y-4">
                            <div class="flex items-center text-xs">
                               <div class="w-20 font-black text-amber-600 bg-amber-50 px-2 py-1 rounded text-center mr-3">观测靶点</div>
                               <div class="text-slate-500">🏆 拖入您要评估的终极绩效得分，只能拖一个。</div>
                            </div>
                            <div class="flex items-center text-xs">
                               <div class="w-20 font-black text-blue-600 bg-blue-50 px-2 py-1 rounded text-center mr-3">节点标识</div>
                               <div class="text-slate-500">🏢 拖入该层级的名字（比如省厅、警局等）。</div>
                            </div>
                            <div class="flex items-center text-xs">
                               <div class="w-20 font-black text-emerald-600 bg-emerald-50 px-2 py-1 rounded text-center mr-3">协变量 X</div>
                               <div class="text-slate-500">🌧️ 拖入客观影响条件（如：本地GDP水平、警力投入度）。可以放好几个。</div>
                            </div>
                         </div>
                      </div>
                      <div class="w-1/2 pl-6 bg-slate-50 flex items-center justify-center">
                         <!-- Visual representation of drag -->
                         <div class="text-center">
                            <div class="p-2 bg-white border border-slate-300 rounded shadow-sm text-[10px] font-bold text-slate-600 inline-block rotate-3 transform translate-y-2 cursor-grab">
                               <i class="fas fa-grip-vertical text-slate-300 mr-2"></i>资金投入列
                            </div>
                            <i class="fas fa-arrow-down text-indigo-300 text-lg block my-3"></i>
                            <div class="p-4 border-2 border-dashed border-emerald-300 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-lg opacity-80">
                               放入协变量框中
                            </div>
                         </div>
                      </div>
                   </div>
                 </div>

                 <!-- Step 3 -->
                 <div class="mb-8">
                   <div class="flex items-center mb-3">
                     <div class="w-8 h-8 rounded-full bg-slate-900 text-white flex justify-center items-center font-black mr-3 shadow">3</div>
                     <h3 class="text-lg font-bold text-slate-800">搭建多层级“大厦”并修改好看的名字</h3>
                   </div>
                   <div class="ml-11 grid grid-cols-2 gap-6 leading-relaxed">
                      <div class="bg-indigo-50 p-5 rounded-2xl border border-indigo-100">
                         <div class="text-[11px] font-bold text-indigo-800 mb-2"><i class="fas fa-layer-group mr-2"></i> 增加层级</div>
                         <p class="text-[11px] text-indigo-700">点击右下方巨大的框框**“添加下一级网络节点”**。您可以把省设为L1，市设为L2，区局设为L3。这就是“网络拓扑”！</p>
                      </div>
                      <div class="bg-indigo-50 p-5 rounded-2xl border border-indigo-100">
                         <div class="text-[11px] font-bold text-indigo-800 mb-2"><i class="fas fa-edit mr-2"></i> 改个别人看得懂的名称</div>
                         <p class="text-[11px] text-indigo-700">觉得原始列名太丑？将鼠标悬停在要素上的铅笔小图标，或在生成图表后双击标题即可重命名，<strong class="text-indigo-900">这完全安全，绝不会改变原始数据的内核！</strong></p>
                      </div>
                   </div>
                 </div>

                 <!-- Step 4 -->
                 <div>
                   <div class="flex items-center mb-3">
                     <div class="w-8 h-8 rounded-full bg-slate-900 text-white flex justify-center items-center font-black mr-3 shadow">4</div>
                     <h3 class="text-lg font-bold text-slate-800">点击绿色引擎按钮启动大盘推演！</h3>
                   </div>
                   <div class="ml-11">
                      <p class="text-[12px] text-slate-600 mb-3">当所有层级都塞满后，点击右上方绿色的 **“执行数据体检与推演”** 按钮即可拔锚起航。</p>
                      <div class="p-3 bg-amber-50 border-l-4 border-amber-500 rounded-r text-[11px] text-amber-800">
                        <strong class="font-black"><i class="fas fa-exclamation-triangle mr-1"></i> 不要慌：等待期间卡在 88% 是正常现象。</strong>
                        <br/>那一刻系统正在进行最高难度的 R-hat 收敛性收尾检查，确保交出的预测不再有统计层面的偏差。大约会耗时 10~30秒，您可以借此时间泡杯咖啡。
                      </div>
                   </div>
                 </div>

              </section>
            </div>

            <!-- Tab: Read Reports & What-If -->
            <div v-if="activeTab === 'reports'" class="space-y-12 animate-fade-in">
              <section class="max-w-4xl">
                 <h2 class="text-2xl font-black text-slate-800 mb-8 border-b border-slate-100 pb-4">怎么看懂出来的天书图表？以及如何把玩沙盘？</h2>
                 
                 <!-- Q&A 1 -->
                 <div class="mb-8 p-6 bg-slate-50 border border-slate-200 rounded-3xl relative">
                    <div class="absolute -left-3 top-6 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center font-black text-xs">Q</div>
                    <h3 class="text-sm font-black text-slate-800 mb-3 ml-4">左侧的“散点图”和“地图像素点”代表什么？</h3>
                    <div class="ml-4 text-xs text-slate-600 leading-relaxed space-y-2">
                       <p><strong class="text-slate-900">答案：</strong> 它们都在向您控诉系统的“偏私现象”：</p>
                       <p>✅ <strong class="text-emerald-600 bg-emerald-50 px-1">偏青色/绿色的点与块</strong>，代表这些机构表现非凡！在排除大环境优势后，它自身的业务能力实打实地超越了系统期望。</p>
                       <p>❌ <strong class="text-rose-600 bg-rose-50 px-1">偏红色/粉色的点与块</strong>，是重点督办对象！在同样条件配给下，结果跌破期望。点一下它们，不仅能看它缺什么，还能借此发现整个结构的软肋。</p>
                    </div>
                 </div>

                 <!-- Q&A 2 -->
                 <div class="mb-10 p-6 bg-slate-50 border border-slate-200 rounded-3xl relative">
                    <div class="absolute -left-3 top-6 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center font-black text-xs">Q</div>
                    <h3 class="text-sm font-black text-slate-800 mb-3 ml-4">那张有很多蓝色和绿色曲线交织的图 (后验验证) 是用来干什么呢？</h3>
                    <div class="ml-4 text-xs text-slate-600 leading-relaxed">
                       <p><strong class="text-slate-900">答案：</strong> 它是帮您验证“这次建模靠不靠谱”的检验金标准 <span class="font-mono bg-slate-200 px-1 rounded">(PPC)</span>。</p>
                       <p class="mt-2">系统会给出一个带有几条浅蓝色阴影带的曲线 (这是系统的各种预判可能)，和一根翠绿色的粗曲线 (这是绝对真实的成绩单)。**只要这条绿曲线被安全地裹在蓝带子里，您就可以放心大胆地拿着这份报告在大会上宣读** —— 这意味着模型完全掌握了数据的底层规律节奏。</p>
                    </div>
                 </div>

                 <div class="mb-8">
                     <h3 class="text-lg font-black text-slate-800 mb-4 flex items-center">
                        <i class="fas fa-meteor text-rose-500 mr-3"></i> 刺激的重头戏：灾难按钮怎么按？
                     </h3>
                     <p class="text-xs text-slate-600 mb-6">切换到右侧第三个 **[冲击分析选项卡]**。深呼吸，您可以亲手发动一次金融危机式海啸：</p>
                     
                     <div class="grid grid-cols-2 gap-6">
                        <div class="p-6 bg-rose-50 border border-rose-200 rounded-2xl">
                           <div class="font-black text-rose-700 text-sm mb-2">🔥 全环境级联坍塌演习</div>
                           <p class="text-[11px] text-rose-800/80 leading-relaxed">
                              这是终极压力测试。点击后，所有的条件变量将瞬间触底 (-3 标准差)。不用看谁跌的猛，系统将自动帮您筛选出在一地残骸中 <strong class="font-black border-b border-rose-800">依然保持正增长的“扛压英雄”资产标的。</strong>
                           </p>
                        </div>
                        <div class="p-6 bg-slate-900 text-white rounded-2xl shadow-xl shadow-slate-900/20">
                           <div class="font-black text-cyan-400 text-sm mb-2 flex items-center"><i class="fas fa-robot mr-2"></i> AI 将立刻上岗指挥</div>
                           <p class="text-[11px] text-slate-300 leading-relaxed">
                              当按下红色按钮，地图右侧面板将瞬间弹出 **AI 大脑决断室**。不管您懂不懂数据，用不了一秒，AI 就会用最干练、最毒辣的业务词藻，告诉您当下最该抢救哪里的局势！
                           </p>
                        </div>
                     </div>
                 </div>

              </section>
            </div>

            <!-- Tab: Demos & Scenarios -->
            <div v-if="activeTab === 'demos'" class="space-y-12 animate-fade-in">
                <section>
                   <div class="flex items-center gap-4 mb-8">
                       <h2 class="text-2xl font-black text-slate-800 tracking-tight">📦 还没准备好自己的数据？先玩沙盘体会魅力。</h2>
                   </div>
                   <p class="text-sm text-slate-500 mb-8 font-medium">在“数据导入”看板的最上方有个下拉菜单，里面有精心准备好的业务演练场。一键载入后，它会自动拼装并运行所有推演逻辑。</p>

                   <div class="grid grid-cols-2 gap-6">
                       <!-- Demo Card -->
                       <div class="border border-slate-200 rounded-2xl overflow-hidden group hover:border-indigo-400 transition-colors">
                           <div class="bg-indigo-50 px-5 py-3 border-b border-slate-200">
                               <h4 class="font-black text-indigo-800 text-sm flex items-center"><i class="fas fa-shield-alt mr-2 text-indigo-500"></i>社会治理效能评估沙盘</h4>
                           </div>
                           <div class="p-5 bg-white text-xs text-slate-600 leading-relaxed h-[110px]">
                               体验从“省 -> 市局 -> 基层单位”的一张张大网结。重点看“加派巡逻警力”或者“削减布控预算”究竟会不会产生发案率爆表的连锁灾难反馈。
                           </div>
                       </div>
                       <!-- Demo Card -->
                       <div class="border border-slate-200 rounded-2xl overflow-hidden group hover:border-rose-400 transition-colors">
                           <div class="bg-rose-50 px-5 py-3 border-b border-slate-200">
                               <h4 class="font-black text-rose-800 text-sm flex items-center"><i class="fas fa-globe-asia mr-2 text-rose-500"></i>地缘冲突级联演化地图</h4>
                           </div>
                           <div class="p-5 bg-white text-xs text-slate-600 leading-relaxed h-[110px]">
                               这是张自带经纬度雷达投影的战略版图。按一下“全域坍塌”灾难演习，去查探万一遭到极端经济制裁绞杀，究竟哪个阵营会第一个在地图上粉碎溃落。
                           </div>
                       </div>
                       <!-- Demo Card -->
                       <div class="border border-slate-200 rounded-2xl overflow-hidden group hover:border-emerald-400 transition-colors">
                           <div class="bg-emerald-50 px-5 py-3 border-b border-slate-200">
                               <h4 class="font-black text-emerald-800 text-sm flex items-center"><i class="fas fa-store-alt mr-2 text-emerald-500"></i>跨国商业下沉零售测算</h4>
                           </div>
                           <div class="p-5 bg-white text-xs text-slate-600 leading-relaxed h-[110px]">
                               以跨国零售巨头为原型设计。用来推算“缩减公关预算的同时，对下沉市场的竞品进行高强度掠夺打击”，是否能带来总利润额的惊险回春！
                           </div>
                       </div>
                       <!-- Demo Card -->
                       <div class="border border-slate-200 rounded-2xl overflow-hidden flex flex-col justify-center items-center h-[160px] bg-slate-50 cursor-pointer hover:bg-slate-100 transition-colors">
                           <div class="text-4xl text-slate-300 mb-2">+</div>
                           <div class="text-xs font-bold text-slate-600">下拉列表查看更多隐藏关卡...</div>
                       </div>
                   </div>
                </section>
            </div>

          </div>
        </div>

        <!-- Sticky Status Footer -->
        <div class="px-12 py-7 bg-slate-50 border-t border-slate-100 flex justify-end items-center shrink-0">
          <div class="flex gap-4">
             <button @click="$emit('close')" class="px-10 py-3 bg-white border border-slate-300 text-slate-600 shadow-sm text-sm font-bold rounded-xl hover:bg-slate-100 hover:text-slate-800 transition-all font-mono">
               下次再看
             </button>
             <button @click="$emit('close')" class="px-10 py-3 bg-indigo-600 text-white text-sm font-bold rounded-xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 active:scale-95 transition-all flex items-center group">
               我完全明白了，立刻开启操作！
               <i class="fas fa-arrow-right ml-3 group-hover:translate-x-1 transition-transform"></i>
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
  { id: 'highlights', label: '1. 系统亮点与价值', icon: 'fas fa-star text-amber-500' },
  { id: 'quickstart', label: '2. 五步零基础实操', icon: 'fas fa-route text-emerald-500' },
  { id: 'reports', label: '3. 读懂报告与沙盘推演', icon: 'fas fa-chart-pie text-indigo-500' },
  { id: 'demos', label: '4. 内置沙盒推演体验', icon: 'fas fa-box-open text-rose-500' }
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
