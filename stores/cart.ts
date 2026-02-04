import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface CartItem {
  id: string
  name: string
  price: number
  image?: string
  qty: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const storeId = ref<string | null>(null)
  const distanceKm = ref(0)

  const count = computed(() => items.value.reduce((n, i) => n + i.qty, 0))
  const subtotal = computed(() => items.value.reduce((sum, i) => sum + i.price * i.qty, 0))

  function setStoreId(id: string) { storeId.value = id }
  function setDistanceKm(km: number) { distanceKm.value = km }
  function addItem(item: Omit<CartItem, 'qty'>, qty = 1) {
    const existing = items.value.find(i => i.id === item.id)
    if (existing) existing.qty += qty
    else items.value.push({ ...item, qty })
  }
  function increment(id: string) {
    const it = items.value.find(i => i.id === id)
    if (it) it.qty += 1
  }
  function decrement(id: string) {
    const it = items.value.find(i => i.id === id)
    if (!it) return
    it.qty -= 1
    if (it.qty <= 0) items.value = items.value.filter(i => i.id !== id)
  }
  function remove(id: string) {
    items.value = items.value.filter(i => i.id !== id)
  }
  function clear() { items.value = [] }

  return { items, storeId, distanceKm, count, subtotal, setStoreId, setDistanceKm, addItem, increment, decrement, remove, clear }
})
