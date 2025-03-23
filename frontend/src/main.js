import './assets/main.css'

import { createApp, markRaw } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query';


// Setup the query client with your custom configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      cacheTime: 10 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
});


const app = createApp(App)
const pinia = createPinia()

pinia.use(({ store }) => {
  store.router = markRaw(router)
})

// Options for toast notifications (optional)
const options = {
  // You can set options here (e.g., timeout, position, etc.)
  timeout: 3000,
  position: 'bottom-right',
};

app.use(pinia)
app.use(router)
app.use(Toast, options)

// Provide the queryClient to the Vue app
app.use(VueQueryPlugin, {
  queryClient,
  enableDevtoolsV6Plugin: true,
})


app.mount('#app')
