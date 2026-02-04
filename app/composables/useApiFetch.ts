import { computed } from 'vue'

export function useApiFetch<T = any>(path: string | (() => string), options: any = {}) {
  const config = useRuntimeConfig()
  const url = computed(() => {
    const p = typeof path === 'function' ? (path as () => string)() : path
    const base = config.public.apiBase || ''
    if (!p) return base
    if (p.startsWith('http')) return p
    return `${base}${p.startsWith('/') ? p : `/${p}`}`
  })
  return useFetch<T>(url as any, options as any)
}
