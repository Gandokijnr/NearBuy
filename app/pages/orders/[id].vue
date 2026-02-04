<template>
  <div class="min-h-screen px-4 sm:px-6 pt-16 md:pt-20 pb-6 bg-[#0A0F1E] text-[#F2F2F2]">
    <div class="mx-auto max-w-3xl">
      <div class="mb-6">
        <div class="text-xs text-white/60"><NuxtLink to="/discover" class="hover:text-white">← Back to Discover</NuxtLink></div>
        <h1 class="text-2xl font-bold">Order #{{ id }}</h1>
        <div class="text-sm text-white/70">Status: <span class="font-semibold">{{ displayStatus }}</span></div>
      </div>

      <div class="rounded-xl bg-white/5 border border-white/10 p-4">
        <div class="space-y-4">
          <div v-for="s in steps" :key="s.key" class="flex items-start gap-3">
            <div class="mt-1 h-3 w-3 rounded-full" :class="stepDotClass(s.key)"></div>
            <div>
              <div class="font-medium">{{ s.label }}</div>
              <div class="text-xs text-white/60" v-if="s.key === status">{{ updatedAt ? formattedTime : '' }}</div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="wsError" class="mt-4 text-[#FF7A00] text-sm">{{ wsError }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const route = useRoute()
const id = computed(() => route.params.id as string)
const status = ref<'preparing' | 'out_for_delivery' | 'arrived' | 'created'>('created')
const updatedAt = ref<number | null>(null)
const wsError = ref('')

const steps = [
  { key: 'created', label: 'Order Placed' },
  { key: 'preparing', label: 'Preparing' },
  { key: 'out_for_delivery', label: 'Out for Delivery' },
  { key: 'arrived', label: 'Arrived' },
] as const

const displayStatus = computed(() => steps.find(s => s.key === status.value)?.label || 'Created')
const formattedTime = computed(() => updatedAt.value ? new Date(updatedAt.value).toLocaleTimeString() : '')

function stepDotClass(key: typeof steps[number]['key']) {
  const idx = steps.findIndex(s => s.key === key)
  const cur = steps.findIndex(s => s.key === status.value)
  if (idx < cur) return 'bg-[#FF7A00]'
  if (idx === cur) return 'bg-[#FF7A00] animate-pulse'
  return 'bg-white/20'
}

let socket: WebSocket | null = null
onMounted(() => {
  const wsBase = useRuntimeConfig().public.wsBase || ''
  if (!wsBase) { wsError.value = 'WebSocket base not configured'; return }
  try {
    socket = new WebSocket(`${wsBase}/ws/orders/${id.value}/`)
    socket.onmessage = (evt) => {
      try {
        const msg = JSON.parse(evt.data)
        if (msg?.status) {
          status.value = msg.status
          updatedAt.value = Date.now()
        }
      } catch (e) {
        // ignore
      }
    }
    socket.onerror = () => { wsError.value = 'WebSocket error' }
    socket.onclose = () => { /* optional: attempt reconnect */ }
  } catch (e: any) {
    wsError.value = e?.message || 'Failed to connect to WebSocket'
  }
})

onBeforeUnmount(() => { if (socket) { try { socket.close() } catch {} } })
</script>
