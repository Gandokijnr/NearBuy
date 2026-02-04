<template>
  <Teleport to="body">
    <div v-show="model" class="fixed inset-0 z-50">
      <div class="absolute inset-0 bg-black/40" @click="close" />
      <div class="absolute right-0 top-0 h-full w-full sm:w-96 bg-[#0A0F1E] text-[#F2F2F2] shadow-xl transition-transform">
        <div class="p-4 flex items-center justify-between border-b border-white/10">
          <h3 class="text-lg font-semibold">Cart ({{ count }})</h3>
          <button class="p-2" @click="close">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="p-4 space-y-3 max-h-[60vh] overflow-y-auto">
          <div v-if="items.length === 0" class="text-sm text-white/70">Your cart is empty</div>
          <div v-for="it in items" :key="it.id" class="flex items-center gap-3">
            <img v-if="it.image" :src="it.image" alt="" class="h-12 w-12 rounded object-cover"/>
            <div class="flex-1 min-w-0">
              <div class="font-medium truncate">{{ it.name }}</div>
              <div class="text-sm text-white/70">{{ currency(it.price) }}</div>
            </div>
            <div class="flex items-center gap-2">
              <button class="h-8 w-8 rounded-full bg-white/10" @click="decrement(it.id)">-</button>
              <div class="w-6 text-center">{{ it.qty }}</div>
              <button class="h-8 w-8 rounded-full bg-white/10" @click="increment(it.id)">+</button>
            </div>
            <button class="ml-2 text-white/60 hover:text-white" @click="remove(it.id)">Remove</button>
          </div>
        </div>
        <div class="p-4 border-t border-white/10 space-y-2">
          <div class="flex items-center justify-between text-sm"><span>Subtotal</span><span>{{ currency(subtotal) }}</span></div>
          <NuxtLink to="/checkout" class="block text-center w-full rounded-full bg-[#FF7A00] px-6 py-3 font-semibold text-[#0A0F1E]" @click="close">Checkout</NuxtLink>
        </div>
      </div>
    </div>
  </Teleport>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useCartStore } from '../../stores/cart'
const model = defineModel<boolean>({ default: false })
const cart = useCartStore()
const { items, subtotal, count } = storeToRefs(cart)
const increment = (id: string) => cart.increment(id)
const decrement = (id: string) => cart.decrement(id)
const remove = (id: string) => cart.remove(id)
const close = () => { model.value = false }
const currency = (n: number) => new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n)
</script>
