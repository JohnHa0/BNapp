<template>
  <div class="h-full bg-ice-white p-6 pb-20" @dragover.prevent="onRootDragOver" @drop.prevent>
    <div class="max-w-7xl mx-auto space-y-6">
      <!-- 页面标题 -->
      <div class="mb-5">
        <h1 class="text-xl font-extrabold text-slate-900 tracking-tight">数据接入</h1>
        <p class="text-sm text-slate-500 mt-1">上传业务数据或加载内置场景，拖拽列名搭建分析网络</p>
      </div>
      
      <!-- 操作栏 -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
        <div class="flex flex-wrap items-center gap-3">
          <!-- 场景加载组 -->
          <div class="flex items-center gap-2.5 px-4 py-2.5 bg-slate-50 rounded-xl border border-slate-200 hover:border-indigo-200 transition-colors">
            <i class="fas fa-magic text-indigo-500"></i>
            <select v-model="selectedDemo" @change="loadDemo" class="bg-transparent text-slate-700 text-sm font-medium outline-none cursor-pointer min-w-[220px]">
              <option value="">加载行业场景模板...</option>
              <option value="public_security">社会治理 · 三级警务效能</option>
              <option value="geopolitics">地缘政治 · 四层博弈沙盘</option>
              <option value="health">公共卫生 · 重症致死率归因</option>
              <option value="retail">商业零售 · 跨国销量推演</option>
              <option value="coral_reef">生态保护 · 珊瑚礁观测网</option>
              <option value="overseas_resilience">战略规划 · 海外利益韧性</option>
            </select>
          </div>
          
          <div class="w-px h-8 bg-slate-200"></div>
          
          <!-- 数据来源组 -->
          <button @click="showManualInput = true" class="px-4 py-2.5 text-sm font-medium text-slate-600 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl transition-colors flex items-center gap-2">
            <i class="fas fa-keyboard text-slate-400"></i>手动输入
          </button>
          <button @click="downloadSampleCSV" class="px-4 py-2.5 text-sm font-medium text-slate-600 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl transition-colors flex items-center gap-2">
            <i class="fas fa-download text-slate-400"></i>模板下载
          </button>
          <label class="px-5 py-2.5 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl cursor-pointer transition-colors shadow-lg shadow-indigo-500/20 flex items-center gap-2">
            <i class="fas fa-cloud-upload-alt"></i>上传 CSV
            <input type="file" class="hidden" accept=".csv" @change="handleFileUpload" />
          </label>
        </div>
      </div>

      <!-- 预设场景深度说明面板 -->
      <div v-if="selectedDemo && currentPresetInfo" class="bg-white border border-indigo-200 rounded-xl shadow-sm overflow-hidden">
        <!-- 标题栏 -->
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-500 px-5 py-3 flex justify-between items-center">
          <h3 class="text-sm font-black text-white flex items-center gap-2">
            <i class="fas fa-cube"></i>{{ currentPresetInfo.title }}
          </h3>
          <button @click="selectedDemo = ''; currentPresetInfo = null" class="text-indigo-200 hover:text-white transition-colors">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="p-5 space-y-4">
          <!-- 业务描述 -->
          <p class="text-sm text-slate-600 leading-relaxed">{{ currentPresetInfo.description }}</p>
          
          <!-- 三栏：结构 + 因子 + 原理 -->
          <div class="grid grid-cols-3 gap-4">
            <!-- 左：网络结构 -->
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
              <div class="text-[11px] font-black text-slate-700 mb-3 flex items-center gap-2">
                <i class="fas fa-project-diagram text-indigo-500"></i>网络结构
              </div>
              <div class="space-y-2">
                <div v-for="(lvl, i) in currentPresetInfo.hierarchy" :key="i">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="w-5 h-5 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-[9px] font-black">L{{ i + 1 }}</span>
                    <span class="text-xs font-bold text-slate-700">{{ lvl.name }}</span>
                  </div>
                  <div class="ml-7 text-[10px] text-slate-500 mb-1">ID列：{{ lvl.idDesc }}</div>
                  <div v-if="i < currentPresetInfo.hierarchy.length - 1" class="ml-2 border-l-2 border-dashed border-indigo-200 h-4"></div>
                </div>
              </div>
              <div class="mt-3 pt-3 border-t border-dashed border-slate-200 text-[10px] text-slate-400">
                上层节点的变化会自动影响下层所有节点——这就是"层级嵌套"模型的核心。
              </div>
            </div>
            
            <!-- 中：评估因子 -->
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
              <div class="text-[11px] font-black text-slate-700 mb-3 flex items-center gap-2">
                <i class="fas fa-crosshairs text-amber-500"></i>评估因子
              </div>
              <div class="space-y-2">
                <div class="flex items-center gap-2 text-xs">
                  <span class="w-2 h-2 rounded-full bg-amber-400 shrink-0"></span>
                  <span class="font-bold text-slate-700">目标：</span>
                  <span class="text-slate-600">{{ currentPresetInfo.targetDesc }}</span>
                </div>
                <div class="text-[9px] text-slate-400 ml-4 mb-2">系统将排除客观条件差异，计算每个节点的"净贡献"</div>
                <div v-for="(cov, i) in currentPresetInfo.covariates" :key="i" class="flex items-start gap-2 text-xs">
                  <span class="w-2 h-2 rounded-full bg-blue-400 shrink-0 mt-1"></span>
                  <div>
                    <span class="font-bold text-slate-700">{{ cov.name }}</span>
                    <span class="text-slate-500 ml-1">— {{ cov.desc }}</span>
                  </div>
                </div>
              </div>
              <div class="mt-3 pt-3 border-t border-dashed border-slate-200 text-[10px] text-slate-400">
                系统会量化每个因素对目标的影响力（β值），找到最关键的因素。
              </div>
            </div>
            
            <!-- 右：计算原理 -->
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
              <div class="text-[11px] font-black text-slate-700 mb-3 flex items-center gap-2">
                <i class="fas fa-calculator text-emerald-500"></i>计算原理
              </div>
              <div class="space-y-2 text-[10px] text-slate-600 leading-relaxed">
                <div class="bg-white rounded-lg p-2 border border-slate-100">
                  <span class="font-bold text-indigo-600">① 标准化</span>
                  <p class="text-slate-500 mt-0.5">将所有数值转换为统一尺度（Z-score），消除量纲差异</p>
                </div>
                <div class="bg-white rounded-lg p-2 border border-slate-100">
                  <span class="font-bold text-indigo-600">② 层次建模</span>
                  <p class="text-slate-500 mt-0.5">按您设定的层级自动抓取嵌套关系（如：同一省下的市具有关联性）</p>
                </div>
                <div class="bg-white rounded-lg p-2 border border-slate-100">
                  <span class="font-bold text-indigo-600">③ MCMC采样</span>
                  <p class="text-slate-500 mt-0.5">运行数千次模拟推演，算出每个因素的β权重和置信区间</p>
                </div>
                <div class="bg-white rounded-lg p-2 border border-slate-100">
                  <span class="font-bold text-indigo-600">④ 偏差计算</span>
                  <p class="text-slate-500 mt-0.5">实际值 − 模型预期值 = 净贡献。正数 = 超预期，负数 = 需关注</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 适配提示 -->
          <div class="bg-amber-50 border border-amber-200 rounded-lg p-3 flex items-start gap-2">
            <i class="fas fa-exchange-alt text-amber-500 mt-0.5"></i>
            <div class="text-xs">
              <span class="font-bold text-amber-800">如何适配到您的数据：</span>
              <span class="text-amber-700">保持层级关系不变，将列名替换为您的对应列。例如将「{{ currentPresetInfo.adaptExample.from }}」替换为「{{ currentPresetInfo.adaptExample.to }}」，将各层级ID列替换为您的组织名称列。</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Layout -->
      <div v-if="columns.length > 0" class="flex gap-6 items-start">
        
        <!-- Left: Unassigned Columns -->
        <div class="w-1/3 bg-white rounded-xl shadow-sm border border-slate-200">
          <div class="p-4 border-b border-slate-200 bg-slate-50 rounded-t-xl flex justify-between items-center">
            <h2 class="font-bold text-slate-700"><i class="fas fa-database mr-2 text-slate-400"></i> 待分配数据列</h2>
            <span class="bg-slate-200 text-slate-600 text-xs px-2 py-0.5 rounded-full font-bold">{{ unassignedColumns.length }}</span>
          </div>
          
          <div 
            class="p-4 min-h-[500px] max-h-[700px] overflow-y-auto space-y-3 bg-white"
            @dragover="onDragOver"
            @dragenter.prevent
            @drop="onDropUnassigned"
          >
            <!-- Draggable items -->
            <div 
              v-for="col in unassignedColumns" 
              :key="col.id"
              draggable="true"
              @dragstart="onDragStart($event, col, 'unassigned', null, null)"
              class="group relative p-3 bg-white border border-slate-200 rounded-lg cursor-grab active:cursor-grabbing hover:border-indigo-400 hover:shadow-md transition-all flex items-center shadow-sm"
            >
              <i class="fas fa-grip-vertical text-slate-300 mr-3 group-hover:text-indigo-400"></i>
              <div class="flex-1">
                <div class="font-semibold text-slate-700 text-sm truncate" :title="col.original">{{ col.alias || col.original }}</div>
                <div class="text-xs text-slate-400 font-mono tracking-tight mt-0.5">{{ col.original !== col.alias ? '源: '+col.original : 'Type: Auto' }}</div>
              </div>
              <button @click.prevent="editAlias(col)" class="text-slate-300 hover:text-indigo-600 p-1 opacity-0 group-hover:opacity-100 transition-opacity" title="重命名别名">
                <i class="fas fa-pencil-alt text-xs"></i>
              </button>
            </div>
            
            <div v-if="unassignedColumns.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 pt-20 pb-10">
              <div class="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mb-3">
                <i class="fas fa-check text-2xl text-emerald-400"></i>
              </div>
              <span class="text-sm font-medium">所有要素均已映射完毕</span>
            </div>
          </div>
        </div>

        <!-- Right: Network Topology Builder -->
        <div class="w-2/3 space-y-4">
          
          <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex justify-between items-center group relative">
            <div>
              <h2 class="font-bold text-slate-700"><i class="fas fa-project-diagram mr-2 text-indigo-500"></i> N 维贝叶斯拓扑构建器 (N-Level Builder)</h2>
              <p class="text-[11px] text-slate-400 mt-1">新手必读：至少需要一层网络。Y=最终结果；ID=地点/人；X=影响因素。</p>
            </div>
            
            <div class="flex items-center space-x-4">
               <div class="relative group/tip">
                 <div class="flex items-center text-xs text-slate-500 bg-slate-50 p-1.5 rounded-lg border border-slate-200 cursor-default">
                    <span :class="{'font-bold text-indigo-600': samplingMode === 'accurate', 'text-slate-400 cursor-pointer hover:text-slate-600': samplingMode === 'fast'}" @click="samplingMode = 'accurate'; customDraws = 1500; customTune = 1000;">精确模式</span>
                    <div class="w-9 h-[18px] bg-slate-200 mx-2 rounded-full relative cursor-pointer" @click="toggleSamplingMode">
                       <div class="absolute top-[3px] w-3 h-3 rounded-full transition-all shadow" :class="samplingMode === 'fast' ? 'bg-amber-500 right-[3px]' : 'bg-indigo-600 left-[3px]'"></div>
                    </div>
                    <span :class="{'font-bold text-amber-600': samplingMode === 'fast', 'text-slate-400 cursor-pointer hover:text-slate-600': samplingMode === 'accurate'}" @click="samplingMode = 'fast'; customDraws = 500; customTune = 300;">快速预览 <i class="fas fa-bolt ml-0.5"></i></span>
                 </div>
                 <!-- Tooltip -->
                 <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-72 bg-slate-800 text-white text-[11px] p-3 rounded-lg shadow-xl opacity-0 group-hover/tip:opacity-100 transition-opacity pointer-events-none z-50">
                    <div class="font-bold mb-1"><i class="fas fa-info-circle mr-1 text-neon-cyan"></i> 采样模式说明</div>
                    <p><strong class="text-amber-400">快速预览</strong>: Draws=500, Tune=300。适合快速验证模型结构是否合理 (~5秒)。</p>
                    <p class="mt-1"><strong class="text-indigo-300">精确模式</strong>: Draws=1500, Tune=1000。生成学术级可信后验分布 (~20秒)。</p>
                    <div class="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-[6px] border-r-[6px] border-t-[6px] border-l-transparent border-r-transparent border-t-slate-800"></div>
                 </div>
               </div>

               <!-- 高级参数展开 -->
               <button @click="showAdvancedSampling = !showAdvancedSampling" class="text-xs text-slate-400 hover:text-indigo-600 transition-colors" :title="showAdvancedSampling ? '收起高级参数' : '展开自定义采样参数'">
                 <i :class="showAdvancedSampling ? 'fas fa-chevron-up' : 'fas fa-cog'"></i>
               </button>
               
               <button @click="proceedToHealthCheck" class="px-5 py-2.5 text-sm font-bold text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors shadow-sm shadow-emerald-600/30 flex items-center group-hover:shadow-lg">
                 <i class="fas fa-play mr-2"></i>执行数据体检与推演
               </button>
            </div>
          </div>

          <!-- 高级采样参数面板 -->
          <div v-if="showAdvancedSampling" class="bg-indigo-50/60 p-4 rounded-xl border border-indigo-200 shadow-sm">
            <h4 class="text-xs font-bold text-indigo-700 mb-3 flex items-center"><i class="fas fa-sliders-h mr-2"></i>高级 MCMC 采样参数 (仅限专业用户)</h4>
            <div class="flex gap-4 items-end">
              <div class="flex-1">
                <label class="block text-[11px] font-bold text-slate-500 mb-1">Draws (后验抽样次数)</label>
                <input type="number" v-model.number="customDraws" min="100" max="10000" step="100" class="w-full bg-white border border-indigo-200 rounded-lg px-3 py-2 text-sm font-mono text-slate-700 focus:ring-2 focus:ring-indigo-400 focus:outline-none" />
              </div>
              <div class="flex-1">
                <label class="block text-[11px] font-bold text-slate-500 mb-1">Tune (预热调优次数)</label>
                <input type="number" v-model.number="customTune" min="100" max="5000" step="100" class="w-full bg-white border border-indigo-200 rounded-lg px-3 py-2 text-sm font-mono text-slate-700 focus:ring-2 focus:ring-indigo-400 focus:outline-none" />
              </div>
              <div class="text-[10px] text-slate-400 pb-2 flex-shrink-0">总迭代: {{ (customDraws + customTune) * 4 }} 次</div>
            </div>
          </div>

          <!-- Target Variable Area -->
          <div class="bg-gradient-to-br from-amber-50 to-orange-50 p-5 rounded-xl border border-amber-200 shadow-sm relative overflow-hidden">
            <div class="absolute right-0 top-0 w-32 h-32 bg-amber-500/10 rounded-full blur-2xl transform translate-x-1/2 -translate-y-1/2"></div>
            <h3 class="text-sm font-bold text-amber-900 mb-3 flex items-center">
              <i class="fas fa-bullseye text-amber-500 mr-2"></i> 评估目标（核心KPI）
            </h3>
            <div 
              class="w-full min-h-[60px] border-2 border-dashed rounded-lg flex items-center justify-center p-2 transition-colors"
              :class="targetVariable ? 'border-amber-300 bg-white/60' : 'border-amber-300/50 bg-amber-100/30 hover:bg-amber-100/50'"
              @dragover="onDragOver"
              @dragenter.prevent
              @drop="onDropTarget"
            >
              <div v-if="targetVariable" 
                draggable="true"
                @dragstart="onDragStart($event, targetVariable, 'target', null, null)"
                class="w-full relative px-4 py-2.5 bg-white border border-amber-300 rounded-md shadow-sm flex items-center cursor-grab"
              >
                <i class="fas fa-star text-amber-400 mr-3"></i>
                <span class="font-bold text-amber-900">{{ targetVariable.alias || targetVariable.original }}</span>
                <span class="ml-auto text-xs text-amber-600/70 font-mono">{{ targetVariable.original }}</span>
              </div>
              <div v-else class="text-amber-700/60 text-sm font-medium">
                将您的核心KPI拖到这里
              </div>
            </div>
          </div>

          <!-- Dynamic Levels -->
          <div class="space-y-4">
            <div v-for="(level, index) in hierarchy" :key="level.id" class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative group">
              <div class="absolute -left-3 top-5 w-8 h-8 bg-indigo-600 rounded-full border-[3px] border-ice-white flex items-center justify-center text-xs text-white font-bold shadow-md z-10 transition-transform group-hover:scale-110">
                L{{ index + 1 }}
              </div>
              
              <div class="flex justify-between items-center mb-5 pl-4">
                <div class="flex-1 items-center flex">
                  <input v-model="level.level_name" class="text-lg font-bold text-slate-800 bg-transparent border-b border-transparent focus:border-indigo-400 hover:border-slate-300 focus:outline-none pb-0.5 w-1/2 transition-colors" placeholder="命名当前节点层级..."/>
                  <i class="fas fa-pen text-xs text-slate-300 ml-2"></i>
                </div>
                <button v-if="hierarchy.length > 1" @click="removeLevel(index)" class="text-slate-400 hover:text-rose-500 px-2 py-1 transition-colors"><i class="fas fa-trash-alt"></i></button>
              </div>

              <div class="grid grid-cols-5 gap-4 pl-4 relative">
                <!-- ID/Node Identifier -->
                <div class="col-span-2 bg-slate-50 p-3 rounded-lg border border-slate-200">
                  <div class="text-xs font-bold text-slate-500 mb-2 uppercase tracking-wide flex justify-between">
                    <span>节点标识 (Node ID)</span>
                  </div>
                  <div 
                    class="min-h-[44px] border-2 border-dashed border-slate-300 rounded-md flex flex-wrap gap-2 p-1 items-center justify-center"
                    :class="{'bg-white': level.id_column}"
                    @dragover="onDragOver"
                    @dragenter.prevent
                    @drop="onDropId($event, index)"
                  >
                    <div v-if="level.id_column" 
                      draggable="true"
                      @dragstart="onDragStart($event, level.id_column, 'id', index, null)"
                      class="w-full px-3 py-1.5 bg-white border border-blue-200 text-blue-700 rounded shadow-sm flex items-center cursor-grab text-sm font-semibold"
                    >
                      <i class="fas fa-sitemap text-blue-400 mr-2"></i>
                      <span class="truncate">{{ level.id_column.alias || level.id_column.original }}</span>
                    </div>
                    <span v-else class="text-xs text-slate-400 w-full text-center">拖拽标识列...</span>
                  </div>
                </div>

                <!-- Covariates -->
                <div class="col-span-3 bg-slate-50 p-3 rounded-lg border border-slate-200">
                  <div class="text-xs font-bold text-slate-500 mb-2 uppercase tracking-wide">环境协变量 (Covariates X)</div>
                  <div 
                    class="min-h-[44px] border-2 border-dashed border-slate-300 rounded-md flex flex-wrap gap-2 p-2 items-start"
                    :class="{'bg-white': level.covariates.length > 0}"
                    @dragover="onDragOver"
                    @dragenter.prevent
                    @drop="onDropCovariate($event, index)"
                  >
                    <div v-for="(cov, covIndex) in level.covariates" :key="cov.id" 
                      draggable="true"
                      @dragstart="onDragStart($event, cov, 'covariate', index, covIndex)"
                      class="px-3 py-1.5 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded shadow-sm flex items-center cursor-grab text-sm font-semibold whitespace-nowrap"
                    >
                      <i class="fas fa-chart-line text-emerald-500 mr-2"></i>
                      {{ cov.alias || cov.original }}
                    </div>
                    
                    <span v-if="level.covariates.length === 0" class="text-xs text-slate-400 w-full text-center py-1">拖拽影响该层级的客观变量至此...</span>
                  </div>
                </div>
                
                <!-- Connection Visuals -->
                <div v-if="index < hierarchy.length - 1" class="absolute -bottom-8 left-8 w-px h-6 bg-indigo-300 z-0 border-l border-dashed border-indigo-400"></div>
              </div>
            </div>

            <!-- Add Level Button -->
            <button @click="addLevel" class="w-full py-3 border-2 border-dashed border-indigo-200 bg-indigo-50/50 rounded-xl text-indigo-500 hover:text-white hover:bg-indigo-500 hover:border-indigo-500 transition-all font-bold text-sm flex items-center justify-center group shadow-sm">
              <i class="fas fa-plus mr-2 group-hover:scale-110 transition-transform"></i> 添加下一级网络节点 (Add Sub-Level)
            </button>
          </div>
          
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="h-[60vh] flex flex-col items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl bg-white/80">
        <div class="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mb-5">
          <i class="fas fa-table text-2xl text-indigo-400"></i>
        </div>
        <h2 class="text-lg font-bold text-slate-700 mb-1">准备开始分析</h2>
        <p class="text-sm text-slate-400 max-w-sm text-center mb-6">上传 CSV 文件、粘贴数据，或加载内置行业场景快速体验</p>
        <div class="flex gap-3">
          <label class="px-5 py-2.5 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl cursor-pointer transition-colors shadow-sm shadow-indigo-200 flex items-center gap-2">
            <i class="fas fa-upload"></i>上传数据
            <input type="file" class="hidden" accept=".csv" @change="handleFileUpload" />
          </label>
          <button @click="() => { selectedDemo = 'public_security'; loadDemo(); }" class="px-5 py-2.5 text-sm font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-xl border border-indigo-200 transition-colors flex items-center gap-2">
            <i class="fas fa-play"></i>加载示例
          </button>
        </div>
      </div>
    </div>

    <!-- Alias Editor Modal -->
    <div v-if="editingCol" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-xl shadow-2xl w-96 transform transition-all">
        <h3 class="font-bold text-lg text-slate-800 mb-1">自定义可视化归因标签</h3>
        <p class="text-xs text-slate-500 mb-4">修改在最终折线图/散点图中呈现的名称，仅用作展示，绝不影响底层张量计算引擎。</p>
        
        <div class="mb-4">
          <label class="block text-xs font-bold text-slate-500 mb-1">原始数据表头列名</label>
          <input type="text" :value="editingCol.original" disabled class="w-full bg-slate-100 border border-slate-200 rounded p-2 text-slate-600 font-mono text-sm" />
        </div>
        <div class="mb-6">
          <label class="block text-xs font-bold text-indigo-600 mb-1">图表展示动态别名 (Alias)</label>
          <input type="text" v-model="tempAlias" autofocus @keyup.enter="saveAlias" class="w-full bg-white border border-indigo-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 rounded p-2 font-bold text-slate-800 outline-none" placeholder="输入更易于领导读懂的名称..." />
        </div>
        
        <div class="flex justify-end space-x-3">
          <button @click="editingCol = null" class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded font-medium">取消设置</button>
          <button @click="saveAlias" class="px-4 py-2 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded font-bold shadow-sm">保存别名</button>
        </div>
      </div>
    </div>

    <!-- Manual Input Modal -->
    <div v-if="showManualInput" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-xl shadow-2xl w-[800px] max-w-full flex flex-col h-[70vh]">
        <h3 class="font-bold text-lg text-slate-800 mb-1">手动录入宽表数据</h3>
        <p class="text-xs text-slate-500 mb-4">您可以直接将 Excel 的数据粘贴到下方文本框中 (也支持 CSV 格式输入)。<strong class="text-indigo-500">新手注：数据首行必须是列名，且必须包含数值类数据。若想体验地图大屏，请命名经度列为'经度坐标'、纬度列为'纬度坐标'。</strong></p>
        
        <textarea v-model="manualCsvText" class="flex-1 w-full border border-slate-300 rounded p-3 font-mono text-sm bg-slate-50 focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-none mb-4" placeholder="大洲,大区名称,经度坐标,纬度坐标,资金投入X,目标达成情况Y&#10;亚洲,远东,116.4,39.9,150.5,0.88&#10;美洲,北美,-74.0,40.7,210.0,0.92"></textarea>
        
        <div class="flex justify-between items-center mt-auto">
          <div class="flex space-x-3">
             <button @click="loadDemoToEditor" class="px-3 py-1.5 text-xs text-indigo-600 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded font-medium transition flex items-center">
               <i class="fas fa-file-import mr-1.5"></i>载入当前所选范例模板
             </button>
             <button @click="exportManualData" class="px-3 py-1.5 text-xs text-slate-600 bg-slate-50 border border-slate-200 hover:bg-slate-100 rounded font-medium transition flex items-center" title="将编辑区内容保存为CSV文件">
               <i class="fas fa-save mr-1.5"></i>保存至本地 (.csv)
             </button>
          </div>
          <div class="flex space-x-3">
            <button @click="showManualInput = false" class="px-4 py-2 text-sm text-slate-600 hover:bg-slate-100 rounded font-medium">取消</button>
            <button @click="handleManualSubmit" class="px-4 py-2 text-sm text-white bg-emerald-600 hover:bg-emerald-700 rounded font-bold shadow-sm">解析并载入模型</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { save } from '@tauri-apps/plugin-dialog';
