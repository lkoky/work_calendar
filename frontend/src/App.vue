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
  background: var(--color-bg-app);
  position: relative;
  box-sizing: border-box;
  transition: background 0.4s ease;
  /* overflow-x: hidden; */
}

.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(var(--color-grid-line) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-grid-line) 1px, transparent 1px);
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
  background: radial-gradient(circle, var(--color-glow) 0%, transparent 50%);
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
