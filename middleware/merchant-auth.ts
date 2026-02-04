export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie<string | null>('auth_token').value
  try {
    const { data } = await useApiFetch<any>('/api/me/', {
      method: 'GET',
      credentials: 'include',
      headers: token ? { Authorization: `Bearer ${token}` } as any : undefined,
    })
    const u = data.value
    const isMerchant = !!(u && (u.is_merchant || u.role === 'merchant' || u.roles?.includes?.('merchant') || u.groups?.includes?.('merchant')))
    if (!isMerchant) return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  } catch {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }
})
