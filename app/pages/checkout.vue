<template>
  <div class="min-h-screen px-4 sm:px-6 pt-16 md:pt-20 pb-6 bg-[#0A0F1E] text-[#F2F2F2]">
    <div class="mx-auto max-w-3xl grid md:grid-cols-2 gap-6">
      <div class="space-y-4">
        <h1 class="text-2xl font-bold">Checkout</h1>
        <div class="rounded-xl bg-white/5 border border-white/10 p-4 space-y-3">
          <div class="font-semibold">Delivery Address</div>
          <input v-model="address.line1" placeholder="Address line" class="w-full rounded-lg bg-white/5 border border-white/10 px-3 py-2 outline-none focus:border-[#FF7A00]"/>
          <div class="grid grid-cols-2 gap-3">
            <input v-model="address.city" placeholder="City" class="rounded-lg bg-white/5 border border-white/10 px-3 py-2 outline-none focus:border-[#FF7A00]"/>
            <input v-model="address.state" placeholder="State" class="rounded-lg bg-white/5 border border-white/10 px-3 py-2 outline-none focus:border-[#FF7A00]"/>
          </div>
          <input v-model="address.postal" placeholder="Postal code" class="w-full rounded-lg bg-white/5 border border-white/10 px-3 py-2 outline-none focus:border-[#FF7A00]"/>
          <label class="flex items-center gap-2 text-sm text-white/80">
            <input type="checkbox" v-model="addressConfirmed" class="h-4 w-4"/>
            <span>I confirm my delivery address is correct</span>
          </label>
        </div>

        <div class="rounded-xl bg-white/5 border border-white/10 p-4">
          <div class="font-semibold mb-2">Payment</div>
          <ClientOnly>
            <div id="payment-element" class="bg-white/5 border border-white/10 rounded-lg p-3"></div>
          </ClientOnly>
          <div v-if="stripeError" class="mt-2 text-[#FF7A00] text-sm">{{ stripeError }}</div>
        </div>

        <button :disabled="!canPay || loading" class="w-full rounded-full bg-[#FF7A00] text-[#0A0F1E] px-6 py-3 font-semibold disabled:opacity-60" @click="submitPayment">
          {{ loading ? 'Processing...' : 'Confirm and Pay' }}
        </button>
      </div>

      <div class="space-y-4">
        <div class="rounded-xl bg-white/5 border border-white/10 p-4">
          <div class="font-semibold mb-3">Order Summary</div>
          <div class="space-y-2">
            <div class="flex justify-between text-sm" v-for="it in cart.items" :key="it.id">
              <span>{{ it.name }} × {{ it.qty }}</span>
              <span>{{ currency(it.price * it.qty) }}</span>
            </div>
          </div>
          <div class="h-px bg-white/10 my-3"></div>
          <div class="flex justify-between text-sm"><span>Subtotal</span><span>{{ currency(subtotal) }}</span></div>
          <div class="flex justify-between text-sm"><span>Delivery Fee</span><span>{{ currency(deliveryFee) }}</span></div>
          <div class="flex justify-between text-sm"><span>Service Fee</span><span>{{ currency(serviceFee) }}</span></div>
          <div class="h-px bg-white/10 my-3"></div>
          <div class="flex justify-between font-semibold"><span>Total</span><span>{{ currency(total) }}</span></div>
        </div>
        <div class="text-xs text-white/60">Distance: {{ cart.distanceKm?.toFixed?.(1) ?? cart.distanceKm }} km</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, computed } from 'vue'
import { useCartStore } from '../../stores/cart'

const cart = useCartStore()
const subtotal = computed(() => cart.subtotal)
const deliveryFee = computed(() => 2.5 + (cart.distanceKm || 0) * 1.2)
const serviceFee = computed(() => Math.max(0.5, subtotal.value * 0.05))
const total = computed(() => subtotal.value + deliveryFee.value + serviceFee.value)

const address = reactive({ line1: '', city: '', state: '', postal: '' })
const addressConfirmed = ref(false)
const canPay = computed(() => Boolean(address.line1 && address.city && address.state && address.postal && addressConfirmed.value && cart.items.length > 0))

const nuxtApp = useNuxtApp()
const stripeError = ref('')
const loading = ref(false)
let elements: any = null

onMounted(async () => {
  try {
    const stripe = await nuxtApp.$stripe
    if (!stripe) return
    const apiBase = useRuntimeConfig().public.apiBase || ''
    const payload = { address, items: cart.items, delivery_km: cart.distanceKm, amounts: { subtotal: subtotal.value, delivery: deliveryFee.value, service: serviceFee.value, total: total.value } }
    const res: any = await $fetch(`${apiBase}/api/payments/create-intent/`, { method: 'POST', body: payload })
    if (!res?.client_secret) { stripeError.value = 'Missing client secret'; return }
    elements = stripe.elements({ clientSecret: res.client_secret })
    const pe = elements.create('payment')
    pe.mount('#payment-element')
  } catch (e: any) {
    stripeError.value = e?.message || 'Stripe failed to initialize'
  }
})

async function submitPayment() {
  if (!canPay.value || loading.value) return
  loading.value = true
  stripeError.value = ''
  const stripe = await nuxtApp.$stripe
  if (!stripe || !elements) { stripeError.value = 'Stripe not ready'; loading.value = false; return }
  try {
    const { error } = await stripe.confirmPayment({ elements, redirect: 'if_required' })
    if (error) stripeError.value = error.message || 'Payment failed'
  } catch (e: any) {
    stripeError.value = e?.message || 'Payment failed'
  } finally {
    loading.value = false
  }
}

function currency(n: number) { return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(n) }
</script>
