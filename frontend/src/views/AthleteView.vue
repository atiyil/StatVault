<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { athleteApi, eventApi, type Athlete, type Event } from '../api/client'
import EventCard from '../components/EventCard.vue'

const route = useRoute()
const athlete = ref<Athlete | null>(null)
const events = ref<Event[]>([])
const loading = ref(true)

const statLabels: Record<string, Record<string, string>> = {
  basketball: { ppg: 'PPG', rpg: 'RPG', apg: 'APG', gp: 'GP' },
  football:   { pass_yds: 'Pass Yds', pass_td: 'Pass TD', int: 'INT', qbr: 'QBR' },
  soccer:     { goals: 'Goals', assists: 'Assists', matches: 'Matches', shots_pg: 'Shots/G' },
}

const sportEmoji: Record<string, string> = {
  basketball: '🏀', football: '🏈', soccer: '⚽',
}

async function load(id: string) {
  loading.value = true
  const [a, e] = await Promise.all([
    athleteApi.get(id),
    eventApi.list({ sport: undefined, limit: 5 }),
  ])
  athlete.value = a
  // Show recent events for athlete's team
  events.value = e.items.filter(ev =>
    ev.home_team.id === a.team_id || ev.away_team.id === a.team_id
  ).slice(0, 3)
  loading.value = false
}

onMounted(() => load(route.params.id as string))
watch(() => route.params.id, id => load(id as string))
</script>

<template>
  <div v-if="loading" class="flex items-center justify-center h-64">
    <div class="text-gray-500">Loading…</div>
  </div>

  <div v-else-if="athlete" class="max-w-2xl mx-auto">
    <!-- Header -->
    <div class="card p-6 mb-6">
      <div class="flex gap-6 items-start">
        <img
          :src="athlete.image_url"
          :alt="athlete.name"
          class="w-24 h-24 rounded-full bg-gray-800"
        />
        <div class="flex-1 min-w-0">
          <h1 class="text-2xl font-bold text-white">{{ athlete.name }}</h1>
          <div class="text-gray-400 mt-1">
            {{ athlete.position }} ·
            <RouterLink :to="`/teams/${athlete.team_id}`" class="text-blue-400 hover:underline">
              {{ athlete.team_name }}
            </RouterLink>
          </div>
          <div class="flex gap-3 mt-3 text-sm text-gray-500">
            <span>{{ sportEmoji[athlete.sport] ?? '🏅' }} {{ athlete.sport }}</span>
            <span>🌍 {{ athlete.nationality }}</span>
            <span>🎂 Age {{ athlete.age }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="card p-5 mb-6">
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Season Stats</h2>
      <div class="grid grid-cols-4 gap-4">
        <div
          v-for="[key, value] in Object.entries(athlete.stats)"
          :key="key"
          class="text-center"
        >
          <div class="text-2xl font-bold text-white tabular-nums">{{ value }}</div>
          <div class="text-xs text-gray-500 mt-1">
            {{ (statLabels[athlete.sport] ?? {})[key] ?? key.toUpperCase() }}
          </div>
        </div>
      </div>
    </div>

    <!-- Recent team events -->
    <div v-if="events.length">
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Recent Games</h2>
      <div class="space-y-3">
        <EventCard v-for="e in events" :key="e._id" :event="e" />
      </div>
    </div>
  </div>

  <div v-else class="text-center text-gray-600 py-20">Athlete not found.</div>
</template>
