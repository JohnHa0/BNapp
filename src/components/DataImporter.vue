<template>
  <div class="min-h-screen bg-slate-50 p-8">
    <div class="mb-8 flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-100">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">构建层次贝叶斯网络</h1>
        <p class="text-sm text-slate-500 mt-2">导入您的宽表数据 (CSV)，系统将自动嗅探层级与变量映射。</p>
      </div>
      <div class="flex space-x-4">
        <button class="px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors">
          <i class="fas fa-download mr-2"></i>下载《视频侦查效能评估》模板
        </button>
        <label class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg cursor-pointer transition-colors shadow-sm flex items-center">
          <i class="fas fa-upload mr-2"></i>上传数据源 (CSV)
          <input type="file" class="hidden" accept=".csv" @change="handleFileUpload" />
        </label>
      </div>
    </div>

    <div v-if="columns.length > 0" class="flex gap-6 min-h-[600px]">
      
      <div class="w-1/3 bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex flex-col">
        <h2 class="text-lg font-bold text-slate-700 mb-4 border-b border-slate-100 pb-3">数据池 (未分配字段)</h2>
        <div class="flex-1 overflow-y-auto space-y-3 pr-2">
          <div v-for="col in unassignedColumns" :key="col" 
               class="p-3 bg-slate-50 border border-slate-200 rounded-lg cursor-move hover:border-indigo-400 hover:shadow-sm transition-all flex items-center justify-between group">
            <span class="text-sm font-medium text-slate-700">{{ col }}</span>
            <i class="fas fa-grip-vertical text-slate-300 group-hover:text-indigo-400"></i>
          </div>
          <div v-if="unassignedColumns.length === 0" class="text-center text-slate-400 text-sm py-8">
            所有字段已分配完毕
          </div>
        </div>
      </div>

      <div class="w-2/3 bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex flex-col">
        <div class="flex justify-between items-center border-b border-slate-100 pb-3 mb-5">
          <h2 class="text-lg font-bold text-slate-700">网络拓扑结构</h2>
          <button @click="showHealthCheck = true" class="px-4 py-2 text-sm font-bold text-emerald-700 bg-emerald-50 rounded-lg hover:bg-emerald-100 border border-emerald-200 transition-colors">
            <i class="fas fa-stethoscope mr-2"></i>运行数据体检
          </button>
        </div>
        
        <div class="mb-6 p-4 bg-amber-50 rounded-lg border border-amber-200">
          <div class="text-xs font-bold text-amber-800 mb-2 uppercase tracking-wider">靶点观测指标 (Y)</div>
          <div v-if="targetVariable" class="text-sm font-medium text-amber-900 bg-white px-3 py-2 rounded border border-amber-100 inline-block">
            🎯 {{ targetVariable.name }}
          </div>
          <div v-else class="text-sm text-amber-600/70 italic">请指定模型需要评估的目标变量...</div>
        </div>
        
        <div class="flex-1 overflow-y-auto space-y-6 pr-2">
          <div v-for="(level, index) in hierarchy" :key="index" class="p-5 bg-indigo-50/40 border border-indigo-100 rounded-xl relative">
            <div class="absolute -left-3 top-6 w-7 h-7 bg-indigo-100 rounded-full border-2 border-white flex items-center justify-center text-xs text-indigo-700 font-bold shadow-sm">
              L{{ index + 1 }}
            </div>
            
            <div class="flex justify-between items-center mb-4 pl-4">
              <input v-model="level.level_name" class="text-lg font-bold text-indigo-900 bg-transparent border-b border-dashed border-indigo-300 focus:outline-none focus:border-indigo-600 pb-1 w-1/2" placeholder="定义层级名称 (如: 战役层)"/>
              <button @click="removeLevel(index)" class="text-slate-400 hover:text-rose-500 transition-colors"><i class="fas fa-times"></i></button>
            </div>
            
            <div class="grid grid-cols-2 gap-5 pl-4">
              <div class="bg-white p-4 rounded-lg border border-slate-200">
                <div class="text-xs font-bold text-slate-500 mb-3">节点 ID 标识列</div>
                <div v-if="level.id_column" class="text-sm font-medium bg-blue-50 text-blue-700 p-2 rounded border border-blue-100 flex items-center">
                  <i class="fas fa-sitemap mr-2 text-blue-400"></i>{{ level.id_column }}
                </div>
              </div>
              <div class="bg-white p-4 rounded-lg border border-slate-200">
                <div class="text-xs font-bold text-slate-500 mb-3">环境协变量 (X)</div>
                <div class="space-y-2">
                  <div v-for="cov in level.covariates" :key="cov" class="text-sm font-medium bg-emerald-50 text-emerald-700 p-2 rounded border border-emerald-100 flex items-center">
                    <i class="fas fa-chart-line mr-2 text-emerald-400"></i>{{ cov }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <button @click="addLevel" class="w-full py-4 border-2 border-dashed border-slate-300 rounded-xl text-slate-500 hover:text-indigo-600 hover:border-indigo-400 hover:bg-indigo-50 transition-all font-medium text-sm">
            <i class="fas fa-plus mr-2"></i>添加下级网络节点
          </button>
        </div>
      </div>
    </div>

    <div v-if="showHealthCheck" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex justify-center items-center z-50 transition-opacity">
      <div class="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <DataHealthCheck 
          :hierarchy="hierarchy" 
          :targetVariable="targetVariable" 
          :tableData="parsedTableData"
          @close="showHealthCheck = false" 
          @proceed="handleProceedToBackend"
        />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import DataHealthCheck from './DataHealthCheck.vue'; // 确保路径正确引入了体检组件

// --- 声明触发给父组件 (App.vue) 的事件 ---
const emit = defineEmits(['start-inference']);

// --- 响应式状态区 ---
const columns = ref([]); 
const unassignedColumns = ref([]);
const parsedTableData = ref([]); 

const hierarchy = ref([]);
const targetVariable = ref(null); 
const showHealthCheck = ref(false);

// ==========================================
// 核心逻辑 1：真实的纯前端 CSV 解析引擎
// ==========================================
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const text = e.target.result;
    
    // 基础的 CSV 按行切割解析
    const lines = text.split('\n').filter(line => line.trim() !== '');
    if (lines.length < 2) {
      alert("CSV 数据格式错误或数据为空！");
      return;
    }

    // 提取表头
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    columns.value = [...headers];
    unassignedColumns.value = [...headers];

    // 提取并重组数据体
    const dataList = [];
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
      let rowObj = {};
      headers.forEach((header, index) => {
        // 尝试转换为数字，若失败则保留字符串（后续由体检组件拦截报错）
        const val = values[index];
        rowObj[header] = isNaN(Number(val)) || val === '' ? val : Number(val);
      });
      dataList.push(rowObj);
    }
    
    parsedTableData.value = dataList;
    console.log("CSV 解析成功，共加载数据：", dataList.length, "行");
    
    // 触发智能嗅探
    autoMapFields();
  };
  
  reader.readAsText(file); // 执行读取
};

