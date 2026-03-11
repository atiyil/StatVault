<script setup lang="ts">
import type { Event } from '../api/client'

const props = defineProps<{ event: Event }>()

const sportEmoji: Record<string, string> = {
  basketball: '🏀',
  football: '🏈',
  soccer: '⚽',
}

function formatTime(iso: string) {
  const d = new Date(iso)
  return d.toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: 'numeric', minute: '2-digit',
  })
}

const statusLabel: Record<string, string> = {
  live: 'LIVE',
  upcoming: 'Upcoming',
  completed: 'Final',
}
</script>

<template>
  <div class="card p-5">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2 text-sm text-gray-500">
        <span>{{ sportEmoji[event.sport] ?? '🏅' }}</span>
        <span>{{ event.league }}</span>
      </div>
      <span :class="`badge-${event.status}`">{{ statusLabel[event.status] }}</span>
    </div>

    <!-- Teams + Score -->
    <div class="flex items-center gap-4">
      <!-- Home team -->
      <div class="flex-1 text-right">
        <RouterLink
          :to="`/teams/${event.home_team.id}`"
          class="font-semibold text-white hover:text-blue-400 transition-colors"
        >
          {{ event.home_team.name }}
        </RouterLink>
        <div class="text-xs text-gray-500 mt-0.5">HOME</div>
      </div>

      <!-- Score / vs -->
      <div class="text-center w-24 shrink-0">
        <template v-if="event.score">
          <div class="text-2xl font-bold tabular-nums text-white">
            {{ event.score.home }}
            <span class="text-gray-600 mx-1">–</span>
            {{ event.score.away }}
          </div>
        </template>
        <template v-else>
          <div class="text-sm font-medium text-gray-400">vs</div>
          <div class="text-xs text-gray-600 mt-1">{{ formatTime(event.start_time) }}</div>
        </template>
      </div>

      <!-- Away team -->
      <div class="flex-1">
        <RouterLink
          :to="`/teams/${event.away_team.id}`"
          class="font-semibold text-white hover:text-blue-400 transition-colors"
        >
          {{ event.away_team.name }}
        </RouterLink>
        <div class="text-xs text-gray-500 mt-0.5">AWAY</div>
      </div>
    </div>

    <!-- Venue -->
    <div v-if="event.venue" class="mt-3 text-xs text-gray-600 text-center">
      📍 {{ event.venue }}
    </div>

    <!-- Final date for completed -->
    <div v-if="event.status === 'completed'" class="mt-1 text-xs text-gray-600 text-center">
      {{ formatTime(event.start_time) }}
    </div>
  </div>
</template>
