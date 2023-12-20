import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../views/LandingPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LandingPage,
  },
  {
    path: '/listening',
    name: 'ListeningPage',
    component: () => import('@/views/ListeningPage.vue')
  },
  {
    path: '/vocabulary',
    name: 'VocabularyPage',
    component: () => import('@/views/VocabularyPage.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
