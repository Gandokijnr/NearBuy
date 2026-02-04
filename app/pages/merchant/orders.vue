<template>
  <div class="grid grid-cols-1 gap-4">
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="flex items-center justify-between mb-3">
        <div class="font-semibold">New</div>
        <div class="text-xs text-white/60">WS: {{ wsStatus }}</div>
      </div>
      <div class="space-y-3">
        <div v-for="o in newOrders" :key="o.id" class="rounded-lg bg-white/5 border border-white/10 p-3">
          <div class="flex items-center justify-between">
            <div class="font-semibold">#{{ o.id }} — {{ o.customer_name || o.customer?.name || 'Customer' }}</div>
            <div class="text-sm">{{ money(o.total || o.amount_total || o.total_amount) }}</div>
          </div>
          <div class="text-xs text-white/70 mt-1">Items: {{ (o.items || o.lines || []).length }}</div>
          <div class="mt-3 flex gap-2">
            <button class="px-3 py-1 rounded-full bg-[#22c55e] text-[#0A0F1E] font-medium disabled:opacity-60" :disabled="loading" @click="accept(o)">Accept</button>
            <button class="px-3 py-1 rounded-full bg-[#ef4444] text-[#0A0F1E] font-medium disabled:opacity-60" :disabled="loading" @click="reject(o)">Reject</button>
          </div>
        </div>
        <div v-if="!newOrders.length" class="text-sm text-white/60">No new orders.</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

definePageMeta({ layout: 'protected', middleware: ['merchant-auth'] })

const newOrders = ref<any[]>([])
const loading = ref(false)

const { data: initial } = await useApiFetch<any>('/api/orders/?status=new', { server: false })
if (Array.isArray(initial.value)) newOrders.value = initial.value

function beep() {
  if (process.server) return
  try {
    const Ctx = (window as any).AudioContext || (window as any).webkitAudioContext
    const ctx = new Ctx()
    const o = ctx.createOscillator()
    const g = ctx.createGain()
    o.type = 'sine'
    o.frequency.value = 880
    o.connect(g)
    g.connect(ctx.destination)
    g.gain.value = 0.1
    o.start()
    setTimeout(() => { o.stop(); ctx.close() }, 400)
  } catch {}
}

const { lastMessage, status: wsStatus } = useAutoWS('/ws/merchant/orders/', { heartbeatMs: 25000 })
watch(lastMessage, (msg) => {
  if (!msg) return
  const order = (msg as any).order || msg
  if (!order?.id) return
  if (!newOrders.value.find((x: any) => x.id === order.id)) {
    newOrders.value.unshift(order)
    beep()
  }
})

async function patchOrder(id: number | string, body: any) {
  const { error } = await useApiFetch(`/api/orders/${id}/`, { method: 'PATCH', body })
  return !error.value
}

async function accept(o: any) {
  loading.value = true
  const ok = await patchOrder(o.id, { order_status: 'preparing' })
  if (ok) newOrders.value = newOrders.value.filter((x: any) => x.id !== o.id)
  loading.value = false
}

async function reject(o: any) {
  loading.value = true
  const ok = await patchOrder(o.id, { order_status: 'rejected' })
  if (ok) newOrders.value = newOrders.value.filter((x: any) => x.id !== o.id)
  loading.value = false
}

function money(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n || 0) }
</script>