import { writeTextFile } from '@tauri-apps/plugin-fs';

const emit = defineEmits(['health-check']);

// Column and Data management
const columns = ref([]);
const unassignedColumns = ref([]);
const parsedTableData = ref([]);

// Topology Definition (Uses the original name mapped structures!)
const targetVariable = ref(null);
const hierarchy = ref([]);

// Demo selection
const selectedDemo = ref('');
const currentPresetInfo = ref(null);

// 预设场景说明数据
const presetInfoMap = {
  public_security: {
    title: '社会治理 · 省市三级公安防效能评估',
    description: '模拟从省级调度→市局指挥→基层分局执行的三级警务效能网络。评估各分局在给定资源条件下（经费、巡防密度、监控覆盖率）的实际打防转化效率，识别超常发挥和需要支援的单位。',
    hierarchy: [
      { name: '省级调度池', idDesc: '省厅区划（如XX省）' },
      { name: '市局作战圈', idDesc: '市局单位（如XX市公安局）' },
      { name: '基层分局（落实方）', idDesc: '分局名称（如XX分局）' }
    ],
    targetDesc: '综合打防转化率（核心KPI）',
    covariates: [
      { name: '专班经费投入', desc: '市局层面的专项经费' },
      { name: '警力巡防密度', desc: '基层警力部署程度' },
      { name: '监控覆盖率', desc: '技防设施完备程度' }
    ],
    adaptExample: { from: '综合打防转化率', to: '您的核心考核指标' }
  },
  geopolitics: {
    title: '地缘政治 · 全球同盟冲突演化博弈',
    description: '构建联盟→战区→国家→城市的四层地缘影响网络。评估各城市在所属联盟政策、战区局势和国家条件下的区域稳定性，支持地理空间可视化。',
    hierarchy: [
      { name: '全球联盟层', idDesc: '联盟名称（如XX同盟）' },
      { name: '战区层', idDesc: '战区（如XX战区）' },
      { name: '国家层', idDesc: '国家名称' },
      { name: '城市层', idDesc: '城市名称' }
    ],
    targetDesc: '区域维稳指数（核心KPI）',
    covariates: [
      { name: '联盟制裁压力', desc: '所属联盟面临的制裁强度' },
      { name: '经济韧性指数', desc: '本地经济抗压能力' },
      { name: '军事部署密度', desc: '战区军事力量配置' }
    ],
    adaptExample: { from: '区域维稳指数', to: '您的核心评估指标' }
  },
  health: {
    title: '公共卫生 · 跨国-区域重症致死率归因',
    description: '在全球→区域→国家的层级下，分析各国重症致死率与医疗资源、卫生投入的关系，识别同等条件下表现优异或异常的国家。',
    hierarchy: [
      { name: '全球大区', idDesc: '大洲或国际区域' },
      { name: '国家层', idDesc: '国家名称' }
    ],
    targetDesc: '重症致死率（核心指标）',
    covariates: [
      { name: '人均医疗支出', desc: '医疗资源投入水平' },
      { name: '床位数/千人', desc: '基础设施完备度' }
    ],
    adaptExample: { from: '重症致死率', to: '您的健康评估指标' }
  },
  retail: {
    title: '商业零售 · 跨国总部-区域市场销量推演',
    description: '总部→大区→国家→城市的四级零售网络。评估各市场在给定条件下（广告投放、门店密度）的实际销量表现，发现被低估的高潜力市场。',
    hierarchy: [
      { name: '全球总部', idDesc: '总部/集团' },
      { name: '大区层', idDesc: '大区（如亚太区）' },
      { name: '国家层', idDesc: '国家' },
      { name: '城市层', idDesc: '城市' }
    ],
    targetDesc: '市场销量（核心KPI）',
    covariates: [
      { name: '广告投放预算', desc: '市场推广投入' },
      { name: '门店覆盖密度', desc: '渠道覆盖程度' }
    ],
    adaptExample: { from: '市场销量', to: '您的销售业绩指标' }
  },
  coral_reef: {
    title: '生态保护 · 珊瑚礁生态保护观测网',
    description: '海洋区域→礁群→观测站的三级生态评估。分析各观测站在给定环境条件（水温、污染指数）下的珊瑚覆盖率表现，定位生态保护亮点和暗点。',
    hierarchy: [
      { name: '海洋区域', idDesc: '海域名称' },
      { name: '礁群', idDesc: '礁群编号' },
      { name: '观测站', idDesc: '站点编号' }
    ],
    targetDesc: '珊瑚覆盖率（核心指标）',
    covariates: [
      { name: '年均水温', desc: '环境温度影响' },
      { name: '污染综合指数', desc: '人类活动影响' }
    ],
    adaptExample: { from: '珊瑚覆盖率', to: '您的生态评估指标' }
  },
  overseas_resilience: {
    title: '战略规划 · 海外利益韧性图谱与风险预测',
    description: '大洲→国家→城市的三级海外利益评估。分析各节点在给定风险条件下的韧性表现，支持跨国投资和安全规划决策。',
    hierarchy: [
      { name: '大洲层', idDesc: '大洲' },
      { name: '国家层', idDesc: '国家' },
      { name: '城市层', idDesc: '城市' }
    ],
    targetDesc: '利益韧性指数（核心指标）',
    covariates: [
      { name: '政治稳定度', desc: '所在国政治环境' },
      { name: '经济依存度', desc: '与母国经济联系' },
      { name: '安保投入', desc: '安全保障资源' }
    ],
    adaptExample: { from: '利益韧性指数', to: '您的风险评估指标' }
  }
};

