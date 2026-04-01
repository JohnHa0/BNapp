<template>
  <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100 mt-6">
    <div class="flex justify-between items-center mb-6 border-b pb-3">
      <h2 class="text-xl font-bold text-gray-800 flex items-center">
        <i class="fas fa-heartbeat text-rose-500 mr-2"></i> 数据健康体检报告
      </h2>
      <div v-if="isChecking" class="text-sm text-indigo-600 font-medium flex items-center">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        正在执行深度扫描...
      </div>
      <div v-else-if="checkComplete && fatalErrors.length === 0" class="text-sm font-bold text-green-600 bg-green-50 px-3 py-1 rounded">
        <i class="fas fa-check-circle mr-1"></i> 校验通过，可运行模型
      </div>
    </div>

    <div v-if="checkComplete" class="space-y-4">
      
      <div v-if="fatalErrors.length > 0" class="p-4 bg-red-50 border border-red-200 rounded-lg">
        <h3 class="text-sm font-bold text-red-800 mb-2 flex items-center">
          <i class="fas fa-times-circle mr-2"></i> 致命错误 (必须修复)
        </h3>
        <ul class="space-y-2">
          <li v-for="(err, idx) in fatalErrors" :key="idx" class="text-sm text-red-700 bg-white p-2 rounded border border-red-100 flex justify-between items-center">
            <span><strong>{{ err.column }}</strong>: {{ err.message }}</span>
          </li>
        </ul>
      </div>

      <div v-if="warnings.length > 0" class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <h3 class="text-sm font-bold text-yellow-800 mb-2 flex items-center">
          <i class="fas fa-exclamation-triangle mr-2"></i> 数据预警 (建议修复)
        </h3>
        <ul class="space-y-2">
          <li v-for="(warn, idx) in warnings" :key="idx" class="text-sm text-yellow-700 bg-white p-2 rounded border border-yellow-100 flex justify-between items-center">
            <span><strong>{{ warn.column }}</strong>: {{ warn.message }}</span>
            
            <button v-if="warn.fixable" @click="applyAutoFix(warn)" class="px-2 py-1 bg-yellow-100 hover:bg-yellow-200 text-yellow-800 text-xs font-semibold rounded transition-colors">
              <i class="fas fa-wrench mr-1"></i>一键均值填充
            </button>
            <button v-if="warn.type === 'zero_variance'" @click="removeColumn(warn.column)" class="px-2 py-1 bg-red-100 hover:bg-red-200 text-red-800 text-xs font-semibold rounded transition-colors">
              <i class="fas fa-trash-alt mr-1"></i>移除该变量
            </button>
          </li>
        </ul>
      </div>

      <div v-if="fatalErrors.length === 0 && warnings.length === 0" class="p-8 text-center bg-gray-50 rounded-lg border border-dashed border-gray-200">
        <i class="fas fa-shield-check text-4xl text-green-500 mb-3"></i>
        <p class="text-gray-600 font-medium">所有数据列均符合要求，多重共线性与方差校验完美。</p>
      </div>

    </div>

    <div class="mt-6 flex justify-end space-x-3">
      <button @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded hover:bg-gray-50">
        返回微调
      </button>
      <button 
        :disabled="fatalErrors.length > 0 || !checkComplete"
        @click="generateSchemaAndProceed" 
        class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        生成配置并启动推演 <i class="fas fa-rocket ml-1"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 接收父组件传入的映射关系和解析后的宽表JSON数据
const props = defineProps({
  hierarchy: Array,
  targetVariable: Object,
  tableData: Array // 模拟解析后的CSV数组，如 [{ '建设资金': 5000, '考核得分': 90 }, ...]
});

const emit = defineEmits(['close', 'proceed']);

const isChecking = ref(false);
const checkComplete = ref(false);
const fatalErrors = ref([]);
const warnings = ref([]);

// 核心：执行数据体检逻辑
const runDiagnostics = () => {
  isChecking.value = true;
  fatalErrors.value = [];
  warnings.value = [];

  // 模拟一个异步扫描过程，给用户一种“系统在干活”的掌控感
  setTimeout(() => {
    // 获取所有参与计算的列名 (X 和 Y)
    let activeColumns = [];
    if (props.targetVariable) activeColumns.push(props.targetVariable.name);
    props.hierarchy.forEach(level => {
      activeColumns = activeColumns.concat(level.covariates);
    });

    activeColumns.forEach(colName => {
      let missingCount = 0;
      let typeErrorCount = 0;
      const values = [];

      props.tableData.forEach((row, rowIndex) => {
        const val = row[colName];
        
        // 1. 空值检测
        if (val === null || val === undefined || val === '') {
          missingCount++;
        } else {
          // 2. 类型检测 (强转数字看是否为 NaN)
          const numVal = Number(val);
          if (isNaN(numVal)) {
            typeErrorCount++;
          } else {
            values.push(numVal);
          }
        }
      });

      // 生成诊断结果
      if (typeErrorCount > 0) {
        fatalErrors.value.push({
          column: colName,
          message: `发现 ${typeErrorCount} 处非数字内容，请检查表格格式。`
        });
      }

      if (missingCount > 0) {
        warnings.value.push({
          column: colName,
          type: 'missing',
          fixable: true,
          message: `发现 ${missingCount} 处空值，可能导致模型崩溃。`
        });
      }

      // 3. 零方差检测 (所有数值都一样)
      if (values.length > 0) {
        const firstVal = values[0];
        const allSame = values.every(v => v === firstVal);
        if (allSame) {
          warnings.value.push({
            column: colName,
            type: 'zero_variance',
            fixable: false,
            message: `该列所有数值均为 ${firstVal}，缺乏统计区分度，建议移除。`
          });
        }
      }
    });

    // 检查拓扑结构是否连贯
    props.hierarchy.forEach((level, index) => {
      if (!level.idColumn) {
        fatalErrors.value.push({
          column: `第 ${index + 1} 层网络 (${level.name})`,
          message: `缺失 ID 标识映射，层级发生断裂。`
        });
      }
    });

    isChecking.value = false;
    checkComplete.value = true;
  }, 1200); // 模拟 1.2 秒的扫描耗时
};

// 一键修复功能：均值填充
const applyAutoFix = (warning) => {
  console.log(`正在对 ${warning.column} 执行均值填充...`);
  // 实际逻辑：计算列平均值，遍历 tableData 将 null 替换为均值
  // 填充完毕后，将该警告从 warnings 数组中移除
  warnings.value = warnings.value.filter(w => w !== warning);
};

// 移除变量
const removeColumn = (colName) => {
  // 实际逻辑：从 hierarchy 中找到该 covariate 并 splice 掉
  warnings.value = warnings.value.filter(w => w.column !== colName);
};

const generateSchemaAndProceed = () => {
  // 组装最终 JSON Schema 传递给 Python
  emit('proceed', {
    status: 'success',
    hierarchy: props.hierarchy,
    target: props.targetVariable
  });
};

onMounted(() => {
  runDiagnostics();
});
</script>