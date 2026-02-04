<template>
  <div class="min-h-screen animated-bg text-[#F2F2F2] font-sans overflow-x-hidden selection:bg-[#FF7A00]/30">
    <!-- Decorative neon glow -->
    <div class="pointer-events-none fixed inset-0 -z-10">
      <div class="absolute -top-40 left-1/2 -translate-x-1/2 h-42 w-96 md:h-[42rem] md:w-[42rem] rounded-full blur-3xl opacity-30 bg-[#FF7A00]/15"></div>
    </div>

    <!-- Header with improved mobile UX -->
    <header ref="header" class="fixed top-0 left-0 right-0 z-50 transition-smooth safe-top">
      <div class="mx-auto max-w-7xl px-4 sm:px-6">
        <div class="flex items-center justify-between h-16 md:h-20">
          <!-- Logo -->
          <NuxtLink to="/" class="inline-flex items-center gap-1.5 -ml-1 tap-target">
            <span class="text-xl md:text-2xl font-extrabold tracking-tight leading-none flex items-center">
              <span>NearB</span>
              <span class="mx-0.5 inline-flex items-center justify-center">
                <svg class="h-5 w-5 md:h-6 md:w-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22s6-5.6 6-10a6 6 0 1 0-12 0c0 4.4 6 10 6 10Z" fill="#FF7A00" fill-opacity="0.2"/>
                  <path d="M12 22s6-5.6 6-10a6 6 0 1 0-12 0c0 4.4 6 10 6 10Z" stroke="#FF7A00" stroke-opacity="0.8" stroke-width="1.25"/>
                  <path d="M9 9.5a3 3 0 1 1 6 0" stroke="#FF7A00" stroke-width="1.5" stroke-linecap="round"/>
                  <circle cx="12" cy="12" r="1.5" fill="#FF7A00" />
                </svg>
              </span>
              <span>y</span>
            </span>
          </NuxtLink>

          <!-- Desktop Nav -->
          <nav class="hidden md:flex items-center gap-4">
            <NuxtLink to="#features" class="px-3 py-2 rounded-full text-sm text-[#F2F2F2]/80 hover:text-[#F2F2F2] hover:bg-[#FF7A00]/10 transition-colors">Features</NuxtLink>
            <NuxtLink to="#partners" class="px-3 py-2 rounded-full text-sm text-[#F2F2F2]/80 hover:text-[#F2F2F2] hover:bg-[#FF7A00]/10 transition-colors">Partners</NuxtLink>
            <NuxtLink to="#explore" class="inline-flex items-center gap-2 rounded-full bg-[#FF7A00] px-5 py-2.5 text-sm font-semibold text-[#F2F2F2] hover:scale-105 transition-transform">
              Explore Nearby
            </NuxtLink>
          </nav>

          <!-- Mobile Menu Button -->
          <button @click="toggleMenu" class="block md:hidden p-2 -mr-2 tap-target" aria-label="Menu">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-show="!menuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              <path v-show="menuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu Dropdown -->
      <div :class="['mobile-menu md:hidden fixed inset-0 pt-16 md:pt-20 overflow-y-auto z-50 bg-[#0A0F1E]', { active: menuOpen }]">
        <button @click="closeMenu" aria-label="Close menu" class="absolute top-4 right-4 p-2 tap-target text-[#F2F2F2]">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
        <nav class="px-4 py-6 space-y-4">
          <NuxtLink to="#features" @click="closeMenu" class="block px-4 py-4 rounded-xl text-base font-medium tap-target bg-[#FF7A00]/10 hover:bg-[#FF7A00]/20 ring-1 ring-[#FF7A00]/20 text-[#F2F2F2]">Features</NuxtLink>
          <NuxtLink to="#partners" @click="closeMenu" class="block px-4 py-4 rounded-xl text-base font-medium tap-target bg-[#FF7A00]/10 hover:bg-[#FF7A00]/20 ring-1 ring-[#FF7A00]/20 text-[#F2F2F2]">Partners</NuxtLink>
          <NuxtLink to="#explore" @click="closeMenu" class="block px-4 py-4 rounded-xl text-base font-medium tap-target bg-[#FF7A00]/10 hover:bg-[#FF7A00]/20 ring-1 ring-[#FF7A00]/20 text-[#F2F2F2]">Explore Nearby</NuxtLink>
        </nav>
      </div>
    </header>

    <main class="pt-16 md:pt-20">
      <!-- Hero Section - Mobile Optimized -->
      <section class="relative px-4 sm:px-6 pt-8 md:pt-16 pb-12 md:pb-20">
        <div class="mx-auto max-w-7xl">
          <div class="grid md:grid-cols-2 gap-8 md:gap-12 items-center">
            <!-- Text Content -->
            <div class="space-y-5 md:space-y-6 text-center md:text-left fade-in">
              <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.1]">
                <span class="text-[#FF7A00]">Your Neighborhood,</span>
                <br/>
                <span class="text-[#F2F2F2]">Synced to Your Schedule.</span>
              </h1>
              <p class="text-base sm:text-lg md:text-xl text-[#F2F2F2]/80 max-w-xl mx-auto md:mx-0">
                NearBuy bridges the gap between your busy day and local shelves. Real-time shopping from the stores you trust, delivered to your door in minutes.
              </p>
              
              <!-- CTA Buttons -->
              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 pt-2" id="explore">
                <a href="#features" class="btn-primary inline-flex items-center justify-center gap-2 rounded-full bg-[#FF7A00] px-6 py-3.5 sm:py-4 text-[#F2F2F2] font-semibold shadow-lg transition-smooth tap-target">
                  <span>Explore Nearby Stores</span>
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                  </svg>
                </a>
                <a href="#partners" class="inline-flex items-center justify-center gap-2 rounded-full glass px-6 py-3.5 sm:py-4 text-[#F2F2F2]/90 font-medium hover:bg-[#F2F2F2]/10 transition-smooth tap-target">
                  Become a Partner
                </a>
              </div>

              <!-- Trust Indicators -->
              <div class="flex flex-wrap items-center justify-center md:justify-start gap-4 sm:gap-6 pt-4 text-xs sm:text-sm text-[#F2F2F2]/60">
                <div class="flex items-center gap-2">
                  <span class="h-2 w-2 rounded-full bg-[#FF7A00] pulse-glow"></span>
                  <span>Real-time sync</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="h-2 w-2 rounded-full bg-[#FF7A00]"></span>
                  <span>PostGIS proximity</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="h-2 w-2 rounded-full bg-[#F2F2F2]/50"></span>
                  <span>PWA-ready</span>
                </div>
              </div>
            </div>

            <!-- Phone Mockup - Optimized for mobile -->
            <div class="relative flex justify-center md:justify-end mt-8 md:mt-0 phone-mockup fade-in">
              <div class="relative phone-3d">
                <div class="relative h-[480px] sm:h-[540px] w-[260px] sm:w-[290px] rounded-[2rem] sm:rounded-[2.2rem] glass-strong shadow-2xl overflow-hidden">
                  <!-- Phone notch -->
                  <div class="absolute top-0 left-1/2 -translate-x-1/2 h-6 w-24 sm:w-28 rounded-b-2xl bg-black/60 z-10"></div>
                  
                  <!-- Screen content -->
                  <div class="absolute inset-0 bg-[#0A0F1E]">
                    <!-- App header in phone -->
                    <div class="relative z-10 px-6 pt-10 pb-4 flex items-center justify-between">
                      <span class="text-xs font-semibold text-[#F2F2F2]/90">Find Stores Near You</span>
                      <div class="h-8 w-8 rounded-full glass flex items-center justify-center">
                        <svg class="h-4 w-4 text-[#FF7A00]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                      </div>
                    </div>

                    <!-- Radar visualization -->
                    <div class="absolute inset-0 flex items-center justify-center">
                      <div class="relative h-52 sm:h-60 w-52 sm:w-60">
                        <!-- Radar rings -->
                        <div class="absolute inset-0 rounded-full border border-[#FF7A00]/40"></div>
                        <div class="absolute inset-4 rounded-full border border-[#FF7A00]/30"></div>
                        <div class="absolute inset-8 rounded-full border border-[#FF7A00]/20"></div>
                        <div class="absolute inset-12 rounded-full border border-[#FF7A00]/10"></div>
                        
                        <!-- Center point (user location) -->
                        <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
                          <div class="h-3 w-3 rounded-full bg-[#FF7A00] shadow-[0_0_20px_4px_rgba(255,122,0,0.35)]"></div>
                          <div class="absolute inset-0 h-3 w-3 rounded-full bg-[#FF7A00] radar-ping"></div>
                        </div>

                        <!-- Store markers -->
                        <span class="absolute left-8 top-16 h-2.5 w-2.5 rounded-full bg-[#FF7A00] shadow-[0_0_12px_2px_rgba(255,122,0,0.45)] pulse-glow"></span>
                        <span class="absolute right-8 top-32 h-2.5 w-2.5 rounded-full bg-[#FF7A00] shadow-[0_0_12px_2px_rgba(255,122,0,0.35)] pulse-glow" style="animation-delay: 0.5s;"></span>
                        <span class="absolute left-16 bottom-16 h-2 w-2 rounded-full bg-[#F2F2F2]/70"></span>
                        <span class="absolute right-12 bottom-24 h-2 w-2 rounded-full bg-[#F2F2F2]/60"></span>
                      </div>
                    </div>

                    <!-- Bottom card preview in phone -->
                    <div class="absolute bottom-6 left-4 right-4 glass-strong rounded-2xl p-4 z-10">
                      <div class="flex items-start gap-3">
                        <div class="h-12 w-12 rounded-xl bg-[#FF7A00]/20 flex items-center justify-center flex-shrink-0">
                          <svg class="h-6 w-6 text-[#FF7A00]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/>
                          </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-center gap-2 mb-1">
                            <p class="text-xs font-semibold text-[#F2F2F2] truncate">Corner Grocery</p>
                            <span class="text-[10px] text-[#FF7A00] font-medium">0.3 mi</span>
                          </div>
                          <p class="text-[10px] text-[#F2F2F2]/60">Open until 9:00 PM</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Glow effect -->
                <div class="absolute -bottom-8 left-1/2 h-20 w-48 sm:w-64 -translate-x-1/2 rounded-full blur-2xl bg-[#FF7A00]/30 pointer-events-none"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section - Card-based for mobile -->
      <section id="features" class="relative px-4 sm:px-6 py-12 md:py-16">
        <div class="mx-auto max-w-7xl">
          <!-- Section header for mobile -->
          <div class="text-center mb-8 md:mb-10 fade-in">
            <h2 class="text-2xl sm:text-3xl md:text-4xl font-bold mb-3">Built for Speed & Convenience</h2>
            <p class="text-[#F2F2F2]/70 text-sm sm:text-base max-w-2xl mx-auto">Everything you need for seamless local shopping</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            <!-- Feature Card 1 -->
            <div class="card-hover glass rounded-2xl sm:rounded-3xl p-6 sm:p-8 transition-smooth tap-target fade-in">
              <div class="h-12 w-12 sm:h-14 sm:w-14 rounded-xl sm:rounded-2xl bg-[#FF7A00]/15 ring-1 ring-[#FF7A00]/40 flex items-center justify-center mb-4 sm:mb-5">
                <svg class="h-6 w-6 sm:h-7 sm:w-7 text-[#FF7A00]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M4 4v6h6"/>
                  <path d="M20 20v-6h-6"/>
                  <path d="M20 4h-8a8 8 0 0 0-8 8v8"/>
                </svg>
              </div>
              <h3 class="text-lg sm:text-xl font-bold mb-2 sm:mb-3">Real-Time Sync</h3>
              <p class="text-[#F2F2F2]/70 text-sm sm:text-base leading-relaxed">Django-powered live tracking. See exactly when your order is picked, packed, and en route.</p>
            </div>

            <!-- Feature Card 2 -->
            <div class="card-hover glass rounded-2xl sm:rounded-3xl p-6 sm:p-8 transition-smooth tap-target fade-in" style="animation-delay: 0.1s;">
              <div class="h-12 w-12 sm:h-14 sm:w-14 rounded-xl sm:rounded-2xl bg-[#FF7A00]/15 ring-1 ring-[#FF7A00]/40 flex items-center justify-center mb-4 sm:mb-5">
                <svg class="h-6 w-6 sm:h-7 sm:w-7 text-[#FF7A00]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 22s6-5.6 6-10a6 6 0 1 0-12 0c0 4.4 6 10 6 10Z"/>
                  <circle cx="12" cy="12" r="2"/>
                </svg>
              </div>
              <h3 class="text-lg sm:text-xl font-bold mb-2 sm:mb-3">Smart Proximity</h3>
              <p class="text-[#F2F2F2]/70 text-sm sm:text-base leading-relaxed">Our PostGIS engine finds the closest store to save you delivery fees and time.</p>
            </div>

            <!-- Feature Card 3 -->
            <div class="card-hover glass rounded-2xl sm:rounded-3xl p-6 sm:p-8 transition-smooth tap-target fade-in" style="animation-delay: 0.2s;">
              <div class="h-12 w-12 sm:h-14 sm:w-14 rounded-xl sm:rounded-2xl bg-[#FF7A00]/15 ring-1 ring-[#FF7A00]/40 flex items-center justify-center mb-4 sm:mb-5">
                <svg class="h-6 w-6 sm:h-7 sm:w-7 text-[#FF7A00]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M8 7h8M8 12h5M5 7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v10l-4-3-4 3-4-3-4 3V7Z"/>
                </svg>
              </div>
              <h3 class="text-lg sm:text-xl font-bold mb-2 sm:mb-3">PWA Performance</h3>
              <p class="text-[#F2F2F2]/70 text-sm sm:text-base leading-relaxed">No App Store required. Add to home screen and order in one tap.</p>
            </div>
          </div>
        </div>
      </section>  

      <!-- Partner Section - Mobile Optimized -->
      <section id="partners" class="relative px-4 sm:px-6 py-12 md:py-16">
        <div class="mx-auto max-w-7xl">
          <div class="glass-strong rounded-2xl sm:rounded-3xl p-6 sm:p-8 md:p-12 fade-in">
            <div class="text-center md:text-left md:grid md:grid-cols-2 md:gap-12 md:items-center">
              <div class="mb-6 md:mb-0">
                <h2 class="text-xl sm:text-2xl md:text-3xl font-bold tracking-tight mb-3 sm:mb-4">Store Partner Logistics, Off Your Plate</h2>
                <p class="text-[#F2F2F2]/75 text-sm sm:text-base leading-relaxed">Too busy to manage your own deliveries? Let NearBuy handle the logistics while you focus on your inventory.</p>
              </div>
              <div class="flex md:justify-end">
                <a href="#" class="btn-primary w-full md:w-auto inline-flex items-center justify-center rounded-full glass-strong px-6 py-3.5 sm:py-4 text-[#F2F2F2] font-semibold hover:bg-[#F2F2F2]/15 transition-smooth tap-target">
                  Talk to Sales
                  <svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Social Proof Section -->
      <section class="relative px-4 sm:px-6 py-12 md:py-16">
        <div class="mx-auto max-w-7xl">
          <div class="text-center space-y-8 fade-in">
            <div>
              <p class="text-sm sm:text-base text-[#F2F2F2]/60 font-medium mb-4">Trusted by local communities</p>
              <div class="flex flex-wrap items-center justify-center gap-6 sm:gap-12">
                <div class="text-center">
                  <div class="text-3xl sm:text-4xl font-bold text-[#FF7A00] mb-1">5k+</div>
                  <div class="text-xs sm:text-sm text-[#F2F2F2]/60">Active Users</div>
                </div>
                <div class="text-center">
                  <div class="text-3xl sm:text-4xl font-bold text-[#FF7A00] mb-1">200+</div>
                  <div class="text-xs sm:text-sm text-[#F2F2F2]/60">Partner Stores</div>
                </div>
                <div class="text-center">
                  <div class="text-3xl sm:text-4xl font-bold text-[#FF7A00] mb-1">15min</div>
                  <div class="text-xs sm:text-sm text-[#F2F2F2]/60">Avg Delivery</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom spacer for FAB -->
      <div class="h-24 md:h-0"></div>
    </main>

    <!-- Floating Action Button (Mobile Only) -->
    <div class="fixed bottom-0 left-0 right-0 md:hidden z-40 safe-bottom" v-show="!menuOpen">
      <div class="px-4 pb-4">
        <a href="#features" id="cta" class="fab btn-primary flex items-center justify-center w-full rounded-full bg-[#FF7A00] px-6 py-4 text-[#F2F2F2] font-bold text-base transition-smooth tap-target">
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          Order Now
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

