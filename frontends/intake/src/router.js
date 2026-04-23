import { createRouter, createWebHistory } from 'vue-router';

export const router = createRouter({
  history: createWebHistory('/intake/'),
  routes: [
    { path: '/new', name: 'new', component: () => import('./views/IntakeNew.vue') },
    { path: '/:intakeId', name: 'intake', component: () => import('./views/ClientIntake.vue'), props: true },
    { path: '/:pathMatch(.*)*', redirect: '/new' },
  ],
});
