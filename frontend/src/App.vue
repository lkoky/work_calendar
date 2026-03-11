<template>
  <div class="app-container">
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>
    <Calendar />
  </div>
</template>

<script setup lang="ts">
import Calendar from './components/Calendar.vue';
</script>

<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 20px;
  font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
  background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0d1428 100%);
  position: relative;
  box-sizing: border-box;
  /* overflow-x: hidden; */
}

.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 212, 255, 0.08) 0%, transparent 50%);
  animation: rotate 30s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  /* overflow-x: hidden; */
  
}
</style>
