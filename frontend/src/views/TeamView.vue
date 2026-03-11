<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { teamApi, eventApi, type Team, type Event } from '../api/client'
import EventCard from '../components/EventCard.vue'

const route = useRoute()
const team = ref<Team | null>(null)
const events = ref<Event[]>([])
const loading = ref(true)

const sportEmoji: Record<string, string> = {
  basketball: '🏀', football: '🏈', soccer: '⚽',
}

async function load(id: string) {
  loading.value = true
  const [t, e] = await Promise.all([
    teamApi.get(id),
    eventApi.list({ limit: 20 }),
  ])
  team.value = t
  events.value = e.items.filter(ev =>
    ev.home_team.id === id || ev.away_team.id === id
  ).slice(0, 5)
  loading.value = false
}

onMounted(() => load(route.params.id as string))
watch(() => route.params.id, id => load(id as string))
</script>

<template>
  <div v-if="loading" class="flex items-center justify-center h-64">
    <div class="text-gray-500">Loading…</div>
  </div>

  <div v-else-if="team" class="max-w-2xl mx-auto">
    <!-- Header -->
    <div class="card p-6 mb-6">
      <div class="flex gap-6 items-center">
        <img :src="team.logo_url" :alt="team.name" class="w-20 h-20 rounded-full bg-gray-800" />
        <div>
          <h1 class="text-2xl font-bold text-white">{{ team.name }}</h1>
          <div class="flex gap-3 mt-2 text-sm text-gray-400">
            <span>{{ sportEmoji[team.sport] ?? '🏅' }} {{ team.sport }}</span>
            <span>🏟 {{ team.league }}</span>
            <span>📍 {{ team.city }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Roster -->
    <div class="card p-5 mb-6">
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Roster</h2>
      <div class="divide-y divide-gray-800">
        <div
          v-for="entry in team.roster"
          :key="entry.athlete_id"
          class="py-3 flex justify-between items-center"
        >
          <RouterLink
            :to="`/athletes/${entry.athlete_id}`"
            class="font-medium text-white hover:text-blue-400 transition-colors"
          >
            {{ entry.name }}
          </RouterLink>
          <span class="text-sm text-gray-500 bg-gray-800 px-2 py-0.5 rounded font-mono">
            {{ entry.position }}
          </span>
        </div>
      </div>
    </div>

    <!-- Recent events -->
    <div v-if="events.length">
      <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Recent & Upcoming Games</h2>
      <div class="space-y-3">
        <EventCard v-for="e in events" :key="e._id" :event="e" />
      </div>
    </div>
    <div v-else class="text-center text-gray-600 py-8 text-sm">No games found.</div>
  </div>

  <div v-else class="text-center text-gray-600 py-20">Team not found.</div>
</template>