useHead({
  title: 'NearBuy — Hyper-local Real‑Time Delivery',
  meta: [
    { name: 'description', content: 'NearBuy bridges the gap between your busy day and local shelves. Real-time shopping from the stores you trust, delivered to your door in minutes.' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover' },
    { name: 'theme-color', content: '#0A0F1E' },
    { name: 'apple-mobile-web-app-capable', content: 'yes' },
    { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }
  ],
  link: [
    { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
    { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: 'anonymous' },
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap' }
  ]
})

const menuOpen = ref(false)
const header = ref<HTMLElement | null>(null)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

// Header scroll effect
const handleScroll = () => {
  if (!header.value) return
  
  const currentScroll = window.pageYOffset
  
  if (currentScroll > 20) {
    header.value.classList.add('glass', 'header-shadow')
  } else {
    header.value.classList.remove('glass', 'header-shadow')
  }
}

// Intersection Observer for fade-in animations
const setupIntersectionObserver = () => {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
      }
    })
  }, observerOptions)

  document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el)
  })
}

// Smooth scroll for anchor links
const setupSmoothScroll = () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (this: HTMLAnchorElement, e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href') as string)
      if (target) {
        const headerOffset = 80
        const elementPosition = target.getBoundingClientRect().top
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        })
      }
    })
  })
}

