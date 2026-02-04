import { loadStripe } from '@stripe/stripe-js'

export default defineNuxtPlugin(() => {
  const stripePk = useRuntimeConfig().public.stripePk
  const stripe = stripePk ? loadStripe(stripePk) : Promise.resolve(null)
  return { provide: { stripe } }
})