// 加载预设时设置说明信息
const setPresetInfo = (key) => {
  currentPresetInfo.value = presetInfoMap[key] || null;
};

// Sampling mode ('accurate' or 'fast') - 默认快速模式
const samplingMode = ref('fast');
const showAdvancedSampling = ref(false);
const customDraws = ref(500);
const customTune = ref(300);

const toggleSamplingMode = () => {
    if (samplingMode.value === 'fast') {
        samplingMode.value = 'accurate';
        customDraws.value = 1500;
        customTune.value = 1000;
    } else {
        samplingMode.value = 'fast';
        customDraws.value = 500;
        customTune.value = 300;
    }
};

// Manual Input state
const showManualInput = ref(false);
const manualCsvText = ref('');

const handleManualSubmit = () => {
    if(!manualCsvText.value.trim()){
        alert("请输入数据");
        return;
    }
    // Simple tab to comma converter if user pastes from excel
    let cleanedText = manualCsvText.value.replace(/\t/g, ',');
    parseCsvToState(cleanedText);
    showManualInput.value = false;
    selectedDemo.value = 'custom';
};

// Drag and drop state
const draggedItem = ref(null);
const dragSource = ref({ type: '', levelIndex: null, covIndex: null });

// Alias Editor State
const editingCol = ref(null);
const tempAlias = ref('');

