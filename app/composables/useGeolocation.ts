import { onBeforeUnmount, ref } from 'vue'

export function useGeolocation() {
  const isSupported = typeof navigator !== 'undefined' && !!navigator.geolocation
  const permission = ref<'prompt'|'granted'|'denied'>('prompt')
  const coords = ref<{ lat: number|null, lng: number|null, accuracy?: number, timestamp?: number }>({ lat: null, lng: null })
  const error = ref<string>('')
  let watchId: number | null = null

  async function queryPermission() {
    try {
      if (typeof navigator === 'undefined' || !(navigator as any).permissions) return
      const r = await (navigator as any).permissions.query({ name: 'geolocation' })
      permission.value = r.state
      r.onchange = () => { permission.value = r.state }
    } catch {}
  }

  function start() {
    if (!isSupported || watchId !== null) return
    error.value = ''
    try {
      watchId = navigator.geolocation.watchPosition((pos) => {
        coords.value = { lat: pos.coords.latitude, lng: pos.coords.longitude, accuracy: pos.coords.accuracy, timestamp: pos.timestamp }
      }, (err) => {
        error.value = err?.message || 'Geolocation error'
      }, { enableHighAccuracy: true, maximumAge: 10000, timeout: 20000 })
    } catch (e: any) {
      error.value = e?.message || 'Geolocation error'
    }
  }

  function stop() {
    if (!isSupported) return
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId)
      watchId = null
    }
  }

  onBeforeUnmount(stop)
  queryPermission()

  return { isSupported, permission, coords, error, start, stop }
}
