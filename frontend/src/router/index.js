// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import UserProfile from '@/components/UserProfile.vue';
import LoginSignup from '@/components/LoginSignup.vue';
import EventDetail from '@/components/EventDetail.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/profile', component: UserProfile },
  { path: '/login', component: LoginSignup },
  { path: '/event/:id', component: EventDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
