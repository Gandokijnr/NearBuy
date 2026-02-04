<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div v-for="col in columns" :key="col.key" class="rounded-xl bg-white/5 border border-white/10 p-4" @dragover.prevent @drop="onDrop(col.key)">
      <div class="font-semibold mb-3">{{ col.label }}</div>
      <div class="space-y-3 min-h-[200px]">
        <div v-for="o in lists[col.key]" :key="o.id" class="rounded-lg bg-white/5 border border-white/10 p-3 cursor-move" draggable="true" @dragstart="onDragStart(o, col.key)">
          <div class="flex items-center justify-between">
            <div class="font-semibold">#{{ o.id }}</div>
            <div class="text-sm">{{ money(o.total || o.amount_total || o.total_amount) }}</div>
          </div>
          <div class="mt-3 flex gap-2">
            <button v-if="col.key === 'preparing'" class="px-3 py-1 rounded-full bg-[#22c55e] text-[#0A0F1E] font-medium" @click="moveTo(o, 'ready_for_pickup')">Mark Ready</button>
            <button v-else-if="col.key === 'ready_for_pickup'" class="px-3 py-1 rounded-full bg-[#3b82f6] text-[#0A0F1E] font-medium" @click="moveTo(o, 'completed')">Complete</button>
          </div>
        </div>
        <div v-if="!lists[col.key].length" class="text-sm text-white/60">No orders</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

definePageMeta({ layout: 'protected', middleware: ['merchant-auth'] })

type StatusKey = 'preparing' | 'ready_for_pickup' | 'completed'
const columns = [
  { key: 'preparing', label: 'Preparing' },
  { key: 'ready_for_pickup', label: 'Ready for Pickup' },
  { key: 'completed', label: 'Completed' },
] as { key: StatusKey, label: string }[]

const lists = reactive<Record<StatusKey, any[]>>({
  preparing: [],
  ready_for_pickup: [],
  completed: [],
})

const { data: dp } = await useApiFetch<any>('/api/orders/?status=preparing')
const { data: dr } = await useApiFetch<any>('/api/orders/?status=ready_for_pickup')
const { data: dc } = await useApiFetch<any>('/api/orders/?status=completed')
if (Array.isArray(dp.value)) lists.preparing = dp.value
if (Array.isArray(dr.value)) lists.ready_for_pickup = dr.value
if (Array.isArray(dc.value)) lists.completed = dc.value

const dragging = ref<{ order: any, from: StatusKey } | null>(null)
function onDragStart(o: any, from: StatusKey) {
  dragging.value = { order: o, from }
}
async function onDrop(to: StatusKey) {
  if (!dragging.value) return
  const { order, from } = dragging.value
  if (from === to) { dragging.value = null; return }
  await moveTo(order, to)
  dragging.value = null
}
function removeFromAll(id: any) {
  ;(['preparing','ready_for_pickup','completed'] as StatusKey[]).forEach((k) => {
    (lists as any)[k] = (lists as any)[k].filter((x: any) => x.id !== id)
  })
}
async function moveTo(o: any, to: StatusKey) {
  const { error } = await useApiFetch(`/api/orders/${o.id}/`, { method: 'PATCH', body: { order_status: to } })
  if (!error.value) {
    removeFromAll(o.id)
    ;(lists as any)[to].unshift({ ...o, order_status: to })
  }
}
function money(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n || 0) }
</script>
