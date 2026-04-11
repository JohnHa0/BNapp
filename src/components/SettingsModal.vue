<template>
  <transition name="fade">
    <div v-if="show" class="fixed inset-0 bg-slate-900/60 backdrop-blur-md flex justify-center items-center z-[100]" @click.self="$emit('close')">
      <div class="w-full max-w-4xl max-h-[85vh] bg-slate-50 flex flex-col rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden border border-slate-700/50 scale-in-center">
        
        <!-- Header -->
        <div class="px-6 py-4 bg-slate-900 flex justify-between items-center shrink-0 border-b border-slate-700">
          <div class="flex items-center space-x-3">
             <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-neon-cyan flex items-center justify-center shadow-[0_0_15px_rgba(79,70,229,0.5)]">
                 <i class="fas fa-brain text-white text-sm"></i>
             </div>
             <div>
                 <h2 class="text-white font-bold tracking-wide">DeepBayes 智库与核心引擎枢纽</h2>
                 <p class="text-[10px] text-slate-400 font-mono">LLM & Knowledge RAG Configurator</p>
             </div>
          </div>
          <button @click="$emit('close')" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-rose-500 text-slate-400 hover:text-white flex items-center justify-center transition-colors">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <!-- Layout -->
        <div class="flex flex-1 overflow-hidden">
           
           <!-- Sidebar -->
           <div class="w-48 bg-white border-r border-slate-200 p-4 shrink-0 flex flex-col space-y-2">
              <button @click="activeTab = 'llm'" :class="activeTab === 'llm' ? 'bg-indigo-50 text-indigo-700 font-bold border-indigo-200' : 'text-slate-600 hover:bg-slate-50 border-transparent hover:text-slate-900'" class="w-full flex items-center px-4 py-3 rounded-xl border text-sm transition-all focus:outline-none">
                 <i class="fas fa-microchip w-6 text-center"></i> 大模型引擎
              </button>
              <button @click="activeTab = 'rag'" :class="activeTab === 'rag' ? 'bg-emerald-50 text-emerald-700 font-bold border-emerald-200' : 'text-slate-600 hover:bg-slate-50 border-transparent hover:text-slate-900'" class="w-full flex items-center px-4 py-3 rounded-xl border text-sm transition-all focus:outline-none">
                 <i class="fas fa-database w-6 text-center"></i> 战略私有智库
              </button>
              <div class="mt-auto pt-6 border-t border-slate-100 flex flex-col space-y-3">
                 <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest pl-2">System Status</div>
                 <div class="flex items-center text-xs text-slate-600 pl-2">
                    <span class="w-2 h-2 rounded-full border border-slate-400 flex items-center justify-center mr-2" :class="llmStatus === 'ready' ? 'bg-emerald-500 border-none animate-pulse' : 'bg-slate-300'"></span>
                    LLM: {{ llmStatus === 'ready' ? 'Connected' : 'Offline' }}
                 </div>
                 <div class="flex items-center text-xs text-slate-600 pl-2">
                    <span class="w-2 h-2 rounded-full border border-slate-400 flex items-center justify-center mr-2" :class="dbStatus === 'ready' ? 'bg-indigo-500 border-none animate-pulse' : 'bg-slate-300'"></span>
                    DB: {{ dbStatus === 'ready' ? 'Active' : 'Uninitialized' }}
                 </div>
              </div>
           </div>

           <!-- Content Area -->
           <div class="flex-1 bg-slate-50 overflow-y-auto p-6 relative">
              
              <!-- Tab 1: LLM Engine -->
              <div v-show="activeTab === 'llm'" class="animate-fade-in max-w-2xl mx-auto">
                 <h3 class="text-sm font-black text-slate-800 mb-6 flex items-center border-b pb-3">
                    <i class="fas fa-bolt text-amber-500 mr-2"></i> 算力平台与模型挂载配置
                 </h3>

                 <div class="space-y-5">
                    <!-- Engine Mode Selection -->
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                       <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">当前运行模式与提供商</label>
                       
                       <div class="grid grid-cols-2 gap-4">
                          <!-- Built-in Light Model -->
                          <div @click="config.provider = 'llama_cpp'" :class="config.provider==='llama_cpp' ? 'border-indigo-500 bg-indigo-50/50 shadow-md ring-2 ring-indigo-200' : 'border-slate-200 hover:border-indigo-300'" class="p-4 border-2 rounded-xl cursor-pointer transition-all relative">
                             <div v-if="config.provider==='llama_cpp'" class="absolute -top-3 -right-3 w-8 h-8 bg-indigo-500 text-white rounded-full flex items-center justify-center shadow-lg"><i class="fas fa-check"></i></div>
                             <div class="text-3xl text-indigo-500 mb-2"><i class="fas fa-leaf"></i></div>
                             <div class="font-bold text-slate-800 text-sm">内置轻量突击队 (GGUF)</div>
                             <div class="text-[11px] text-slate-500 mt-1 leading-relaxed">静默安装且绝对离线。依靠 llama.cpp 最高效利用纯 CPU 推理，开箱即用，适合基础战术意图分析。</div>
                          </div>
                          
                          <!-- External API (Ollama) -->
                          <div @click="config.provider = 'ollama'" :class="config.provider==='ollama' ? 'border-indigo-500 bg-indigo-50/50 shadow-md ring-2 ring-indigo-200' : 'border-slate-200 hover:border-indigo-300'" class="p-4 border-2 rounded-xl cursor-pointer transition-all relative">
                             <div v-if="config.provider==='ollama'" class="absolute -top-3 -right-3 w-8 h-8 bg-indigo-500 text-white rounded-full flex items-center justify-center shadow-lg"><i class="fas fa-check"></i></div>
                             <div class="text-3xl text-slate-800 mb-2"><i class="fas fa-network-wired"></i></div>
                             <div class="font-bold text-slate-800 text-sm">满血算力桥接 (Ollama)</div>
                             <div class="text-[11px] text-slate-500 mt-1 leading-relaxed">如果你本地拥有高端显卡并安装了 Ollama，可无缝代理至本地重型大语言模型 (如 Llama3)，获取顶级分析深度。</div>
                          </div>
                       </div>
                    </div>

                    <!-- Ollama Specific Settings -->
                    <div v-if="config.provider === 'ollama'" class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm animate-fade-in">
                       <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Ollama 接口配置</label>
                       
                       <div class="mb-4">
                          <label class="block text-xs font-bold text-slate-700 mb-1">API Endpoint (通常为 11434 端口)</label>
                          <input type="text" v-model="config.ollama_host" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono" placeholder="http://127.0.0.1:11434">
                       </div>
                       <div>
                          <label class="block text-xs font-bold text-slate-700 mb-1">目标模型标识 (Model Tag)</label>
                          <input type="text" v-model="config.ollama_model" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono" placeholder="llama3:latest 或 qwen:7b">
                       </div>
                       
                       <button @click="testLlmConnection" class="mt-4 px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold rounded-lg shadow transition-colors w-full flex items-center justify-center">
                          <i v-if="testingLlm" class="fas fa-spinner fa-spin mr-2"></i>
                          <i v-else class="fas fa-link mr-2"></i>
                          {{ testingLlm ? '正在通讯探测中...' : '测试引擎连接并保存' }}
                       </button>
                    </div>
                 </div>
              </div>

              <!-- Tab 2: RAG Knowledge Base -->
              <div v-show="activeTab === 'rag'" class="animate-fade-in h-full flex flex-col max-w-3xl mx-auto">
                 <h3 class="text-sm font-black text-slate-800 mb-4 flex items-center border-b pb-3 shrink-0">
                    <i class="fas fa-shield-alt text-emerald-500 mr-2"></i> RAG 私有战略知识防线构建
                 </h3>

                 <!-- Upload Zone -->
                 <div class="bg-white rounded-xl border-2 border-dashed border-slate-300 p-8 flex flex-col items-center justify-center text-center transition-colors hover:border-emerald-500 hover:bg-emerald-50/30 cursor-pointer shrink-0 mb-6" @click="$refs.fileInput.click()">
                    <input type="file" ref="fileInput" class="hidden" accept=".pdf,.docx,.txt" multiple @change="handleFileUpload">
                    <div class="w-16 h-16 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center text-3xl mb-3">
                       <i class="fas fa-cloud-upload-alt"></i>
                    </div>
                    <div class="font-bold text-slate-700 text-sm mb-1">点击或拖拽上传防损手册/战略研报</div>
                    <div class="text-xs text-slate-400 max-w-sm">
                       支持 PDF, DOCX, TXT 格式。系统将自动进行分词切片并转化为稠密向量 (Embedding) 沉淀至深层数据库中。数据 100% 留存在本地，绝无外泄风险。
                    </div>
                 </div>

                 <!-- File List -->
                 <div class="flex-1 flex flex-col bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                    <div class="bg-slate-50 px-4 py-3 border-b border-slate-200 flex justify-between items-center text-xs font-bold text-slate-600">
                       <span><i class="fas fa-hdd mr-1.5 text-slate-400"></i>本地数据库索引池 (ChromaDB)</span>
                       <button @click="fetchRagFiles" class="text-indigo-600 hover:text-indigo-800"><i class="fas fa-sync-alt mr-1"></i>刷新</button>
                    </div>
                    
                    <div class="flex-1 overflow-y-auto p-2 bg-slate-50/50">
                       <div v-if="ragFiles.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400">
                          <i class="fas fa-box-open text-3xl mb-2 opacity-50"></i>
                          <span class="text-xs">智能防御网尚未挂载任何战略文献</span>
                       </div>
                       
                       <div v-else class="space-y-2">
                          <div v-for="file in ragFiles" :key="file.id" class="bg-white p-3 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between group">
                             <div class="flex items-center overflow-hidden">
                                <i v-if="file.name.endsWith('.pdf')" class="fas fa-file-pdf text-rose-500 text-lg mr-3 shrink-0"></i>
                                <i v-else-if="file.name.endsWith('.docx')" class="fas fa-file-word text-blue-500 text-lg mr-3 shrink-0"></i>
                                <i v-else class="fas fa-file-alt text-slate-400 text-lg mr-3 shrink-0"></i>
                                
                                <div class="truncate pr-4">
                                   <div class="text-xs font-bold text-slate-700 truncate" :title="file.name">{{ file.name }}</div>
                                   <div class="text-[10px] text-slate-400 flex items-center mt-0.5">
                                      <span class="bg-emerald-100 text-emerald-700 px-1.5 py-[1px] rounded text-[9px] font-mono mr-2">{{ file.chunks }} Chunks</span>
                                      加载于 {{ file.timestamp }}
                                   </div>
                                </div>
                             </div>
                             <button @click="deleteRagFile(file.id)" class="w-8 h-8 rounded-full text-slate-300 hover:bg-rose-50 hover:text-rose-600 flex items-center justify-center transition-colors shrink-0 opacity-0 group-hover:opacity-100" title="自毁该文献碎片">
                                <i class="fas fa-trash-alt"></i>
                             </button>
                          </div>
                       </div>
                    </div>
                 </div>

              </div>

           </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  show: Boolean
});
const emit = defineEmits(['close', 'config-saved']);

