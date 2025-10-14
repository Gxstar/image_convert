<template>
    <div class="sidebar-container">
        <!-- 顶部标题 -->
        <div class="sidebar-header">
            <h2 class="sidebar-title">图片格式转换器</h2>
        </div>

        <!-- 输入按钮区域 -->
        <div class="input-section">
            <el-button 
                type="primary" 
                icon="Picture"
                class="input-button"
                @click="selectImages"
            >
                选择图片
            </el-button>
            <el-button 
                type="primary" 
                icon="Folder"
                class="input-button"
                @click="selectFolder"
            >
                选择文件夹
            </el-button>
        </div>

        <!-- 输出区域 -->
        <div class="output-section">
            <div class="output-label">输出目录</div>
            <el-input 
                v-model="outputPath" 
                placeholder="请选择输出目录" 
                readonly
            >
                <template #append>
                    <el-button icon="FolderOpened" @click="selectOutputFolder" />
                </template>
            </el-input>
            <div class="selected-path" v-if="outputPath">
                已选择: {{ outputPath }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { Picture, Folder, FolderOpened } from '@element-plus/icons-vue'

// 输出路径
const outputPath = ref('')

// 选择图片方法
const selectImages = () => {
    console.log('选择图片')
    // 这里可以添加实际的选择图片逻辑
}

// 选择文件夹方法
const selectFolder = () => {
    console.log('选择文件夹')
    // 这里可以添加实际的选择文件夹逻辑
}

// 选择输出文件夹方法
const selectOutputFolder = () => {
    console.log('选择输出文件夹')
    // 这里可以添加实际的选择输出文件夹逻辑
    // 示例：设置一个模拟路径
    outputPath.value = '/example/output/path'
}
</script>

<style scoped>
.sidebar-container {
    height: 100vh;
    background-color: #f5f7fa;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.sidebar-header {
    text-align: center;
    padding-bottom: 20px;
    border-bottom: 1px solid #e4e7ed;
}

.sidebar-title {
    margin: 0;
    color: #303133;
    font-size: 24px;
    font-weight: 600;
}

.input-section {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.input-button {
    height: 40px;
    font-size: 16px;
}

.output-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.output-label {
    font-size: 16px;
    font-weight: 500;
    color: #606266;
}

.selected-path {
    font-size: 14px;
    color: #909399;
    margin-top: 5px;
    word-break: break-all;
}
</style>
