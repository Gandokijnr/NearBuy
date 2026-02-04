import { ref } from 'vue'

export function useIpLocation() {
  const city = ref<string | null>(null)
  const region = ref<string | null>(null)
  const country = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchCity() {
    if (typeof window === 'undefined') return
    loading.value = true
    error.value = null

    const candidates: Array<{ url: string; pick: (d: any) => string | null; ok?: (d: any) => boolean }>
      = [
        {
          url: 'https://ipapi.co/json/',
          pick: (d) => d?.city ?? null,
        },
        {
          url: 'https://ipwho.is/',
          pick: (d) => d?.city ?? null,
          ok: (d) => d?.success !== false,
        },
      ]

    try {
      for (const c of candidates) {
        try {
          const res = await fetch(c.url, { headers: { 'Accept': 'application/json' }, cache: 'no-store', mode: 'cors' })
          if (!res.ok) continue
          const data = await res.json()
          if (c.ok && !c.ok(data)) continue
          const picked = c.pick(data)
          if (picked) {
            city.value = data?.city ?? picked
            region.value = data?.region ?? data?.region_name ?? null
            country.value = data?.country ?? data?.country_name ?? data?.country_code ?? null
            break
          }
        } catch (_) {
          // try next candidate
          continue
        }
      }
      if (!city.value) {
        error.value = 'Could not determine city from IP'
      }
    } catch (e: any) {
      error.value = e?.message || 'Failed to load IP location'
    } finally {
      loading.value = false
    }
  }

  return { city, region, country, loading, error, fetchCity }
}
