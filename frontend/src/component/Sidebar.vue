<template>
  <div class="w-64 bg-white shadow-lg flex flex-col">
    <!-- 顶部标题 -->
    <div class="p-6 border-b border-gray-200">
      <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
        <el-icon><Picture /></el-icon>
        图片复制工具
      </h1>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="flex-1 p-4 space-y-4">
      <!-- 添加图片和文件夹按钮 -->
      <div class="space-y-2">
        <button 
          @click="emit('add-images')" 
          class="sidebar-button w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left font-medium text-gray-700 hover:text-primary"
        >
          <el-icon class="text-gray-500 hover:text-primary"><PictureFilled /></el-icon>
          <span>添加图片</span>
        </button>
        
        <button 
          @click="emit('add-folder')" 
          class="sidebar-button w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left font-medium text-gray-700 hover:text-primary"
        >
          <el-icon class="text-gray-500 hover:text-primary"><FolderAdd /></el-icon>
          <span>添加文件夹</span>
        </button>
      </div>
      
      <!-- 操作区域 -->
      <div class="pt-4 border-t border-gray-200">
        <h3 class="font-semibold text-gray-700 mb-3">操作</h3>
        
        <button 
          @click="emit('copy-images')" 
          class="w-full bg-primary hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <el-icon><CopyDocument /></el-icon>
          复制图片
        </button>
        
        <!-- 目标路径选择 -->
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">目标路径</label>
          <div class="flex gap-2">
            <el-input 
              v-model="targetPath" 
              placeholder="选择或输入目标文件夹路径" 
              class="flex-1"
            />
            <el-button 
              @click="emit('browse-target')" 
              type="primary"
              icon="FolderOpened"
              class="!bg-primary !border-primary hover:!bg-blue-600"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- 底部信息 -->
    <div class="p-4 border-t border-gray-200 text-xs text-gray-500">
      <p>支持 JPG, PNG, GIF, WEBP, AVIF, HEIF 格式</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  Picture, 
  PictureFilled, 
  FolderAdd, 
  CopyDocument, 
  FolderOpened 
} from '@element-plus/icons-vue'

// Emits
const emit = defineEmits(['add-images', 'add-folder', 'copy-images', 'browse-target'])

// 目标路径
const targetPath = ref('')
</script>

<style scoped>
.sidebar-button {
  transition: all 0.2s ease;
}

.sidebar-button:hover {
  background-color: #f3f4f6;
  transform: translateX(2px);
}
</style>
