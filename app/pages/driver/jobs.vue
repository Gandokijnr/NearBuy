<template>
  <div class="space-y-4">
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="flex items-center justify-between mb-3">
        <div class="font-semibold">Jobs — Ready for Pickup</div>
        <div class="text-xs text-white/60">Location: <span v-if="coords.lat && coords.lng">{{ coords.lat.toFixed(4) }}, {{ coords.lng.toFixed(4) }}</span><span v-else>off</span></div>
      </div>
      <div class="space-y-3">
        <div v-for="o in jobs" :key="o.id" class="rounded-lg bg-white/5 border border-white/10 p-3">
          <div class="flex items-center justify-between">
            <div class="font-semibold">#{{ o.id }} — {{ storeName(o) }}</div>
            <div class="text-sm">{{ money(payout(o)) }}</div>
          </div>
          <div class="text-xs text-white/70 mt-1">Distance to store: {{ distanceToStore(o) }}</div>
          <div class="mt-3 flex gap-2">
            <button class="px-3 py-1 rounded-full bg-[#22c55e] text-[#0A0F1E] font-medium disabled:opacity-60" :disabled="loading" @click="accept(o)">Accept</button>
            <NuxtLink :to="`/driver/active?id=${o.id}`" class="px-3 py-1 rounded-full bg-white/10 hover:bg-white/15">Details</NuxtLink>
          </div>
        </div>
        <div v-if="!jobs.length" class="text-sm text-white/60">No jobs right now.</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useGeolocation } from '~/composables/useGeolocation'
import { navigateTo, useState } from '#app'

definePageMeta({ layout: 'driver' as any, middleware: ['driver-auth'] as any })

const jobs = ref<any[]>([])
const loading = ref(false)

const { coords, start: startGeo } = useGeolocation()

const readyUrlCandidates = ['/api/driver/jobs/', '/api/orders/?status=ready_for_pickup']

onMounted(async () => {
  startGeo()
  for (const url of readyUrlCandidates) {
    const { data, error } = await useApiFetch<any>(url)
    if (!error.value && Array.isArray(data.value)) { jobs.value = data.value; break }
  }
})

function storeName(o: any) { return o.store_name || o.store?.name || 'Store' }
function storeLat(o: any) { return o.store_lat ?? o.store?.lat ?? o.store?.latitude ?? o.pickup?.lat ?? null }
function storeLng(o: any) { return o.store_lng ?? o.store?.lng ?? o.store?.longitude ?? o.pickup?.lng ?? null }

function haversine(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) * Math.sin(dLon/2) * Math.sin(dLon/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  return R * c
}

function distanceToStore(o: any) {
  if (!coords.value.lat || !coords.value.lng) return '—'
  const slat = storeLat(o), slng = storeLng(o)
  if (slat == null || slng == null) return '—'
  const km = haversine(coords.value.lat, coords.value.lng, slat, slng)
  return `${km.toFixed(1)} km`
}

function payout(o: any) {
  const fee = o.driver_payout ?? o.delivery_fee ?? 0
  if (fee) return fee
  // naive estimate fallback: base 2 + 0.7/km from store to customer if available
  const clat = o.dropoff?.lat ?? o.customer?.lat ?? o.customer_lat
  const clng = o.dropoff?.lng ?? o.customer?.lng ?? o.customer_lng
  const slat = storeLat(o), slng = storeLng(o)
  if (slat != null && slng != null && clat != null && clng != null) {
    const km = haversine(slat, slng, clat, clng)
    return Math.max(2, 2 + 0.7 * km)
  }
  return 2
}

async function accept(o: any) {
  loading.value = true
  // Prefer a dedicated accept endpoint, fallback to PATCH order_status
  const tryUrls = [
    { url: `/api/driver/orders/${o.id}/accept/`, method: 'POST' },
    { url: `/api/orders/${o.id}/accept/`, method: 'POST' },
  ]
  let ok = false
  for (const t of tryUrls) {
    const { error } = await useApiFetch(t.url, { method: t.method })
    if (!error.value) { ok = true; break }
  }
  if (!ok) {
    const { error } = await useApiFetch(`/api/orders/${o.id}/`, { method: 'PATCH', body: { order_status: 'out_for_delivery' } })
    ok = !error.value
  }
  if (ok) {
    // set active order state and navigate
    const active = useState<any>('driverActiveOrder', () => null)
    active.value = o
    jobs.value = jobs.value.filter((x) => x.id !== o.id)
    await navigateTo(`/driver/active?id=${o.id}`)
  }
  loading.value = false
}

function money(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n || 0) }
</script>
