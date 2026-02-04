<template>
  <div class="min-h-screen px-4 sm:px-6 pt-16 md:pt-20 pb-6 bg-[#0A0F1E] text-[#F2F2F2]">
    <div class="mx-auto max-w-7xl">
      <div class="flex items-center justify-between mb-4">
        <div>
          <div class="text-xs text-white/60"><NuxtLink to="/discover" class="hover:text-white">← Back</NuxtLink></div>
          <h1 class="text-2xl font-bold">{{ store?.name || 'Store' }}</h1>
          <div class="text-sm text-white/70" v-if="store?.distance_km">{{ store.distance_km.toFixed(1) }} km away</div>
        </div>
        <button class="relative rounded-full px-4 py-2 bg-white/10 hover:bg-white/15" @click="showCart = true">
          Cart
          <span v-if="count" class="ml-2 inline-flex items-center justify-center h-6 min-w-6 px-2 rounded-full bg-[#FF7A00] text-[#0A0F1E] text-sm">{{ count }}</span>
        </button>
      </div>

      <div v-if="storePending || productsPending" class="text-white/70">Loading...</div>

      <div v-else class="space-y-8">
        <div v-for="cat in categories" :key="cat.name">
          <h2 class="text-xl font-semibold mb-3">{{ cat.name }}</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            <div v-for="p in cat.items" :key="p.id" class="rounded-xl bg-white/5 border border-white/10 p-3 flex flex-col">
              <img v-if="p.image" :src="p.image" :alt="p.name" class="h-28 w-full object-cover rounded-lg mb-2"/>
              <div class="font-medium truncate">{{ p.name }}</div>
              <div class="text-sm text-white/70 mb-3">{{ currency(p.price) }}</div>
              <button class="mt-auto rounded-full bg-[#FF7A00] text-[#0A0F1E] px-4 py-2 font-semibold" @click="add(p)">Add</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <MiniCart v-model="showCart" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import MiniCart from '~/components/MiniCart.vue'
import { useCartStore } from '../../../stores/cart'

interface Store { id: string | number; name: string; distance_km?: number }
interface Product { id: string | number; name: string; price: number; image?: string; category?: string }

const route = useRoute()
const id = computed(() => route.params.id as string)
const apiBase = useRuntimeConfig().public.apiBase || ''

const { data: store, pending: storePending } = useFetch<Store>(() => id.value ? `${apiBase}/api/stores/${id.value}/` : '', { default: () => ({ id: id.value, name: 'Store' }) })
const { data: products, pending: productsPending } = useFetch<Product[]>(() => id.value ? `${apiBase}/api/products/?store_id=${id.value}` : '', { default: () => [] })

const categories = computed(() => {
  const groups: Record<string, Product[]> = {}
  for (const p of products.value || []) {
    const key = p.category || 'Other'
    if (!groups[key]) groups[key] = []
    groups[key].push(p)
  }
  return Object.entries(groups).map(([name, items]) => ({ name, items }))
})

const cart = useCartStore()
const showCart = ref(false)
const count = computed(() => cart.count)
function add(p: Product) {
  cart.addItem({ id: String(p.id), name: p.name, price: p.price, image: p.image }, 1)
}

watchEffect(() => {
  if (store.value?.distance_km) cart.setDistanceKm(store.value.distance_km)
  if (store.value?.id) cart.setStoreId(String(store.value.id))
})

function currency(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n) }
</script>