// Generates an object wrapper for columns
const createColObj = (name) => ({
  id: name + '_' + Math.random().toString(36).substring(2, 9),
  original: name,
  alias: name
});

// Start validation and prepare for Inference request payload
const proceedToHealthCheck = () => {
  if (!targetVariable.value) return alert("请先指定您要评估的核心KPI指标");
  
  // Format pure structure back to standard backend API
  const cleanHierarchy = hierarchy.value.filter(l => l.id_column).map(l => ({
     level_index: l.level_index,
     level_name: l.level_name,
     id_column: l.id_column.original,
     covariates: l.covariates.map(c => c.original) // pass original to backend!
  }));
  
  if (cleanHierarchy.length === 0) return alert("必须至少完成一层网络拓扑构建，且带有节点标识");

  emit('health-check', { 
    hierarchy: cleanHierarchy, 
    target: { name: targetVariable.value.original, type: 'continuous' }, 
    tableData: parsedTableData.value,
    displayMapping: generateDisplayMapping(),
    samplingMode: samplingMode.value,
    customDraws: customDraws.value,
    customTune: customTune.value
  });
};

const generateDisplayMapping = () => {
    let map = {};
    if(targetVariable.value) map[targetVariable.value.original] = targetVariable.value.alias;
    hierarchy.value.forEach(l => {
        if(l.id_column) map[l.id_column.original] = l.id_column.alias;
        l.covariates.forEach(c => map[c.original] = c.alias);
    });
    return map;
};

