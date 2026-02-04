<template>
  <div class="space-y-4">
    <div class="rounded-xl overflow-hidden border border-white/10">
      <div class="h-72 bg-black/20 flex items-center justify-center" v-if="!mapUrl">
        <div class="text-white/60 text-sm">Map unavailable. Missing coordinates.</div>
      </div>
      <iframe v-else :src="mapUrl" class="w-full h-72 border-0" allowfullscreen="true" loading="lazy"></iframe>
    </div>

    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div>
          <div class="font-semibold">Active Delivery #{{ order?.id || id }}</div>
          <div class="text-xs text-white/70">Store → Customer</div>
        </div>
        <div class="text-xs text-white/60">Last location sent: <span v-if="lastSentAt">{{ new Date(lastSentAt).toLocaleTimeString() }}</span><span v-else>—</span></div>
      </div>
      <div class="mt-4 flex gap-2">
        <button class="px-4 py-2 rounded-full bg-white/10 hover:bg-white/15" :disabled="!customerPhone" @click="contact()">
          Contact Customer
        </button>
        <button class="px-4 py-2 rounded-full bg-[#22c55e] text-[#0A0F1E] font-medium disabled:opacity-60" :disabled="delivering" @click="markDelivered()">
          {{ delivering ? 'Submitting...' : 'Mark as Delivered' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useDriverTracking } from '~/composables/useDriverTracking'
import { navigateTo } from '#app'

definePageMeta({ layout: 'driver' as any, middleware: ['driver-auth'] as any })

const route = useRoute()
const id = computed(() => (route.query.id as string) || '')

const active = useState<any>('driverActiveOrder', () => null)
const order = ref<any>(active.value)

const config = useRuntimeConfig()

onMounted(async () => {
  if (!order.value && id.value) {
    const tryUrls = [`/api/driver/orders/${id.value}/`, `/api/orders/${id.value}/`]
    for (const url of tryUrls) {
      const { data, error } = await useApiFetch<any>(url)
      if (!error.value && data.value) { order.value = data.value; active.value = data.value; break }
    }
  }
  if (order.value?.id) tracking.start(order.value.id)
})

watch(order, (o) => { if (o?.id) tracking.start(o.id) })

function storeLat(o: any) { return o?.store_lat ?? o?.store?.lat ?? o?.pickup?.lat ?? null }
function storeLng(o: any) { return o?.store_lng ?? o?.store?.lng ?? o?.pickup?.lng ?? null }
function custLat(o: any) { return o?.customer_lat ?? o?.customer?.lat ?? o?.dropoff?.lat ?? null }
function custLng(o: any) { return o?.customer_lng ?? o?.customer?.lng ?? o?.dropoff?.lng ?? null }

const mapUrl = computed(() => {
  const key = String((config.public as any).googleMapsKey || '')
  const slat = storeLat(order.value), slng = storeLng(order.value)
  const clat = custLat(order.value), clng = custLng(order.value)
  if (!key || slat == null || slng == null || clat == null || clng == null) return ''
  const origin = `${slat},${slng}`
  const dest = `${clat},${clng}`
  return `https://www.google.com/maps/embed/v1/directions?key=${encodeURIComponent(key)}&origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(dest)}&mode=driving`
})

const customerPhone = computed(() => order.value?.customer_phone || order.value?.customer?.phone || order.value?.phone || '')
function contact() {
  if (!customerPhone.value) return
  if (typeof window === 'undefined') return
  window.location.href = `tel:${customerPhone.value}`
}

const delivering = ref(false)
async function markDelivered() {
  if (!order.value?.id) return
  delivering.value = true
  // Prefer dedicated endpoint, fallback PATCH
  const tryUrls = [
    { url: `/api/driver/orders/${order.value.id}/deliver/`, method: 'POST' },
    { url: `/api/orders/${order.value.id}/deliver/`, method: 'POST' },
  ]
  let ok = false
  for (const t of tryUrls) {
    const { error } = await useApiFetch(t.url, { method: t.method })
    if (!error.value) { ok = true; break }
  }
  if (!ok) {
    const { error } = await useApiFetch(`/api/orders/${order.value.id}/`, { method: 'PATCH', body: { order_status: 'completed' } })
    ok = !error.value
  }
  if (ok) {
    tracking.stop()
    active.value = null
    await navigateTo('/driver/history')
  }
  delivering.value = false
}

const { lastSentAt, start: startTracking, stop: stopTracking } = useDriverTracking()
const tracking = { start: startTracking, stop: stopTracking }

</script>
