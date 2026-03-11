<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { feedApi, type Event, type Athlete, type Team } from '../api/client'
import EventCard from '../components/EventCard.vue'
import AthleteCard from '../components/AthleteCard.vue'
import TeamCard from '../components/TeamCard.vue'

const feed = ref<Event[]>([])
const trending = ref<{ athletes: Athlete[]; teams: Team[] } | null>(null)
const loading = ref(true)

onMounted(async () => {
  const [feedData, trendingData] = await Promise.all([
    feedApi.feed(20),
    feedApi.trending(),
  ])
  feed.value = feedData
  trending.value = trendingData
  loading.value = false
})
</script>

<template>
  <div v-if="loading" class="flex items-center justify-center h-64">
    <div class="text-gray-500">Loading feed…</div>
  </div>

  <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Main feed -->
    <div class="lg:col-span-2 space-y-4">
      <h2 class="text-lg font-semibold text-gray-200 mb-4">Recent Results</h2>

      <!-- Live events first -->
      <div v-if="feed.filter(e => e.status === 'live').length" class="space-y-3">
        <div class="flex items-center gap-2 text-xs font-bold text-red-400 uppercase tracking-wider">
          <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          Live Now
        </div>
        <EventCard v-for="e in feed.filter(e => e.status === 'live')" :key="e._id" :event="e" />
      </div>

      <!-- Upcoming -->
      <div v-if="feed.filter(e => e.status === 'upcoming').length" class="space-y-3 mt-6">
        <div class="text-xs font-bold text-blue-400 uppercase tracking-wider">Upcoming</div>
        <EventCard v-for="e in feed.filter(e => e.status === 'upcoming')" :key="e._id" :event="e" />
      </div>

      <!-- Completed -->
      <div class="space-y-3 mt-6">
        <div class="text-xs font-bold text-gray-500 uppercase tracking-wider">Final Results</div>
        <EventCard v-for="e in feed.filter(e => e.status === 'completed')" :key="e._id" :event="e" />
      </div>
    </div>

    <!-- Sidebar -->
    <div class="space-y-8">
      <div v-if="trending">
        <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Trending Athletes</h3>
        <div class="space-y-2">
          <AthleteCard v-for="a in trending.athletes.slice(0, 5)" :key="a._id" :athlete="a" />
        </div>
      </div>

      <div v-if="trending">
        <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Trending Teams</h3>
        <div class="space-y-2">
          <TeamCard v-for="t in trending.teams" :key="t._id" :team="t" />
        </div>
      </div>
    </div>
  </div>
</template>