// CSV file processing
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    parseCsvToState(e.target.result);
    selectedDemo.value = '';
  };
  reader.readAsText(file);
};

// Global parsing logic
const parseCsvToState = (csvText) => {
  const lines = csvText.trim().split('\n');
  if (lines.length < 2) return alert("源表格必须包含有效的数据。");
  
  const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
  const dataList = [];
  
  for (let i = 1; i < lines.length; i++) {
    if(!lines[i].trim()) continue;
    const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
    let rowObj = {};
    headers.forEach((header, index) => {
      const val = values[index];
      rowObj[header] = isNaN(Number(val)) || val === '' ? val : Number(val);
    });
    dataList.push(rowObj);
  }

  columns.value = headers.map(h => createColObj(h));
  unassignedColumns.value = [...columns.value];
  parsedTableData.value = dataList;
  targetVariable.value = null;
  hierarchy.value = [{ id: 'L1', level_index: 0, level_name: '网格管理层 L1', id_column: null, covariates: [] }];
};

const getDemoCsvData = (demoKey) => {
    switch (demoKey) {
        case 'public_security':
            return `省厅区划,市局单位,分局名称,专班经费投入,警力巡防密度,监控覆盖率,经度坐标,纬度坐标,综合打防转化率
广东省,广州市,天河分局,450,0.85,0.92,113.264,23.129,0.88
广东省,广州市,越秀分局,520,0.91,0.98,113.266,23.129,0.94
广东省,深圳市,南山分局,310,0.76,0.85,113.930,22.533,0.79
广东省,深圳市,福田分局,390,0.82,0.90,114.055,22.533,0.83
广东省,佛山市,南海分局,280,0.71,0.88,113.122,23.021,0.81
广东省,湛江市,霞山分局,190,0.61,0.72,110.358,21.276,0.65
广东省,珠海市,香洲分局,260,0.75,0.83,113.576,22.270,0.77`;
        case 'geopolitics':
            return `势力阵营,战略大区,主权国家,热点城市,经度坐标,纬度坐标,经济制裁深度,军事兵力投送量,武器军援指数,网络战攻击强度,区域维稳指数Y
北约集群NATO,东欧战略区,乌克兰,基辅Kyiv,30.523,50.450,0.95,0.80,0.92,0.75,0.30
北约集群NATO,东欧战略区,波兰,华沙Warsaw,21.012,52.229,0.15,0.55,0.40,0.20,0.88
北约集群NATO,高加索观察区,格鲁吉亚,第比利斯Tbilisi,44.827,41.715,0.10,0.30,0.20,0.10,0.85
金砖抗压链BRICS,远东及亚太,俄罗斯,符拉迪沃斯托克VVO,131.886,43.119,0.50,0.85,0.70,0.55,0.75
金砖抗压链BRICS,中东新轴心,叙利亚,大马士革Damascus,36.291,33.513,0.88,0.72,0.89,0.60,0.25
金砖抗压链BRICS,中东新轴心,也门,萨那Sanaa,44.206,15.369,0.70,0.45,0.95,0.30,0.18
中间游离带,南亚次大陆,印度,新德里NewDelhi,77.209,28.613,0.05,0.60,0.40,0.35,0.90
中间游离带,非洲之角,索马里,摩加迪沙Mogadishu,45.343,2.046,0.20,0.15,0.80,0.12,0.15
中间游离带,东南亚通道,缅甸,内比都Naypyidaw,96.131,19.763,0.30,0.25,0.55,0.18,0.40`;
        case 'health':
            return `大洲,国家,重症ICU代号,危重医学拨款,医床周转率,院感防控值,病死率
北美洲,美国,US-H1,1500,0.3,0.85,0.012
北美洲,美国,US-H2,1200,0.25,0.91,0.015
北美洲,加拿大,CA-H1,900,0.4,0.70,0.009
欧洲区,英国,UK-H1,1100,0.35,0.88,0.011
欧洲区,德国,DE-H1,1300,0.45,0.65,0.007`;
        case 'retail':
            return `全球大区,国家市场,城市群,品牌公关预算,竞品下沉率,当地人均GDP,当季净利润增长率
APAC,中国,长三角,500,0.8,2.1,1.12
APAC,中国,珠三角,450,0.9,1.9,1.05
APAC,日本,关东圈,300,0.95,3.5,0.98
EMEA,英国,大伦敦,400,0.7,3.8,1.01
AMER,美国,加利福尼亚,800,0.85,4.5,1.25`;
        case 'coral_reef':
            return `国家战略层,站点战役层,经度坐标,纬度坐标,人口驻留X1,保护合规度X2,观测生物量Y
英属印度洋领地,Chagos,71.300,-6.300,0,3,2975.58
巴布亚新几内亚,Karkar,145.900,-4.600,1,2,950.00
所罗门群岛,Choiseul,156.900,-6.700,1,1,1800.00
所罗门群岛,Makira,161.800,-10.500,1,1,1550.00
印度尼西亚,Raja Ampat 1,130.500,-0.200,1,2,850.00
澳大利亚,Lord Howe,159.000,-31.500,1,3,450.00
夏威夷,Oahu 1,-158.000,21.400,1,1,150.00
夏威夷,Maui 1,-156.300,20.800,1,1,180.00
牙买加,Montego Bay 1,-77.900,18.400,1,1.5,80.00
肯尼亚,Diani,39.500,-4.300,1,1,120.00
印度尼西亚,Karimunjawa 2,110.400,-5.800,1,1.5,90.00
澳大利亚,Great Barrier 1,145.000,-15.000,0,3,1100.00
夏威夷,Kauai 1,-159.500,22.100,1,1,350.00
所罗门群岛,Isabel,158.500,-8.000,1,1,1200.00
牙买加,Rio Bueno,-77.400,18.400,1,1,210.00`;
        case 'overseas_resilience':
            return `国家L1,行业L2,项目名称L3,L1_X_东道国治安指数_1_10,L1_X_双边关系热度_1_10,L3_X_劳工本地化比例_Pct,L3_X_社区融合度得分_1_10,Y_项目按期完工率_Pct
新加坡,基础设施,新港深水码头,9.5,8.5,45.0,8.0,92.5
新加坡,数字科技,东南亚云数据中心,9.5,8.5,60.0,7.5,95.0
卢旺达,数字科技,基加利智慧城市中枢,7.5,9.0,85.0,9.0,98.2
卢旺达,公共卫生,中非医疗援助中心,7.5,9.0,70.0,9.5,96.0
巴基斯坦,基础设施,瓜达尔港扩建工程,4.0,9.5,88.0,8.5,85.5
巴基斯坦,能源矿产,塔尔煤田一体化,3.5,9.5,82.0,8.0,81.0
某发达国家A,基础设施,跨国高铁标段二,9.0,6.0,15.0,3.0,35.5
某发达国家A,数字科技,5G核心网建设,9.0,6.0,20.0,4.0,28.0
某拉美国家B,能源矿产,锂矿开采一期,5.0,7.0,30.0,4.5,42.0
某拉美国家B,基础设施,特高压输电走廊,5.0,7.0,50.0,6.0,65.0
苏丹,能源矿产,尼罗河油田管道,2.5,8.0,90.0,8.5,78.5
某东南亚国C,基础设施,雅万高铁枢纽,6.5,8.5,75.0,7.5,88.0
某东南亚国C,金融布局,跨境人民币清算网,6.5,8.5,65.0,7.0,90.5`;
        default:
            return "省厅,分局,经度坐标,纬度坐标,警力投入X1,监控密度X2,打防转化率Y\n广东,天河,113.264,23.129,450,0.92,0.88\n广东,越秀,113.266,23.129,520,0.98,0.94\n广东,南山,113.930,22.533,310,0.85,0.79";
    }
};