// Prevent pull-to-refresh on iOS
const preventPullToRefresh = () => {
  let startY = 0
  
  document.addEventListener('touchstart', (e: TouchEvent) => {
    const firstTouch = e.touches[0]
    if (!firstTouch) return
    startY = firstTouch.pageY
  }, { passive: true })

  document.addEventListener('touchmove', (e: TouchEvent) => {
    const firstTouch = e.touches[0]
    if (!firstTouch) return
    const y = firstTouch.pageY
    if (window.pageYOffset === 0 && y > startY) {
      e.preventDefault()
    }
  }, { passive: false })
}

// Haptic feedback for buttons
const setupHapticFeedback = () => {
  if ('vibrate' in navigator) {
    document.querySelectorAll('.btn-primary, .tap-target').forEach(btn => {
      btn.addEventListener('click', () => {
        navigator.vibrate(10)
      })
    })
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  setupIntersectionObserver()
  setupSmoothScroll()
  preventPullToRefresh()
  setupHapticFeedback()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.body.style.overflow = ''
})

watch(menuOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})
</script>

<style scoped>
* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Animated gradient background */
.animated-bg {
  background: #0A0F1E;
}


/* Pulse animation for dots */
@keyframes pulse-glow {
  0%, 100% { 
    opacity: 1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

/* Radar animation */
@keyframes radar-ping {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.radar-ping {
  animation: radar-ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

/* Smooth transitions */
.transition-smooth {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Active/touch states */
.btn-primary:active {
  transform: scale(0.97);
}

.card-hover:active {
  transform: scale(0.98);
}

/* Safe area insets for notched devices */
.safe-top {
  padding-top: max(1rem, env(safe-area-inset-top));
}

.safe-bottom {
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}

/* Glassmorphism enhanced */
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-strong {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

/* Hero gradient text */
.gradient-text {
  color: #FF7A00;
}

/* Mobile menu transition */
.mobile-menu {
  transform: translateY(-100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-menu.active {
  transform: translateY(0);
}

/* Floating action button */
.fab {
  box-shadow: 0 8px 24px rgba(204, 255, 0, 0.25), 0 0 40px rgba(204, 255, 0, 0.15);
}

.fab:active {
  box-shadow: 0 4px 12px rgba(204, 255, 0, 0.2), 0 0 20px rgba(204, 255, 0, 0.1);
}

/* Intersection observer fade-in */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Sticky header shadow */
.header-shadow {
  box-shadow: 0 1px 20px rgba(0, 0, 0, 0.1);
}

/* Phone mockup */
.phone-mockup {
  perspective: 1000px;
}

.phone-3d {
  transform: rotateY(-5deg) rotateX(2deg);
  transition: transform 0.5s ease;
}

@media (max-width: 768px) {
  .phone-3d {
    transform: rotateY(0deg) rotateX(0deg);
  }
}

/* Tap target sizing */
.tap-target {
  min-height: 44px;
  min-width: 44px;
  align-items: center;
  justify-content: center;
}

/* Remove tap highlight */
* {
  -webkit-tap-highlight-color: transparent;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 122, 0, 0.3);
  border-radius: 2px;
}
</style>