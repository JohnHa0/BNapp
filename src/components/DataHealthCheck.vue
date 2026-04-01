<template>
  <div class="bg-white p-6 rounded-xl shadow-[0_10px_40px_rgba(0,0,0,0.1)] border border-slate-100 flex flex-col h-full max-h-[85vh]">
    <div class="flex justify-between items-center mb-6 border-b border-slate-100 pb-4 shrink-0">
      <h2 class="text-xl font-bold text-deep-blue flex items-center">
        <div class="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center mr-3">
            <i class="fas fa-heartbeat text-indigo-500"></i>
        </div> 
        数据健康体检引擎 (Data Diagnostics)
      </h2>
      <div v-if="isChecking" class="text-sm text-indigo-600 font-bold flex items-center bg-indigo-50 px-3 py-1.5 rounded-full">
        <i class="fas fa-circle-notch fa-spin mr-2"></i> 正在执行 N 维张量合规性扫描...
      </div>
      <div v-else-if="checkComplete && fatalErrors.length === 0 && warnings.length === 0" class="text-sm font-bold text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-full shadow-inner border border-emerald-100">
        <i class="fas fa-shield-check mr-1"></i> 全维效验通过，数据高度健康
      </div>
    </div>

    <div class="flex-1 overflow-y-auto space-y-4 pr-2">
      <div v-if="fatalErrors.length > 0" class="p-4 bg-rose-50 border border-rose-200 rounded-xl shadow-sm">
        <h3 class="text-sm font-bold text-rose-800 mb-3 flex items-center">
          <i class="fas fa-radiation mr-2 text-rose-600"></i> 致命错误 (阻断模型构建)
        </h3>
        <ul class="space-y-2">
          <li v-for="(err, idx) in fatalErrors" :key="idx" class="text-sm text-rose-700 bg-white p-3 rounded-lg border border-rose-100 shadow-sm flex items-start">
            <i class="fas fa-times-circle mt-0.5 mr-2 text-rose-500"></i>
            <div>
              <strong>{{ err.column }}</strong>: {{ err.message }}
            </div>
          </li>
        </ul>
      </div>

      <div v-if="warnings.length > 0" class="p-4 bg-amber-50 border border-amber-200 rounded-xl shadow-sm">
        <h3 class="text-sm font-bold text-amber-800 mb-3 flex items-center">
          <i class="fas fa-exclamation-triangle mr-2 text-amber-500"></i> 质量预警 (非致死但影响推演精度)
        </h3>
        <ul class="space-y-2">
          <li v-for="(warn, idx) in warnings" :key="idx" class="text-sm text-amber-700 bg-white p-3 rounded-lg border border-amber-100 shadow-sm flex flex-col sm:flex-row justify-between sm:items-center gap-3">
            <div class="flex items-start">
               <i class="fas fa-info-circle mt-0.5 mr-2 text-amber-400"></i>
               <div><strong>{{ warn.column }}</strong>: {{ warn.message }}</div>
            </div>
            
            <div class="flex space-x-2 shrink-0">
                <button v-if="warn.type === 'missing'" @click="applyAutoFix(warn)" class="px-3 py-1.5 bg-emerald-100 hover:bg-emerald-200 text-emerald-800 text-xs font-bold rounded flex items-center shadow-sm transition-colors border border-emerald-200">
                  <i class="fas fa-magic mr-1.5"></i> 一键均值填充弥合
                </button>
                <button v-if="warn.type === 'zero_variance' || warn.type === 'missing'" @click="removeColumn(warn.column)" class="px-3 py-1.5 bg-rose-100 hover:bg-rose-200 text-rose-800 text-xs font-bold rounded flex items-center shadow-sm transition-colors border border-rose-200">
                  <i class="fas fa-trash-alt mr-1.5"></i> 剥离该变量
                </button>
            </div>
          </li>
        </ul>
      </div>

      <div v-if="checkComplete && fatalErrors.length === 0 && warnings.length === 0" class="h-full min-h-[200px] flex flex-col items-center justify-center p-8 bg-slate-50 rounded-xl border border-dashed border-slate-200">
        <div class="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mb-4 shadow-inner">
            <i class="fas fa-check-double text-3xl text-emerald-500"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-700 mb-1">多重共线性与量纲校验完美</h3>
        <p class="text-slate-500 text-sm">所有数据列均符合 PyMC NUTS 采样器的严苛张量计算标准。</p>
      </div>
    </div>

    <div class="mt-6 pt-4 border-t border-slate-100 flex justify-end space-x-3 shrink-0">
      <button @click="$emit('close')" class="px-5 py-2.5 text-sm font-bold text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors shadow-sm">
        <i class="fas fa-arrow-left mr-2"></i> 返回微调图谱
      </button>
      <button 
        :disabled="fatalErrors.length > 0 || !checkComplete || isChecking"
        @click="generateSchemaAndProceed" 
        class="px-5 py-2.5 text-sm font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md shadow-indigo-600/30 flex items-center"
      >
        生成计算图谱并启动推演 <i class="fas fa-rocket ml-2"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  hierarchy: Array,       // [{ level_index, level_name, id_column, covariates: [...] }] All using original keys
  targetVariable: Object, // { name: '...', type: 'continuous' }
  tableData: Array,       // raw dataset rows
  displayMapping: Object, // { 'original': 'alias' }
  samplingMode: String,   // 'fast' or 'accurate'
  customDraws: Number,
  customTune: Number
});