const activeTab = ref('llm');
const llmStatus = ref('offline');
const dbStatus = ref('active');

const config = ref({
   provider: 'ollama',
   ollama_host: 'http://127.0.0.1:11434',
   ollama_model: 'qwen'
});

const testingLlm = ref(false);
const ragFiles = ref([]);

// Mock or Fetch existing config
const fetchConfig = async () => {
    try {
        const res = await fetch('http://127.0.0.1:18521/api/settings/get');
        if(res.ok) {
            const data = await res.json();
            config.value = { ...config.value, ...data };
            llmStatus.value = 'ready';
        }
    } catch(e) {
        console.warn("Failed to fetch settings from backend.");
    }
};

const testLlmConnection = async () => {
    testingLlm.value = true;
    try {
        const res = await fetch('http://127.0.0.1:18521/api/settings/llm/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config.value)
        });
        if(res.ok) {
            alert('✅ 大模型火力探测成功！引擎矩阵挂载完毕。');
            llmStatus.value = 'ready';
            emit('config-saved', config.value);
        } else {
            throw new Error((await res.json()).detail || '连通遭拒');
        }
    } catch(e) {
        alert('❌ 扫描失败: ' + e.message + '\n请检查 Ollama 服务是否在后台运行且模型标识正确。');
        llmStatus.value = 'offline';
    } finally {
        testingLlm.value = false;
    }
};

