import { onBeforeUnmount, ref } from 'vue'
import { useGeolocation } from '~/composables/useGeolocation'
import { useApiFetch } from '~/composables/useApiFetch'

export function useDriverTracking() {
  const activeOrderId = ref<string | number | null>(null)
  const sending = ref(false)
  const lastSentAt = ref<number | null>(null)
  let timer: any = null

  const { coords, start: startGeo, stop: stopGeo } = useGeolocation()

  async function sendOnce(orderId: string | number) {
    if (!coords.value.lat || !coords.value.lng) return
    try {
      sending.value = true
      // Prefer driver endpoint, fallback to generic orders endpoint
      let ok = false
      const r1 = await useApiFetch(`/api/driver/orders/${orderId}/location/`, {
        method: 'POST',
        body: { lat: coords.value.lat, lng: coords.value.lng, ts: Date.now() }
      })
      ok = !r1.error.value
      if (!ok) {
        const r2 = await useApiFetch(`/api/orders/${orderId}/location/`, {
          method: 'POST',
          body: { lat: coords.value.lat, lng: coords.value.lng, ts: Date.now() }
        })
        ok = !r2.error.value
      }
      if (ok) lastSentAt.value = Date.now()
    } finally {
      sending.value = false
    }
  }

  function start(orderId: string | number) {
    if (activeOrderId.value === orderId) return
    activeOrderId.value = orderId
    startGeo()
    clearInterval(timer)
    // Send immediately, then every 30s
    sendOnce(orderId)
    timer = setInterval(() => sendOnce(orderId), 30000)
  }

  function stop() {
    activeOrderId.value = null
    clearInterval(timer)
    stopGeo()
  }

  onBeforeUnmount(stop)

  return { activeOrderId, sending, lastSentAt, start, stop }
}
