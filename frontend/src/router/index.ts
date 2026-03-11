import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',          component: () => import('../views/FeedView.vue') },
    { path: '/explore',   component: () => import('../views/ExploreView.vue') },
    { path: '/athletes/:id', component: () => import('../views/AthleteView.vue') },
    { path: '/teams/:id',    component: () => import('../views/TeamView.vue') },
  ],
})
