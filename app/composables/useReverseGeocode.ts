export async function reverseGeocode(lat: number, lng: number): Promise<{ area: string | null; city: string | null; region: string | null; country: string | null }> {
  if (typeof window === 'undefined') return { area: null, city: null, region: null, country: null }
  const bdcUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${encodeURIComponent(lat)}&longitude=${encodeURIComponent(lng)}&localityLanguage=en`
  try {
    const res = await fetch(bdcUrl, { headers: { 'Accept': 'application/json' }, cache: 'no-store', mode: 'cors' })
    if (res.ok) {
      const d = await res.json()
      const region = d?.principalSubdivision || null
      const country = d?.countryName || null
      const city = d?.city || d?.locality || null
      let area: string | null = null
      area = d?.localityInfo?.locality?.name || d?.locality || null
      if (!area && Array.isArray(d?.localityInfo?.administrative)) {
        const pri = [
          'neighbourhood','suburb','quarter','residential','city district','district','ward','locality','town','village','hamlet'
        ]
        const adm = d.localityInfo.administrative as Array<{ name?: string; description?: string }>
        const found = adm.find(x => x?.name && x?.description && pri.includes(String(x.description).toLowerCase()))
        if (found?.name) area = found.name
      }
      if (area || city || region || country) return { area: area || null, city, region, country }
    }
  } catch {}

  const osmUrl = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lng)}&zoom=16&addressdetails=1`
  try {
    const res = await fetch(osmUrl, { headers: { 'Accept': 'application/json' }, cache: 'no-store', mode: 'cors' })
    if (!res.ok) return { area: null, city: null, region: null, country: null }
    const d = await res.json()
    const addr = d?.address || {}
    const area = addr.neighbourhood || addr.suburb || addr.quarter || addr.residential || addr.city_district || addr.district || addr.borough || addr.village || addr.town || null
    const city = addr.city || addr.town || addr.village || null
    const region = addr.state || addr.state_district || addr.region || null
    const country = addr.country || null
    return { area, city, region, country }
  } catch {
    return { area: null, city: null, region: null, country: null }
  }
}
