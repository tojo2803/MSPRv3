import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/home.vue';
import PredictionGraphs from '../components/predictionGraphs.vue';
import Graphiques from '../components/predictionGraphs.vue';
import Prediction from '../components/TestPrediction.vue';
import USMortalite from '../components/USMortalite.vue';
import Data from '../components/Data.vue';
import Confidentialite from '../components/Confidentialite.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/graphiques', component: Graphiques },
  { path: '/prediction', component: Prediction },
  { path: '/prediction-graphs',name: 'PredictionGraphs', component: PredictionGraphs},
  // route pour faciliter la scalabilité
  { path: '/data', component: Data },
  { path: '/us-mortalite', component: USMortalite },
  { path: '/confidentialite', name: 'Confidentialite', component: Confidentialite },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;