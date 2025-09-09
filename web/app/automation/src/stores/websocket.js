import { defineStore } from 'pinia'

// Keep WebSocket instances out of Pinia state to avoid SSR serialization issues
const connectionsMap = new Map()

export const useWebSocketStore = defineStore('websocket', {
  state: () => ({

  }),
  
  actions: {
    connect(sessionId) {
      if (!import.meta.client) return null

      // Prevent duplicate connections
      if (connectionsMap.has(sessionId)) {
        return connectionsMap.get(sessionId)
      }
      
      // Build absolute WebSocket URL to route via Nuxt proxy to automation backend
      const apiScheme = (location.protocol === 'https:') ? 'https' : 'http'
      const wsScheme = apiScheme === 'https' ? 'wss' : 'ws'
      const wsUrl = `${wsScheme}://${location.host}/ws/automation/${sessionId}`

      const ws = new WebSocket(wsUrl)
      connectionsMap.set(sessionId, ws)
      
      ws.onopen = () => {
        console.log(`WebSocket connected for session: ${sessionId}`)
      }
      
      ws.onclose = () => {
        console.log(`WebSocket disconnected for session: ${sessionId}`)
        connectionsMap.delete(sessionId)
      }
      
      ws.onerror = (error) => {
        console.error(`WebSocket error for session ${sessionId}:`, error)
      }
      
      return ws
    },
    
    disconnect(sessionId) {
      if (!import.meta.client) return
      const ws = connectionsMap.get(sessionId)
      if (ws) {
        ws.close()
        connectionsMap.delete(sessionId)
      }
    },
    
    disconnectAll() {
      if (!import.meta.client) return
      connectionsMap.forEach(ws => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.close()
        }
      })
      connectionsMap.clear()
    },
    
    sendMessage(sessionId, message) {
      if (!import.meta.client) return
      const ws = connectionsMap.get(sessionId)
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message))
      }
    },
    
    onMessage(sessionId, callback) {
      if (!import.meta.client) return
      const ws = connectionsMap.get(sessionId)
      if (ws) {
        ws.onmessage = callback
      }
    },
    
    getConnectionStatus(sessionId) {
      if (!import.meta.client) return 'disconnected'
      const ws = connectionsMap.get(sessionId)
      if (!ws) return 'disconnected'
      
      switch (ws.readyState) {
        case WebSocket.CONNECTING:
          return 'connecting'
        case WebSocket.OPEN:
          return 'connected'
        case WebSocket.CLOSING:
          return 'closing'
        case WebSocket.CLOSED:
          return 'disconnected'
        default:
          return 'unknown'
      }
    }
  },
  
  getters: {
    isConnected: () => (sessionId) => {
      if (!import.meta.client) return false
      const ws = connectionsMap.get(sessionId)
      return ws && ws.readyState === WebSocket.OPEN
    },
    
    activeConnections: () => {
      if (!import.meta.client) return []
      return Array.from(connectionsMap.keys())
    }
  }
})
