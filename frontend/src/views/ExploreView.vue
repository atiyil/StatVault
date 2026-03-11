<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { athleteApi, teamApi, type Athlete, type Team } from '../api/client'
import AthleteCard from '../components/AthleteCard.vue'
import TeamCard from '../components/TeamCard.vue'

const sports = ['All', 'Basketball', 'Football', 'Soccer']
const selectedSport = ref('All')
const tab = ref<'athletes' | 'teams'>('athletes')
const query = ref('')

const athletes = ref<Athlete[]>([])
const teams = ref<Team[]>([])
const loading = ref(true)

async function load() {
  loading.value = true
  const sport = selectedSport.value === 'All' ? undefined : selectedSport.value.toLowerCase()
  const q = query.value.trim() || undefined

  const [a, t] = await Promise.all([
    athleteApi.list({ sport, q }),
    teamApi.list({ sport, q }),
  ])
  athletes.value = a.items
  teams.value = t
  loading.value = false
}

onMounted(load)
watch([selectedSport, query], load)
</script>

<template>
  <div>
    <div class="flex flex-col sm:flex-row gap-4 mb-6">
      <input
        v-model="query"
        type="text"
        placeholder="Search athletes or teams…"
        class="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-blue-500"
      />
      <div class="flex gap-1">
        <button
          v-for="sport in sports"
          :key="sport"
          @click="selectedSport = sport"
          class="sport-pill"
          :class="selectedSport === sport
            ? 'bg-blue-600 text-white'
            : 'bg-gray-900 text-gray-400 hover:text-white border border-gray-800'"
        >
          {{ sport }}
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 border-b border-gray-800 mb-6">
      <button
        @click="tab = 'athletes'"
        class="px-4 py-2 text-sm font-medium border-b-2 transition-colors"
        :class="tab === 'athletes'
          ? 'border-blue-500 text-blue-400'
          : 'border-transparent text-gray-500 hover:text-gray-300'"
      >
        Athletes ({{ athletes.length }})
      </button>
      <button
        @click="tab = 'teams'"
        class="px-4 py-2 text-sm font-medium border-b-2 transition-colors"
        :class="tab === 'teams'
          ? 'border-blue-500 text-blue-400'
          : 'border-transparent text-gray-500 hover:text-gray-300'"
      >
        Teams ({{ teams.length }})
      </button>
    </div>

    <div v-if="loading" class="text-gray-500 text-center py-12">Loading…</div>

    <div v-else-if="tab === 'athletes'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      <AthleteCard v-for="a in athletes" :key="a._id" :athlete="a" />
      <div v-if="!athletes.length" class="col-span-3 text-center text-gray-600 py-12">
        No athletes found.
      </div>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      <TeamCard v-for="t in teams" :key="t._id" :team="t" />
      <div v-if="!teams.length" class="col-span-3 text-center text-gray-600 py-12">
        No teams found.
      </div>
    </div>
  </div>
</template>
