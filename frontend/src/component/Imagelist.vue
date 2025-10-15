<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- 顶部工具栏 -->
    <div class="bg-white border-b border-gray-200 p-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-800">图片预览</h2>
        <div class="flex items-center gap-4 text-sm text-gray-600">
          <span>{{ totalImages }} 张图片</span>
          <button 
            @click="emit('clear-all')" 
            class="text-red-500 hover:text-red-700"
          >
            <el-icon><Delete /></el-icon>
            清空
          </button>
        </div>
      </div>
    </div>
    
    <!-- 图片网格区域 -->
    <div 
      ref="dropZone" 
      class="flex-1 overflow-auto bg-gray-50"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @drop.prevent="handleDrop"
      :class="{ 'drag-over': isDragOver }"
    >
      <div v-if="images.length === 0" class="h-full flex flex-col items-center justify-center py-16 text-center">
        <el-icon class="text-6xl text-gray-300 mb-4"><UploadFilled /></el-icon>
        <h3 class="text-xl font-medium text-gray-600 mb-2">暂无图片</h3>
        <p class="text-gray-500 mb-6">点击侧边栏按钮添加图片或文件夹</p>
        <div class="flex gap-3">
          <button 
            @click="emit('add-images')" 
            class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            <el-icon><PictureFilled /></el-icon>
            添加图片
          </button>
          <button 
            @click="emit('add-folder')" 
            class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors"
          >
            <el-icon><FolderAdd /></el-icon>
            添加文件夹
          </button>
        </div>
      </div>
      
      <div v-else class="p-4 grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] gap-3">
        <div 
          v-for="image in images" 
          :key="image.id"
          class="border-2 border-transparent rounded-lg overflow-hidden transition-all duration-200 hover:border-blue-500 hover:shadow-lg hover:-translate-y-1 relative"
          @mouseenter="setHoveredImage(image.id)"
          @mouseleave="clearHoveredImage"
        >
          <!-- 移除按钮 - 鼠标悬停时显示 -->
          <button
            v-if="hoveredImageId === image.id"
            @click="handleRemoveImage(image)"
            class="absolute top-2 right-2 z-10 bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center transition-all duration-200 transform hover:scale-110 shadow-md"
            title="移除图片"
          >
            <el-icon class="text-xs"><Close /></el-icon>
          </button>
          
          <!-- 4:3 比例容器 -->
          <div class="relative aspect-[4/3]">
            <div v-if="isModernFormat(image.name)" class="w-full h-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
              <div class="text-center">
                <div class="text-xl mb-1">{{ getFormatIcon(image.name) }}</div>
                <div class="text-xs text-gray-600 font-medium">{{ image.name.split('.').pop().toUpperCase() }}</div>
              </div>
            </div>
            <img 
              v-else
              :src="image.url" 
              :alt="image.name" 
              class="w-full h-full object-cover"
              loading="lazy"
            />
            <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all duration-200"></div>
          </div>
          <div class="p-2 bg-white">
            <p class="font-medium text-xs text-gray-800 truncate">{{ image.name }}</p>
            <p class="text-xs text-gray-500">{{ formatFileSize(image.size) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Folder, Delete, UploadFilled, PictureFilled, FolderAdd, Close } from '@element-plus/icons-vue'

// 定义props
const props = defineProps({
  images: {
    type: Array,
    default: () => []
  }
})

// 定义emits
const emit = defineEmits([
  'add-images',
  'add-folder',
  'clear-all',
  'drop-files',
  'remove-image'
])

// 拖拽状态
const isDragOver = ref(false)

// 拖拽区域引用
const dropZone = ref(null)

// 鼠标悬停状态
const hoveredImageId = ref(null)

// 处理移除图片
const handleRemoveImage = async (image) => {
  try {
    await ElMessageBox.confirm(
      `确定要移除图片 "${image.name}" 吗？`,
      '移除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    emit('remove-image', image.id)
    ElMessage.success(`已移除图片 "${image.name}"`)
  } catch {
    // 用户取消操作
  }
}

// 设置鼠标悬停状态
const setHoveredImage = (imageId) => {
  hoveredImageId.value = imageId
}

// 清除鼠标悬停状态
const clearHoveredImage = () => {
  hoveredImageId.value = null
}

// 处理拖拽文件
const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  const files = Array.from(event.dataTransfer.files)
  const imageFiles = files.filter(file => file.type.startsWith('image/'))
  
  if (imageFiles.length > 0) {
    emit('drop-files', imageFiles)
    ElMessage.success(`成功添加 ${imageFiles.length} 张图片`)
  } else {
    ElMessage.warning('请拖拽图片文件')
  }
}

// 计算总图片数量
const totalImages = computed(() => props.images.length)

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 检查是否为现代图片格式（需要特殊处理）
const isModernFormat = (fileName) => {
  const extension = fileName.split('.').pop().toLowerCase()
  return ['heif', 'heic'].includes(extension)
}

// 获取文件格式图标
const getFormatIcon = (fileName) => {
  const extension = fileName.split('.').pop().toLowerCase()
  switch (extension) {
    case 'heif':
    case 'heic':
      return '🖼️'
    default:
      return '🖼️'
  }
}
</script>

<style scoped>
.drag-over {
  background-color: #dbeafe;
  border: 2px dashed #3b82f6;
}
</style>