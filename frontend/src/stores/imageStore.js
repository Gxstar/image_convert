import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useImageStore = defineStore('image', () => {
  // 图片列表
  const images = ref([])
  
  // 目标路径
  const targetPath = ref('')
  
  // 支持的图片格式
  const supportedFormats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff', 'avif', 'heif', 'heic']
  
  // 添加图片
  const addImages = (files) => {
    const validImages = files.filter(file => {
      const extension = file.name.split('.').pop().toLowerCase()
      return supportedFormats.includes(extension)
    })
    
    validImages.forEach(file => {
      // 检查是否已存在相同文件
      const exists = images.value.some(img => 
        img.name === file.name && img.size === file.size
      )
      
      if (!exists) {
        const image = {
          id: `${file.name}-${file.size}`,
          name: file.name,
          size: file.size,
          url: URL.createObjectURL(file),
          file: file
        }
        images.value.push(image)
      }
    })
  }
  
  // 清空所有图片
  const clearAllImages = () => {
    // 释放所有图片的URL
    images.value.forEach(image => {
      URL.revokeObjectURL(image.url)
    })
    images.value = []
  }
  
  // 复制图片（模拟功能）
  const copyImages = () => {
    if (images.value.length === 0 || !targetPath.value.trim()) {
      return { success: false, message: '请添加图片并指定目标路径' }
    }
    
    // 在实际的Electron应用中，这里会调用Node.js的fs模块进行文件复制
    // 现在只是模拟操作
    return { 
      success: true, 
      message: `将复制 ${images.value.length} 张图片到: ${targetPath.value}` 
    }
  }
  
  // 获取总图片数量
  const getTotalImages = () => {
    return images.value.length
  }
  
  return {
    images,
    targetPath,
    addImages,
    clearAllImages,
    copyImages,
    getTotalImages
  }
})