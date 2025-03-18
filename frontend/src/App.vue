<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="app">
    <RouterView />
    <Navbar />
  </div>
</template>

<style>
.app {
  min-height: 100vh;
  background: var(--background-color);
  color: var(--text-primary);
}
</style>
