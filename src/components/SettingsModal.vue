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

                    <!-- External API (Ollama) Settings -->
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

                    <!-- Built-in Light Model (GGUF) Settings -->
                    <div v-if="config.provider === 'llama_cpp'" class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm animate-fade-in">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">本地 GGUF 模型库管理</label>
                        <div class="flex items-center text-[11px] text-slate-500 mb-4 bg-slate-50 p-3 rounded-lg border border-slate-100 italic">
                            <span>模型存放目录: </span>
                            <span class="font-mono text-indigo-600 bg-white px-1 py-0.5 rounded border border-slate-200 mx-1">{{ localModelsDir }}</span>
                            <button @click="openModelsDir" class="ml-1 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 w-6 h-6 rounded flex items-center justify-center transition-colors" title="在资源管理器中打开">
                                <i class="far fa-folder-open"></i>
                            </button>
                        </div>
                        
                        <div v-if="localModels.length === 0" class="mb-5 flex flex-col items-center justify-center p-6 bg-rose-50 border border-rose-200 rounded-xl text-center">
                            <i class="fas fa-box-open text-rose-300 text-3xl mb-3"></i>
                            <div class="text-sm font-bold text-rose-700 mb-1">该目录下暂无任何 .gguf 模型文件</div>
                            <div class="text-xs text-rose-600/80 mb-4">您可以自行下载诸如 Llama3.gguf/Qwen.gguf 放入该文件夹。</div>
                            
                            <div class="w-full text-left bg-white p-3 rounded-lg border border-rose-100 shadow-sm">
                                <div class="text-[10px] font-bold text-slate-500 mb-2">或者在此处复制下载命令 (国内镜像):</div>
                                <div class="font-mono text-[9px] bg-slate-800 text-emerald-400 p-2 rounded break-all select-all overflow-x-auto hide-scrollbar leading-tight">
                                    # Windows PowerShell 下载 (Qwen-1.5-1.8B-Chat约1GB)
                                    <br>
                                    New-Item -ItemType Directory -Force -Path "$HOME\.deepbayes\models"; Invoke-WebRequest -Uri "https://hf-mirror.com/Qwen/Qwen1.5-1.8B-Chat-GGUF/resolve/main/qwen1_5-1_8b-chat-q4_k_m.gguf" -OutFile "$HOME\.deepbayes\models\qwen1_5-1_8b-chat-q4_k_m.gguf"
                                </div>
                            </div>
                        </div>

                        <div v-else class="mb-4">
                            <label class="block text-xs font-bold text-slate-700 mb-2">挂载的战斗序列 (选择模型)</label>
                            <div class="space-y-2">
                                <div v-for="mod in localModels" :key="mod.name" @click="config.gguf_path = mod.path" :class="config.gguf_path === mod.path ? 'border-indigo-500 bg-indigo-50/50 ring-1 ring-indigo-500' : 'border-slate-200 hover:border-indigo-300 bg-white'" class="flex items-center justify-between p-3 border rounded-xl cursor-pointer transition-all">
                                    <div class="flex items-center overflow-hidden">
                                        <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center mr-3 shrink-0"><i class="fas fa-cube text-slate-500"></i></div>
                                        <div class="truncate">
                                            <div class="text-xs font-bold text-slate-800 truncate" :title="mod.name">{{ mod.name }}</div>
                                            <div class="text-[10px] text-slate-400 mt-0.5">{{ mod.size_mb }} MB • GGUF</div>
                                        </div>
                                    </div>
                                    <div v-if="config.gguf_path === mod.path" class="text-indigo-600 shrink-0 ml-2"><i class="fas fa-check-circle text-lg"></i></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex space-x-3">
                            <button @click="fetchLocalModels" class="flex-1 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-bold rounded-lg transition-colors flex items-center justify-center">
                                <i class="fas fa-sync-alt mr-2"></i> 重新扫描
                            </button>
                        </div>
                    </div>
                 </div>
                 
                 <!-- Advanced Configuration (Prompt and Temp) -->
                 <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm mt-5 mb-5 animate-fade-in max-w-2xl mx-auto">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-4"><i class="fas fa-sliders-h mr-2"></i>引擎高阶指令与发散度配置</label>
                    <div class="mb-4">
                        <label class="block text-xs font-bold text-slate-700 mb-1">人格与角色设定 (System Prompt) <span class="font-normal text-[10px] text-slate-400">引导大模型的输出口吻与焦点</span></label>
                        <textarea v-model="config.system_prompt" rows="3" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent custom-scrollbar leading-relaxed" placeholder="如：你现在是首席系统调优专家..."></textarea>
                        <div class="flex justify-end mt-1">
                            <button @click="resetPrompt" class="text-[9px] text-indigo-500 hover:text-indigo-700 underline">恢复默认场景设定</button>
                        </div>
                    </div>
                    <div class="mb-5">
                       <label class="flex justify-between text-xs font-bold text-slate-700 mb-2">
                           <span>生成发散度 / 温度 (Temperature)</span>
                           <span class="text-indigo-600 bg-indigo-50 px-2 rounded-sm font-mono">{{ config.temperature }}</span>
                       </label>
                       <input type="range" v-model.number="config.temperature" min="0" max="1" step="0.1" class="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-500">
                       <div class="flex justify-between text-[9px] text-slate-400 mt-1">
                           <span>0.0 (最保守、严谨)</span>
                           <span>1.0 (最具创造性、发散)</span>
                       </div>
                    </div>
                 </div>

                 <div class="flex justify-center max-w-2xl mx-auto">
                    <button @click="testLlmConnection" :disabled="config.provider === 'llama_cpp' && (!config.gguf_path || localModels.length === 0)" class="w-full py-3 bg-slate-800 hover:bg-slate-900 disabled:bg-slate-300 disabled:cursor-not-allowed text-white text-sm font-bold rounded-xl shadow transition-colors flex items-center justify-center">
                        <i v-if="testingLlm" class="fas fa-spinner fa-spin mr-2"></i>
                        <i v-else class="fas fa-save mr-2"></i>
                        保存全局配置与引擎指引
                    </button>
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
   ollama_model: 'qwen',
   gguf_path: '',
   system_prompt: '',
   temperature: 0.3
});

