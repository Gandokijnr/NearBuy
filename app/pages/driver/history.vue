<template>
  <div class="space-y-4">
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="flex items-center justify-between mb-3">
        <div class="font-semibold">Delivery History</div>
        <div class="text-sm">Total: {{ money(totalPayout + totalTips) }}</div>
      </div>
      <div class="text-xs text-white/70 mb-2">Payout: {{ money(totalPayout) }} · Tips: {{ money(totalTips) }} · Runs: {{ runs.length }}</div>
      <div class="divide-y divide-white/10">
        <div v-for="o in runs" :key="o.id" class="py-3 flex items-center justify-between">
          <div>
            <div class="font-medium">#{{ o.id }} — {{ storeName(o) }}</div>
            <div class="text-xs text-white/60">Delivered: {{ deliveredAt(o) }}</div>
          </div>
          <div class="text-right">
            <div class="text-sm">Payout: {{ money(payout(o)) }}</div>
            <div class="text-xs text-white/60">Tip: {{ money(tip(o)) }}</div>
          </div>
        </div>
        <div v-if="!runs.length" class="py-6 text-center text-white/60 text-sm">No completed runs yet.</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

definePageMeta({ layout: 'driver' as any, middleware: ['driver-auth'] as any })

const runs = ref<any[]>([])

const tryUrls = ['/api/driver/deliveries/?status=completed', '/api/orders/?driver=me&status=completed']
for (const url of tryUrls) {
  const { data, error } = await useApiFetch<any>(url)
  if (!error.value && Array.isArray(data.value)) { runs.value = data.value; break }
}

function storeName(o: any) { return o.store_name || o.store?.name || 'Store' }
function payout(o: any) { return o.driver_payout ?? o.delivery_fee ?? 0 }
function tip(o: any) { return o.tip ?? o.tips ?? o.tip_amount ?? 0 }
function deliveredAt(o: any) {
  const t = o.delivered_at ?? o.completed_at ?? o.updated_at ?? o.created_at
  try { return t ? new Date(t).toLocaleString() : '—' } catch { return '—' }
}

const totalPayout = computed(() => runs.value.reduce((acc, o) => acc + (payout(o) || 0), 0))
const totalTips = computed(() => runs.value.reduce((acc, o) => acc + (tip(o) || 0), 0))

function money(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n || 0) }
</script>
