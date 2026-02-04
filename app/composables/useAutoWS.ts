import { computed, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'

type WSStatus = 'closed' | 'connecting' | 'open' | 'reconnecting'

export function useAutoWS(path: string, opts: { protocols?: string | string[], onMessage?: (ev: MessageEvent) => void, onOpen?: () => void, onClose?: () => void, onError?: (ev: Event) => void, heartbeatMs?: number } = {}) {
  const config = useRuntimeConfig()
  const wsUrl = computed(() => {
    const base = config.public.wsBase || ''
    const p = path.startsWith('ws') ? path : `${base}${path.startsWith('/') ? path : `/${path}`}`
    return p
  })
  const status = ref<WSStatus>('closed')
  const ws = shallowRef<WebSocket | null>(null)
  const lastMessage = ref<any>(null)
  let reconnectAttempts = 0
  let reconnectTimer: any
  let heartbeatTimer: any

  const connect = () => {
    if (process.server) return
    try {
      status.value = reconnectAttempts > 0 ? 'reconnecting' : 'connecting'
      const socket = new WebSocket(wsUrl.value, opts.protocols)
      ws.value = socket
      socket.onopen = () => {
        status.value = 'open'
        reconnectAttempts = 0
        if (opts.heartbeatMs && opts.heartbeatMs > 0) {
          clearInterval(heartbeatTimer)
          heartbeatTimer = setInterval(() => {
            try { socket.send(JSON.stringify({ type: 'ping' })) } catch {}
          }, opts.heartbeatMs)
        }
        opts.onOpen && opts.onOpen()
      }
      socket.onmessage = (ev) => {
        lastMessage.value = (() => {
          try { return JSON.parse((ev as any).data) } catch { return (ev as any).data }
        })()
        opts.onMessage && opts.onMessage(ev)
      }
      socket.onerror = (ev) => {
        opts.onError && opts.onError(ev)
      }
      socket.onclose = () => {
        status.value = 'closed'
        clearInterval(heartbeatTimer)
        scheduleReconnect()
        opts.onClose && opts.onClose()
      }
    } catch {
      scheduleReconnect()
    }
  }

  function scheduleReconnect() {
    if (process.server) return
    clearTimeout(reconnectTimer)
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 15000)
    reconnectTimer = setTimeout(() => {
      reconnectAttempts += 1
      connect()
    }, delay)
  }

  function send(data: any) {
    const s = ws.value
    if (!s || s.readyState !== WebSocket.OPEN) return false
    try {
      s.send(typeof data === 'string' ? data : JSON.stringify(data))
      return true
    } catch {
      return false
    }
  }

  function close() {
    clearTimeout(reconnectTimer)
    clearInterval(heartbeatTimer)
    const s = ws.value
    if (s && s.readyState === WebSocket.OPEN) s.close()
    ws.value = null
    status.value = 'closed'
  }

  onMounted(connect)
  onBeforeUnmount(close)

  return { status, lastMessage, send, reconnect: connect, close, ws }
}
