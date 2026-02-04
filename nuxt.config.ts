// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['./assets/css/main.css'],
  ssr: true,
  modules: ['@nuxt/hints', '@nuxt/image'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
})