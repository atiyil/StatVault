<script setup lang="ts">
import type { Team } from '../api/client'

defineProps<{ team: Team }>()

const sportEmoji: Record<string, string> = {
  basketball: '🏀',
  football: '🏈',
  soccer: '⚽',
}
</script>

<template>
  <RouterLink :to="`/teams/${team._id}`" class="card p-4 flex gap-4 items-center hover:border-gray-700 hover:bg-gray-800/50 transition-all group">
    <img
      :src="team.logo_url"
      :alt="team.name"
      class="w-14 h-14 rounded-full object-cover bg-gray-800"
    />
    <div class="min-w-0 flex-1">
      <div class="font-semibold text-white group-hover:text-blue-400 transition-colors truncate">
        {{ team.name }}
      </div>
      <div class="text-sm text-gray-400">{{ team.league }}</div>
      <div class="text-xs text-gray-600 mt-0.5">
        {{ sportEmoji[team.sport] ?? '🏅' }} {{ team.city }}
      </div>
    </div>
  </RouterLink>
</template>
