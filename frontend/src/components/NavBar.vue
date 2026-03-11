<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const isActive = (path: string) => route.path === path
</script>

<template>
  <nav class="border-b border-gray-800 bg-gray-950/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 flex items-center gap-6 h-14">
      <RouterLink to="/" class="flex items-center gap-2 font-bold text-lg text-white">
        <span class="text-2xl">🏆</span>
        <span>StatVault</span>
      </RouterLink>

      <div class="flex items-center gap-1 ml-4">
        <RouterLink
          to="/"
          class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
          :class="isActive('/') ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800'"
        >
          Feed
        </RouterLink>
        <RouterLink
          to="/explore"
          class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
          :class="isActive('/explore') ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800'"
        >
          Explore
        </RouterLink>
      </div>

      <div class="ml-auto text-xs text-gray-600 font-mono">v0.1.0-demo</div>
    </div>
  </nav>
</template>
