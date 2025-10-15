<script setup>
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import Sidebar from './component/Sidebar.vue'
import Imagelist from './component/Imagelist.vue'
import { useImageStore } from './stores/imageStore'

// 使用图片store
const imageStore = useImageStore()

// 隐藏的文件输入元素
const fileInput = ref(null)
const folderInput = ref(null)
const targetFolderInput = ref(null)

// 初始化文件输入
onMounted(() => {
  // 创建隐藏的文件输入元素
  createHiddenInputs()
})

// 创建隐藏的文件输入元素
const createHiddenInputs = () => {
  // 这些元素会在需要时动态创建和使用
}

// 处理添加图片
const handleAddImages = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.multiple = true
  input.onchange = (e) => {
    const files = Array.from(e.target.files)
    imageStore.addImages(files)
  }
  input.click()
}

// 处理添加文件夹
const handleAddFolder = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.webkitdirectory = true
  input.directory = true
  input.multiple = true
  input.onchange = (e) => {
    const files = Array.from(e.target.files)
    imageStore.addImages(files)
  }
  input.click()
}

// 处理浏览目标文件夹
const handleBrowseTarget = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.webkitdirectory = true
  input.directory = true
  input.onchange = (e) => {
    if (e.target.files.length > 0) {
      const folderPath = e.target.files[0].webkitRelativePath.split('/')[0]
      imageStore.targetPath = folderPath // 实际应用中这里应该是完整路径
    }
  }
  input.click()
}

// 处理复制图片
const handleCopyImages = () => {
  const result = imageStore.copyImages()
  if (result.success) {
    ElMessage.success(result.message)
  } else {
    ElMessage.warning(result.message)
  }
}

// 处理清空所有图片
const handleClearAll = async () => {
  if (imageStore.images.length === 0) return
  
  try {
    await ElMessageBox.confirm(
      '确定要清空所有图片吗？',
      '清空确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    imageStore.clearAllImages()
    ElMessage.success('已清空所有图片')
  } catch {
    // 用户取消操作
  }
}

// 处理拖拽文件
const handleDropFiles = (files) => {
  imageStore.addImages(files)
}

// 处理移除单个图片
const handleRemoveImage = (imageId) => {
  const imageIndex = imageStore.images.findIndex(img => img.id === imageId)
  if (imageIndex !== -1) {
    // 释放图片URL
    URL.revokeObjectURL(imageStore.images[imageIndex].url)
    // 从数组中移除图片
    imageStore.images.splice(imageIndex, 1)
  }
}
</script>

<template>
  <div class="app-container">
    <div class="flex h-screen overflow-hidden">
      <!-- 侧边栏 -->
      <Sidebar 
        @add-images="handleAddImages"
        @add-folder="handleAddFolder"
        @copy-images="handleCopyImages"
        @browse-target="handleBrowseTarget"
      />
      
      <!-- 主内容区域 -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <Imagelist 
          :images="imageStore.images"
          @add-images="handleAddImages"
          @add-folder="handleAddFolder"
          @clear-all="handleClearAll"
          @drop-files="handleDropFiles"
          @remove-image="handleRemoveImage"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  height: 100vh;
  background-color: #f9fafb;
}
</style>
