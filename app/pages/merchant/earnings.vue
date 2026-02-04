<script setup lang="ts">
import { computed, ref } from 'vue'

definePageMeta({ layout: 'protected', middleware: ['merchant-auth'] })

const { data: summary, error: sumErr } = await useApiFetch<any>('/api/merchant/earnings/today/')
const hasSummary = computed(() => !!summary.value && Object.keys(summary.value || {}).length > 0 && !sumErr.value)

const totalOrders = ref(0)
const gross = ref(0)

if (!hasSummary.value) {
  const { data: completed } = await useApiFetch<any>('/api/orders/?status=completed&range=today')
  const arr = Array.isArray(completed.value) ? completed.value : []
  totalOrders.value = arr.length
  gross.value = arr.reduce((acc: number, o: any) => acc + (o.total || o.amount_total || o.total_amount || 0), 0)
}

const dailyRevenue = computed(() => {
  if (hasSummary.value) return summary.value.daily_revenue ?? summary.value.revenue ?? 0
  return gross.value
})
const ordersCount = computed(() => {
  if (hasSummary.value) return summary.value.total_orders ?? summary.value.orders ?? 0
  return totalOrders.value
})
const commissionRate = computed(() => {
  if (hasSummary.value) return summary.value.commission_rate ?? 0.1
  return 0.1
})
const commission = computed(() => dailyRevenue.value * commissionRate.value)
const net = computed(() => dailyRevenue.value - commission.value)

function money(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n || 0) }
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="text-sm text-white/70">Daily Revenue</div>
      <div class="text-2xl font-semibold mt-1">{{ money(dailyRevenue) }}</div>
    </div>
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="text-sm text-white/70">Total Orders</div>
      <div class="text-2xl font-semibold mt-1">{{ ordersCount }}</div>
    </div>
    <div class="rounded-xl bg-white/5 border border-white/10 p-4">
      <div class="text-sm text-white/70">Commission Deducted</div>
      <div class="text-2xl font-semibold mt-1">{{ money(commission) }}</div>
    </div>
    <div class="rounded-xl bg-white/5 border border-white/10 p-4 md:col-span-3">
      <div class="text-sm text-white/70">Net Earnings</div>
      <div class="text-2xl font-semibold mt-1">{{ money(net) }}</div>
    </div>
  </div>
</template>
