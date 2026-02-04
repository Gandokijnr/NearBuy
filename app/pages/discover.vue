<template>
  <div class="min-h-screen px-4 sm:px-6 pt-16 md:pt-20 pb-6 bg-[#0A0F1E] text-[#F2F2F2]">
    <div class="mx-auto max-w-7xl">
      <div class="flex items-center gap-3 mb-4">
        <input v-model="query" type="search" placeholder="Search products..." class="w-full rounded-full bg-white/5 border border-white/10 px-4 py-3 outline-none focus:border-[#FF7A00]" @keyup.enter="doSearch"/>
        <button class="rounded-full bg-[#FF7A00] text-[#0A0F1E] px-4 py-3 font-semibold" @click="doSearch">Search</button>
      </div>

      <div class="flex items-center justify-between mb-3">
        <h2 class="text-xl font-semibold">Nearest Stores</h2>
        <button class="text-sm text-white/70" @click="refreshStores">Refresh</button>
      </div>

      <div v-if="locating" class="text-white/70">Detecting your location...</div>
      <div v-else-if="locError" class="text-[#FF7A00]">{{ locError }}</div>

      <div v-if="pending" class="text-white/70">Loading nearby stores...</div>
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        <NuxtLink v-for="s in stores || []" :key="s.id" :to="`/store/${s.id}`" class="rounded-xl bg-white/5 border border-white/10 p-3 hover:border-[#FF7A00]/50 transition-colors">
          <img v-if="s.image" :src="s.image" :alt="s.name" class="h-28 w-full object-cover rounded-lg mb-2"/>
          <div class="font-semibold truncate">{{ s.name }}</div>
          <div class="text-sm text-white/70">{{ s.distance_km?.toFixed(1) ?? '?' }} km</div>
        </NuxtLink>
      </div>

      <div v-if="queryResults && queryResults.length" class="mt-8">
        <h3 class="text-lg font-semibold mb-2">Results</h3>
        <div class="space-y-3">
          <NuxtLink v-for="p in queryResults" :key="p.id" :to="`/store/${p.store_id}`" class="block rounded-lg bg-white/5 border border-white/10 p-3 hover:border-[#FF7A00]/50">
            <div class="font-medium">{{ p.name }}</div>
            <div class="text-sm text-white/70">{{ p.store_name }}</div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect, onMounted } from 'vue'

interface Store { id: string | number; name: string; image?: string; distance_km?: number }
interface ProductHit { id: string | number; name: string; store_id: string | number; store_name: string }

const query = ref('')
const coords = ref<{ lat: number; lng: number } | null>(null)
const locating = ref(true)
const locError = ref('')

onMounted(() => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        coords.value = { lat: pos.coords.latitude, lng: pos.coords.longitude }
        locating.value = false
      },
      (err) => { locError.value = err.message; locating.value = false },
      { enableHighAccuracy: true, timeout: 8000 }
    )
  } else {
    locating.value = false
    locError.value = 'Geolocation not supported'
  }
})

const apiBase = useRuntimeConfig().public.apiBase || ''
const storesUrl = ref('')
const { data: stores, pending, refresh } = useFetch<Store[]>(storesUrl, { default: () => [] })

watchEffect(() => {
  if (coords.value) {
    storesUrl.value = `${apiBase}/api/stores/nearby/?lat=${coords.value.lat}&lng=${coords.value.lng}`
  }
})

function refreshStores() { refresh() }

const queryResults = ref<ProductHit[]>([])
async function doSearch() {
  if (!query.value.trim()) return
  const url = `${apiBase}/api/products/search/?q=${encodeURIComponent(query.value.trim())}`
  const { data } = await useFetch<ProductHit[]>(url)
  queryResults.value = data.value || []
}
</script>