const defaultPrompt = "你现在是 DeepBayes 平台的首席系统调优与安全风险专家。目前系统遭遇了一次参数扰动评估（压力测试）。请结合相关数据与下方提取的参考预案（如有），用专业、简洁的语言给出战术性的行动指导，避免废话。";

const testingLlm = ref(false);
const ragFiles = ref([]);
const localModels = ref([]);
const localModelsDir = ref('~/.deepbayes/models');

const resetPrompt = () => {
    config.value.system_prompt = defaultPrompt;
};

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

const fetchLocalModels = async () => {
    try {
        const res = await fetch('http://127.0.0.1:18521/api/settings/local_models');
        if(res.ok) {
            const data = await res.json();
            localModels.value = data.models || [];
            if(data.models_dir) localModelsDir.value = data.models_dir;
            
            // Auto-select first model if empty
            if(!config.value.gguf_path && localModels.value.length > 0) {
                config.value.gguf_path = localModels.value[0].path;
            }
        }
    } catch(e) {
        console.warn("Failed to fetch local GGUF models", e);
    }
};

const openModelsDir = async () => {
    try {
        await fetch('http://127.0.0.1:18521/api/settings/open_models_dir');
    } catch(e) {
        // Ignore failure
    }
};

const fetchRagFiles = async () => {
    try {
        const res = await fetch('http://127.0.0.1:18521/api/settings/rag/list');
        if(res.ok) {
            const data = await res.json();
            ragFiles.value = data.files || [];
            dbStatus.value = 'ready'; // Mark DB as initialized if we can fetch
        }
    } catch(e) {
        console.warn("Failed to fetch RAG files", e);
        dbStatus.value = 'offline';
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
        fetchLocalModels();
    }
});

</script>