const emit = defineEmits(['close', 'proceed']);

const isChecking = ref(false);
const checkComplete = ref(false);
const fatalErrors = ref([]);
const warnings = ref([]);

// Make mutable copies of data for "Fixing"
let localTableData = [];
let localHierarchy = [];

const runDiagnostics = () => {
  isChecking.value = true;
  fatalErrors.value = [];
  warnings.value = [];

  // Clone data to avoid mutating props directly
  localTableData = JSON.parse(JSON.stringify(props.tableData));
  localHierarchy = JSON.parse(JSON.stringify(props.hierarchy));

  setTimeout(() => {
    let activeColumns = [props.targetVariable.name];
    localHierarchy.forEach(level => {
      activeColumns = activeColumns.concat(level.covariates);
    });

    activeColumns.forEach(colName => {
      let missingCount = 0;
      let typeErrorCount = 0;
      const validNumbers = [];

      localTableData.forEach((row) => {
        const val = row[colName];
        if (val === null || val === undefined || val === '') {
          missingCount++;
        } else {
          const numVal = Number(val);
          if (isNaN(numVal)) typeErrorCount++;
          else validNumbers.push(numVal);
        }
      });

      const aliasName = props.displayMapping[colName] || colName;

      // Report Errors
      if (typeErrorCount > 0) {
        fatalErrors.value.push({ column: colName, alias: aliasName, message: `探测到 ${typeErrorCount} 处无法向量化的字符数据，要求纯数值。` });
      }

      if (missingCount > 0) {
        warnings.value.push({
          column: colName,
          alias: aliasName,
          type: 'missing',
          message: `探测到 ${missingCount} 处空洞数据 (NaN)，若直接推演将导致张量维度崩溃。`
        });
      }

      // Variance check
      if (validNumbers.length > 0) {
        const firstVal = validNumbers[0];
        const allSame = validNumbers.every(v => v === firstVal);
        const hasMissing = missingCount > 0;
        
        if (allSame && !hasMissing) { // If it has missing, filling mean makes it 0 variance anyway.
          warnings.value.push({
            column: colName,
            alias: aliasName,
            type: 'zero_variance',
            message: `此变量所有已知有效值均为 ${firstVal}，零方差特征会使得逆矩阵计算呈现奇异性 (Singular Matrix)，强烈建议剥离。`
          });
        }
      }
    });

    isChecking.value = false;
    checkComplete.value = true;
  }, 800);
};

// Auto fix: Mean Imputation
const applyAutoFix = (warning) => {
  const colName = warning.column;
  let sum = 0, count = 0;
  
  // Calculate mean
  localTableData.forEach(row => {
    const val = Number(row[colName]);
    if (!isNaN(val)) { sum += val; count++; }
  });
  
  const mean = count > 0 ? sum / count : 0;
  
  // Impute
  let imputedCount = 0;
  localTableData.forEach(row => {
    if (row[colName] === null || row[colName] === undefined || row[colName] === '') {
      row[colName] = mean;
      imputedCount++;
    }
  });
  
  console.log(`[AutoFix] ${colName} 已使用均值 ${mean.toFixed(2)} 填补了 ${imputedCount} 条记录。`);
  warnings.value = warnings.value.filter(w => w !== warning);
};

// Auto fix: Drop variable
const removeColumn = (colName) => {
  // Remove from hierarchy
  localHierarchy.forEach(level => {
    level.covariates = level.covariates.filter(cov => cov !== colName);
  });
  
  console.log(`[AutoFix] ${colName} 已被剥离出贝叶斯网络拓扑。`);
  warnings.value = warnings.value.filter(w => w.column !== colName);
};

const generateSchemaAndProceed = () => {
  emit('proceed', {
    status: 'success',
    hierarchy: localHierarchy,
    target: props.targetVariable,
    tableData: localTableData,
    displayMapping: props.displayMapping,
    samplingMode: props.samplingMode,
    customDraws: props.customDraws,
    customTune: props.customTune
  });
};

onMounted(() => {
  runDiagnostics();
});
</script>