// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: ['./assets/css/main.css'],
  ssr: true,
  modules: ['@nuxt/hints', '@nuxt/image', '@pinia/nuxt'],
  runtimeConfig: {
    public: {
      apiBase: (globalThis as any)?.process?.env?.NUXT_PUBLIC_API_BASE || '',
      wsBase: (globalThis as any)?.process?.env?.NUXT_PUBLIC_WS_BASE || '',
      stripePk: (globalThis as any)?.process?.env?.NUXT_PUBLIC_STRIPE_PK || '',
      googleMapsKey: (globalThis as any)?.process?.env?.NUXT_PUBLIC_GOOGLE_MAPS_KEY || ''
    }
  },
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
})