// Tool: Download sample CSV
const downloadSampleCSV = async () => {
    const csvContent = getDemoCsvData(selectedDemo.value).trim();
    const fileName = selectedDemo.value ? `DeepBayes_Template_${selectedDemo.value}.csv` : "DeepBayes_Template_Default.csv";
    
    try {
        const filePath = await save({
            defaultPath: fileName,
            filters: [{ name: 'CSV Document', extensions: ['csv'] }]
        });
        
        if (filePath) {
            await writeTextFile(filePath, csvContent);
            alert("✅ 模版文件已成功保存至本地！");
        }
    } catch(e) {
        console.error("下载模版失败:", e);
        alert(`❌ 保存失败: ${e.message || e}`);
    }
};

const exportManualData = async () => {
    if(!manualCsvText.value.trim()){
        alert("编辑器内无数据可保存");
        return;
    }
    try {
        const filePath = await save({
            defaultPath: "DeepBayes_Manual_Data.csv",
            filters: [{ name: 'CSV Document', extensions: ['csv'] }]
        });
        
        if (filePath) {
            await writeTextFile(filePath, manualCsvText.value);
            alert("✅ 数据已成功保存至本地！");
        }
    } catch(e) {
        console.error("保存失败:", e);
        alert(`❌ 保存失败: ${e.message || e}`);
    }
};

