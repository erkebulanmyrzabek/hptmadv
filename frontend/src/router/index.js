import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Profile from '../views/Profile.vue';
import Hackathon from '../views/Hackathon.vue';
import HackathonDetailView from '../views/HackathonDetailView.vue';
import { useAuthStore } from '../stores/auth';
import ProfileSettings from '../views/ProfileSettings.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile/settings',
    name: 'ProfileSettings',
    component: ProfileSettings,
    meta: { requiresAuth: true },
  },
  {
    path: '/hackathons',
    name: 'Hackathon',
    component: Hackathon,
  },
  {
    path: '/hackathons/:id',
    name: 'HackathonDetail',
    component: HackathonDetailView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = !!authStore.token;
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;