// ==========================================
// 核心逻辑 2：启发式盲猜引擎 (Heuristic Mapping)
// ==========================================
const autoMapFields = () => {
  // 初始化经典三层架构模板
  hierarchy.value = [
    { level_index: 0, level_name: '战略层 (省厅/市局)', id_column: null, covariates: [] },
    { level_index: 1, level_name: '战役层 (支队/分局)', id_column: null, covariates: [] },
    { level_index: 2, level_name: '战术层 (单兵/派出所)', id_column: null, covariates: [] }
  ];

  const remaining = [];

  columns.value.forEach(col => {
    const colName = col.toLowerCase();
    let assigned = false;

    // 1. 嗅探靶点 (Y)
    if (colName.includes('转化率') || colName.includes('成功率') || colName.includes('指标')) {
      targetVariable.value = { name: col, type: 'continuous' };
      assigned = true;
    }
    // 2. 嗅探层级标识 (ID)
    else if (colName.includes('id') || colName.includes('市局') || colName.includes('省')) {
      if (!hierarchy.value[0].id_column) { hierarchy.value[0].id_column = col; assigned = true; }
    }
    else if (colName.includes('分局') || colName.includes('大队')) {
      if (!hierarchy.value[1].id_column) { hierarchy.value[1].id_column = col; assigned = true; }
    }
    else if (colName.includes('派出所') || colName.includes('名称') || colName.includes('节点')) {
      if (!hierarchy.value[2].id_column) { hierarchy.value[2].id_column = col; assigned = true; }
    }
    // 3. 嗅探特征 (X)
    else if (colName.includes('资金') || colName.includes('预算')) {
      hierarchy.value[0].covariates.push(col); assigned = true;
    }
    else if (colName.includes('比例') || colName.includes('在线率')) {
      hierarchy.value[1].covariates.push(col); assigned = true;
    }
    else if (colName.includes('考核') || colName.includes('负荷') || colName.includes('得分')) {
      hierarchy.value[2].covariates.push(col); assigned = true;
    }

    if (!assigned) remaining.push(col);
  });

  unassignedColumns.value = remaining;
};

// ==========================================
// 辅助操作逻辑
// ==========================================
const addLevel = () => {
  hierarchy.value.push({ 
    level_index: hierarchy.value.length, 
    level_name: `新增层级 L${hierarchy.value.length + 1}`, 
    id_column: null, 
    covariates: [] 
  });
};

const removeLevel = (index) => {
  // 生产环境中这里应补充逻辑：将该层的字段退回 unassignedColumns
  hierarchy.value.splice(index, 1);
};

// ==========================================
// 核心逻辑 3：接收体检结果，打包并触发后端请求
// ==========================================
const handleProceedToBackend = (healthCheckPayload) => {
  showHealthCheck.value = false; // 关闭体检弹窗
  
  // 组装最终向 FastAPI 发送的完美 JSON 格式 (对齐 OpenAPI 协议)
  const finalSchema = {
    target: targetVariable.value,
    hierarchy: hierarchy.value,
    tableData: parsedTableData.value // 经过体检组件清洗（如均值填充）后的数据
  };

  console.log("前端清洗与校验完毕！数据包已抛出给总控台：", finalSchema);
  
  // 【关键修复】不在当前组件发请求，而是将干净的数据弹射给 App.vue 的 startInference 方法
  emit('start-inference', finalSchema);
};
</script>