const loadDemoToEditor = () => {
    if (!selectedDemo.value) {
        alert("请先在左侧下拉框中选择一个沙盒模板！");
        return;
    }
    manualCsvText.value = getDemoCsvData(selectedDemo.value).trim();
};

// Alias Rename actions
const editAlias = (col) => {
  editingCol.value = col;
  tempAlias.value = col.alias !== col.original ? col.alias : '';
};
const saveAlias = () => {
  if (editingCol.value) {
    editingCol.value.alias = tempAlias.value.trim() || editingCol.value.original;
    editingCol.value = null;
  }
};

// Hierarchy actions
const addLevel = () => {
  hierarchy.value.push({
    id: 'L' + (hierarchy.value.length + 1) + '_' + Date.now(),
    level_index: hierarchy.value.length,
    level_name: `网格拓展层 L${hierarchy.value.length + 1}`,
    id_column: null,
    covariates: []
  });
};
const removeLevel = (index) => {
  const level = hierarchy.value[index];
  if (level.id_column) unassignedColumns.value.push(level.id_column);
  if (level.covariates.length > 0) unassignedColumns.value.push(...level.covariates);
  hierarchy.value.splice(index, 1);
  hierarchy.value.forEach((l, i) => l.level_index = i); // Repack array
};

// HTML5 API Drag Hooks
const onDragStart = (e, item, sourceType, levelIndex, covIndex) => {
  draggedItem.value = item;
  dragSource.value = { type: sourceType, levelIndex, covIndex };
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', item.id); // Safari/Chrome requires setData to not cancel drag
  e.currentTarget.classList.add('opacity-50');
};

const onDragOver = (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
};

const onRootDragOver = (e) => {
  e.preventDefault();
  if (e.dataTransfer.types.includes('text/plain')) {
    e.dataTransfer.dropEffect = 'move';
  } else {
    e.dataTransfer.dropEffect = 'none';
  }
};

const removeDraggedFromSource = () => {
  const src = dragSource.value;
  if(src.type === 'unassigned') {
    unassignedColumns.value = unassignedColumns.value.filter(c => c.id !== draggedItem.value.id);
  } else if (src.type === 'target') {
    targetVariable.value = null;
  } else if (src.type === 'id') {
    hierarchy.value[src.levelIndex].id_column = null;
  } else if (src.type === 'covariate') {
    hierarchy.value[src.levelIndex].covariates.splice(src.covIndex, 1);
  }
};

// HTML5 Drop Containers Logic
const onDropUnassigned = () => {
  if(!draggedItem.value) return;
  if(dragSource.value.type !== 'unassigned') {
    removeDraggedFromSource();
    unassignedColumns.value.push(draggedItem.value);
  }
  teardownDrag();
};

const onDropTarget = () => {
  if(!draggedItem.value) return;
  if (dragSource.value.type === 'target') return teardownDrag();
  
  if (targetVariable.value) {
    unassignedColumns.value.push(targetVariable.value);
  }
  
  removeDraggedFromSource();
  targetVariable.value = draggedItem.value;
  teardownDrag();
};

const onDropId = (e, levelIndex) => {
  if(!draggedItem.value) return;
  if (dragSource.value.type === 'id' && dragSource.value.levelIndex === levelIndex) return teardownDrag();
  
  const level = hierarchy.value[levelIndex];
  if (level.id_column) {
    unassignedColumns.value.push(level.id_column);
  }
  
  removeDraggedFromSource();
  level.id_column = draggedItem.value;
  teardownDrag();
};

const onDropCovariate = (e, levelIndex) => {
  if(!draggedItem.value) return;
  const level = hierarchy.value[levelIndex];
  
  if (level.covariates.find(c => c.id === draggedItem.value.id)) {
      return teardownDrag();
  }
  
  removeDraggedFromSource();
  level.covariates.push(draggedItem.value);
  teardownDrag();
};

const teardownDrag = () => {
  draggedItem.value = null;
  document.querySelectorAll('.opacity-50').forEach(el => el.classList.remove('opacity-50'));
};


// 模版库自动化装载函数
const loadDemo = () => {
  setPresetInfo(selectedDemo.value);
  if (selectedDemo.value === 'public_security') injectPublicSecurityDemo();
  else if (selectedDemo.value === 'health') injectHealthDemo();
  else if (selectedDemo.value === 'retail') injectRetailDemo();
  else if (selectedDemo.value === 'geopolitics') injectGeopoliticsDemo();
  else if (selectedDemo.value === 'coral_reef') injectCoralReefDemo();
  else if (selectedDemo.value === 'overseas_resilience') injectOverseasResilienceDemo();
};

