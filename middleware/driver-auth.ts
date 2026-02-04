import { defineNuxtRouteMiddleware, navigateTo, useCookie } from '#app'
import { useApiFetch } from '~/composables/useApiFetch'

export default defineNuxtRouteMiddleware(async (to: any) => {
  const token = useCookie<string | null>('auth_token').value
  try {
    const { data } = await useApiFetch<any>('/api/me/', {
      method: 'GET',
      credentials: 'include',
      headers: token ? { Authorization: `Bearer ${token}` } as any : undefined,
    })
    const u = data.value
    const isDriver = !!(u && (u.is_driver || u.role === 'driver' || u.roles?.includes?.('driver') || u.groups?.includes?.('driver')))
    if (!isDriver) return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  } catch {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }
})
