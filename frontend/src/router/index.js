import { createRouter, createWebHistory } from 'vue-router';
import LoginSignup from '@/components/LoginSignup';
import HomePage from '@/components/HomePage';
import store from '@/store'; // Assuming you have Vuex store setup for state management

const routes = [
  {
    path: '/login',
    name: 'LoginSignup',
    component: LoginSignup,
    // Add a route guard to check if the user is already logged in
    beforeEnter: (to, from, next) => {
      if (store.state.isLoggedIn) {
        console.log("1. LoggedIn: ", store.state.isLoggedIn);
        next('/'); // Redirect to profile if logged in
      } else {
        next(); // Proceed to login page if not logged in
      }
    }
  },
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
    // Add a route guard to secure the profile route
    beforeEnter: (to, from, next) => {
      if (!store.state.isLoggedIn) {
        console.log("2. LoggedIn: ", store.state.isLoggedIn);
        next('/login'); // Redirect to login if not logged in
      } else {
        next(); // Proceed to profile page if logged in
      }
    }
  },
  // ... other routes
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;