const injectPublicSecurityDemo = () => {
    const csvData = getDemoCsvData('public_security').trim();
    parseCsvToState(csvData);
    
    // Auto map the structure for demo purposes
    setTimeout(() => {
        const findCol = (name) => unassignedColumns.value.find(c => c.original === name);
        const mapOne = (colObj, type, lIdx) => {
           if(!colObj) return;
           unassignedColumns.value = unassignedColumns.value.filter(c => c.id !== colObj.id);
           if(type === 'target') targetVariable.value = colObj;
           else if (type === 'id') hierarchy.value[lIdx].id_column = colObj;
           else if (type === 'cov') hierarchy.value[lIdx].covariates.push(colObj);
        };
        
        mapOne(findCol('综合打防转化率'), 'target', null);
        
        hierarchy.value = [
          { id: 'l1', level_index: 0, level_name: '省级调度池', id_column: null, covariates: []},
          { id: 'l2', level_index: 1, level_name: '市局作战圈', id_column: null, covariates: []},
          { id: 'l3', level_index: 2, level_name: '基层分局（落实方）', id_column: null, covariates: []}
        ];
        
        mapOne(findCol('省厅区划'), 'id', 0);
        mapOne(findCol('市局单位'), 'id', 1);
        mapOne(findCol('分局名称'), 'id', 2);
        
        mapOne(findCol('专班经费投入'), 'cov', 1);
        mapOne(findCol('警力巡防密度'), 'cov', 2);
        mapOne(findCol('监控覆盖率'), 'cov', 2);
        if(targetVariable.value) targetVariable.value.alias = "作战效率期望 (Y)";
    }, 100);
};

const injectGeopoliticsDemo = () => {
    const csvData = getDemoCsvData('geopolitics').trim();
    parseCsvToState(csvData);
    
    // 自动映射4层拓扑结构
    setTimeout(() => {
        const findCol = (name) => unassignedColumns.value.find(c => c.original === name);
        const mapOne = (colObj, type, lIdx) => {
           if(!colObj) return;
           unassignedColumns.value = unassignedColumns.value.filter(c => c.id !== colObj.id);
           if(type === 'target') targetVariable.value = colObj;
           else if (type === 'id') hierarchy.value[lIdx].id_column = colObj;
           else if (type === 'cov') hierarchy.value[lIdx].covariates.push(colObj);
        };
        
        mapOne(findCol('区域维稳指数Y'), 'target', null);
        hierarchy.value = [
          { id: 'l1', level_index: 0, level_name: '全球阵营联盟 (Alliance)', id_column: null, covariates: []},
          { id: 'l2', level_index: 1, level_name: '战略大区司令部 (Theater)', id_column: null, covariates: []},
          { id: 'l3', level_index: 2, level_name: '主权国家 (State)', id_column: null, covariates: []},
          { id: 'l4', level_index: 3, level_name: '热点爆发城市 (Flashpoint)', id_column: null, covariates: []}
        ];
        mapOne(findCol('势力阵营'), 'id', 0);
        mapOne(findCol('战略大区'), 'id', 1);
        mapOne(findCol('主权国家'), 'id', 2);
        mapOne(findCol('热点城市'), 'id', 3);
        
        mapOne(findCol('经济制裁深度'), 'cov', 0);
        mapOne(findCol('军事兵力投送量'), 'cov', 1);
        mapOne(findCol('武器军援指数'), 'cov', 2);
        mapOne(findCol('网络战攻击强度'), 'cov', 3);
        if(targetVariable.value) targetVariable.value.alias = "全球综合维稳系数 Y";
    }, 100);
};

const injectHealthDemo = () => {
    const csvData = getDemoCsvData('health').trim();
    parseCsvToState(csvData);
};

const injectRetailDemo = () => {
    const csvData = getDemoCsvData('retail').trim();
    parseCsvToState(csvData);
};

const injectCoralReefDemo = () => {
    const csvData = getDemoCsvData('coral_reef').trim();
    parseCsvToState(csvData);
    
    setTimeout(() => {
        const findCol = (name) => unassignedColumns.value.find(c => c.original === name);
        const mapOne = (colObj, type, lIdx) => {
           if(!colObj) return;
           unassignedColumns.value = unassignedColumns.value.filter(c => c.id !== colObj.id);
           if(type === 'target') targetVariable.value = colObj;
           else if (type === 'id') hierarchy.value[lIdx].id_column = colObj;
           else if (type === 'cov') hierarchy.value[lIdx].covariates.push(colObj);
        };
        
        mapOne(findCol('观测生物量Y'), 'target', null);
        hierarchy.value = [
          { id: 'l1', level_index: 0, level_name: '国家环境保护战略级', id_column: null, covariates: []},
          { id: 'l2', level_index: 1, level_name: '站点观测战役级', id_column: null, covariates: []}
        ];
        mapOne(findCol('国家战略层'), 'id', 0);
        mapOne(findCol('站点战役层'), 'id', 1);
        
        mapOne(findCol('人口驻留X1'), 'cov', 1);
        mapOne(findCol('保护合规度X2'), 'cov', 1);
    }, 100);
};

const injectOverseasResilienceDemo = () => {
    const csvData = getDemoCsvData('overseas_resilience').trim();
    parseCsvToState(csvData);
    
    setTimeout(() => {
        const findCol = (name) => unassignedColumns.value.find(c => c.original === name);
        const mapOne = (colObj, type, lIdx) => {
           if(!colObj) return;
           unassignedColumns.value = unassignedColumns.value.filter(c => c.id !== colObj.id);
           if(type === 'target') targetVariable.value = colObj;
           else if (type === 'id') hierarchy.value[lIdx].id_column = colObj;
           else if (type === 'cov') hierarchy.value[lIdx].covariates.push(colObj);
        };
        
        mapOne(findCol('Y_项目按期完工率_Pct'), 'target', null);
        hierarchy.value = [
          { id: 'l1', level_index: 0, level_name: '东道国 (Host Country)', id_column: null, covariates: []},
          { id: 'l2', level_index: 1, level_name: '行业领域 (Industry Sector)', id_column: null, covariates: []},
          { id: 'l3', level_index: 2, level_name: '实体项目 (Project)', id_column: null, covariates: []}
        ];
        mapOne(findCol('国家L1'), 'id', 0);
        mapOne(findCol('行业L2'), 'id', 1);
        mapOne(findCol('项目名称L3'), 'id', 2);
        
        mapOne(findCol('L1_X_东道国治安指数_1_10'), 'cov', 0);
        mapOne(findCol('L1_X_双边关系热度_1_10'), 'cov', 0);
        mapOne(findCol('L3_X_劳工本地化比例_Pct'), 'cov', 2);
        mapOne(findCol('L3_X_社区融合度得分_1_10'), 'cov', 2);
        
        if(targetVariable.value) targetVariable.value.alias = "项目按期完工率期望 (Y)";
    }, 100);
};
</script>