const fetchRagFiles = async () => {
    try {
        const res = await fetch('http://127.0.0.1:18521/api/settings/rag/list');
        if(res.ok) {
            const data = await res.json();
            ragFiles.value = data.files;
        }
    } catch(e) {
        console.warn("Failed to fetch RAG files", e);
    }
};

const handleFileUpload = async (e) => {
    const files = e.target.files;
    if(!files || files.length === 0) return;
    
    // Simulate upload directly for now or call real API
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }
    
    try {
        // Show loading state...
        const res = await fetch('http://127.0.0.1:18521/api/settings/rag/upload', {
            method: 'POST',
            body: formData
        });
        if(res.ok) {
            alert('🌐 核心知识防线注水完成！文件切片矩阵已封存入库。');
            fetchRagFiles();
        } else {
            const err = await res.json();
            alert('上传受阻: ' + (err.detail || '未知错误'));
        }
    } catch(err) {
        alert('无法连接至本地向量据库: ' + err.message);
    }
    
    // Clear input
    e.target.value = null;
};

const deleteRagFile = async (id) => {
    if(!confirm("⚠️ 确定要彻底销毁该份战略文献碎片吗？知识图谱将被重构。")) return;
    try {
        const res = await fetch(`http://127.0.0.1:18521/api/settings/rag/delete/${id}`, { method: 'DELETE' });
        if(res.ok) {
            fetchRagFiles();
        }
    } catch(e) {
        console.error("Delete failed", e);
    }
};

watch(() => props.show, (newVal) => {
    if(newVal) {
        fetchConfig();
        fetchRagFiles();
    }
});

</script>
