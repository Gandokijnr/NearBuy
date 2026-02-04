<template>
  <div class="min-h-screen bg-[#0A0F1E] text-[#F2F2F2]">
    <header class="border-b border-white/10 bg-white/5">
      <div class="max-w-6xl mx-auto px-4 py-4 flex items-center gap-6">
        <NuxtLink to="/" class="font-bold text-lg">NearBuy Merchant</NuxtLink>
        <nav class="flex gap-2 text-sm">
          <NuxtLink to="/merchant/orders" class="px-3 py-1 rounded-full hover:bg-white/10" :class="{ 'bg-[#FF7A00] text-[#0A0F1E] hover:bg-[#FF7A00]': isActive('/merchant/orders') }">Incoming</NuxtLink>
          <NuxtLink to="/merchant/board" class="px-3 py-1 rounded-full hover:bg-white/10" :class="{ 'bg-[#FF7A00] text-[#0A0F1E] hover:bg-[#FF7A00]': isActive('/merchant/board') }">Orders</NuxtLink>
          <NuxtLink to="/merchant/inventory" class="px-3 py-1 rounded-full hover:bg-white/10" :class="{ 'bg-[#FF7A00] text-[#0A0F1E] hover:bg-[#FF7A00]': isActive('/merchant/inventory') }">Inventory</NuxtLink>
          <NuxtLink to="/merchant/earnings" class="px-3 py-1 rounded-full hover:bg-white/10" :class="{ 'bg-[#FF7A00] text-[#0A0F1E] hover:bg-[#FF7A00]': isActive('/merchant/earnings') }">Earnings</NuxtLink>
        </nav>
      </div>
    </header>
    <main class="max-w-6xl mx-auto px-4 py-6">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
function isActive(path: string) {
  return route.path.startsWith(path)
}
</script>
