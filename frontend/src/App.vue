<script setup>
import Sidebar from './component/Sidebar.vue'
import Imagelist from './component/Imagelist.vue'
</script>

<template>
  <div class="app-container">
    <el-row>
      <el-col :span="6">
        <Sidebar />
      </el-col>
      <el-col :span="18">
        <Imagelist />
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.app-container {
    height: 100vh;
    background-color: #f5f5f5;
}
</style>
