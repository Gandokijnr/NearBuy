<script setup lang="ts">
import { ref } from 'vue'

definePageMeta({ layout: 'protected', middleware: ['merchant-auth'] })

const products = ref<any[]>([])
const saving = ref<Record<string, boolean>>({})
let loaded = false

const r1 = await useApiFetch<any>('/api/merchant/products/')
if (!r1.error.value && Array.isArray(r1.data.value)) {
  products.value = r1.data.value
  loaded = true
}
if (!loaded) {
  const r2 = await useApiFetch<any>('/api/products/?mine=1')
  if (Array.isArray(r2.data.value)) products.value = r2.data.value
}

function getInStock(p: any) { return p.in_stock ?? p.available ?? p.is_available ?? true }
function setInStock(p: any, v: boolean) {
  p.in_stock = v
  if ('available' in p) (p as any).available = v
  if ('is_available' in p) (p as any).is_available = v
}

async function save(p: any) {
  saving.value[p.id] = true
  const body: any = { price: p.price ?? p.unit_price ?? p.amount, in_stock: getInStock(p) }
  const { error } = await useApiFetch(`/api/merchant/products/${p.id}/`, { method: 'PATCH', body })
  if (error.value) {
    await useApiFetch(`/api/products/${p.id}/`, { method: 'PATCH', body })
  }
  saving.value[p.id] = false
}

function money(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n || 0) }
</script>

<template>
  <div class="space-y-4">
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="font-semibold mb-3">Inventory</div>
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="text-left text-white/70">
            <tr>
              <th class="py-2 pr-4">Product</th>
              <th class="py-2 pr-4">Price</th>
              <th class="py-2 pr-4">In Stock</th>
              <th class="py-2 pr-4 w-32"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.id" class="border-t border-white/10">
              <td class="py-2 pr-4">{{ p.name }}</td>
              <td class="py-2 pr-4">
                <input type="number" step="0.01" v-model.number="p.price" class="w-32 rounded bg-white/5 border border-white/10 px-2 py-1 outline-none focus:border-[#FF7A00]" />
              </td>
              <td class="py-2 pr-4">
                <label class="inline-flex items-center gap-2">
                  <input type="checkbox" :checked="getInStock(p)" @change="setInStock(p, ($event.target as HTMLInputElement).checked)" />
                  <span class="text-white/80">Available</span>
                </label>
              </td>
              <td class="py-2 pr-4">
                <button class="px-3 py-1 rounded-full bg-[#FF7A00] text-[#0A0F1E] font-medium disabled:opacity-60" :disabled="saving[p.id]" @click="save(p)">
                  {{ saving[p.id] ? 'Saving...' : 'Save' }}
                </button>
              </td>
            </tr>
            <tr v-if="!products.length">
              <td colspan="4" class="py-6 text-center text-white/60">No products found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
