import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export interface Athlete {
  _id: string
  name: string
  sport: string
  position: string
  team_id: string
  team_name: string
  nationality: string
  age: number
  stats: Record<string, number>
  image_url: string
}

export interface RosterEntry {
  athlete_id: string
  name: string
  position: string
}

export interface Team {
  _id: string
  name: string
  sport: string
  league: string
  city: string
  logo_url: string
  roster: RosterEntry[]
}

export interface TeamRef { id: string; name: string }

export interface Event {
  _id: string
  sport: string
  league: string
  home_team: TeamRef
  away_team: TeamRef
  start_time: string
  status: 'upcoming' | 'live' | 'completed'
  score: { home: number; away: number } | null
  venue: string
}

export interface Paginated<T> {
  items: T[]
  total: number
  page: number
  limit: number
}

export const athleteApi = {
  list: (params?: { sport?: string; q?: string; page?: number; limit?: number }) =>
    api.get<Paginated<Athlete>>('/athletes', { params }).then(r => r.data),
  get: (id: string) =>
    api.get<Athlete>(`/athletes/${id}`).then(r => r.data),
}

export const teamApi = {
  list: (params?: { sport?: string; q?: string }) =>
    api.get<Team[]>('/teams', { params }).then(r => r.data),
  get: (id: string) =>
    api.get<Team>(`/teams/${id}`).then(r => r.data),
}

export const eventApi = {
  list: (params?: { sport?: string; status?: string; page?: number; limit?: number }) =>
    api.get<Paginated<Event>>('/events', { params }).then(r => r.data),
  get: (id: string) =>
    api.get<Event>(`/events/${id}`).then(r => r.data),
}

export const feedApi = {
  feed: (limit = 20) =>
    api.get<Event[]>('/feed', { params: { limit } }).then(r => r.data),
  trending: (sport?: string) =>
    api.get<{ athletes: Athlete[]; teams: Team[] }>('/trending', { params: { sport } }).then(r => r.data),
}
