/**
 * Session Manager Composable
 * Handles VNC session creation and management
 */

interface SessionInfo {
  session_id: string
  user_id: string
  task_id?: number
  display: number
  vnc_port: number
  web_port: number
  status: 'creating' | 'active' | 'error'
  created_at: string
  password?: string
}

interface QueueStatus {
  position: number
  total: number
}

interface ResourceStats {
  cpu_percent: number
  memory_percent: number
  active_sessions: number
  max_sessions: number
}

export const useSessionManager = () => {
  const createSession = async (userId: string, taskId?: number): Promise<SessionInfo> => {
    try {
      const response = await $fetch<SessionInfo>('/api/sessions/create', {
        method: 'POST',
        body: {
          user_id: userId,
          task_id: taskId
        }
      })
      return response
    } catch (error: any) {
      console.error('Failed to create session:', error)
      throw new Error(error.data?.detail || 'Failed to create VNC session')
    }
  }

  const getSessionInfo = async (sessionId: string): Promise<SessionInfo> => {
    try {
      const response = await $fetch<SessionInfo>(`/api/sessions/${sessionId}`)
      return response
    } catch (error: any) {
      console.error('Failed to get session info:', error)
      throw new Error(error.data?.detail || 'Failed to get session information')
    }
  }

  const destroySession = async (sessionId: string): Promise<void> => {
    try {
      await $fetch(`/api/sessions/${sessionId}`, {
        method: 'DELETE'
      })
    } catch (error: any) {
      console.error('Failed to destroy session:', error)
      throw new Error(error.data?.detail || 'Failed to destroy session')
    }
  }

  const listSessions = async (): Promise<SessionInfo[]> => {
    try {
      const response = await $fetch<SessionInfo[]>('/api/sessions/')
      return response
    } catch (error: any) {
      console.error('Failed to list sessions:', error)
      throw new Error(error.data?.detail || 'Failed to list sessions')
    }
  }

  const getQueueStatus = async (): Promise<QueueStatus> => {
    try {
      const response = await $fetch<QueueStatus>('/api/sessions/queue/status')
      return response
    } catch (error: any) {
      console.error('Failed to get queue status:', error)
      throw new Error(error.data?.detail || 'Failed to get queue status')
    }
  }

  const getResourceStats = async (): Promise<ResourceStats> => {
    try {
      const response = await $fetch<ResourceStats>('/api/sessions/stats')
      return response
    } catch (error: any) {
      console.error('Failed to get resource stats:', error)
      throw new Error(error.data?.detail || 'Failed to get resource stats')
    }
  }

  const testBrowser = async (sessionId: string, url?: string): Promise<{ status: string; message: string }> => {
    try {
      const response = await $fetch<{ status: string; message: string }>(`/api/test-browser/session/${sessionId}`, {
        method: 'POST',
        body: { url }
      })
      return response
    } catch (error: any) {
      console.error('Failed to test browser:', error)
      throw new Error(error.data?.detail || 'Failed to test browser')
    }
  }

  return {
    createSession,
    getSessionInfo,
    destroySession,
    listSessions,
    getQueueStatus,
    getResourceStats,
    testBrowser
  }
}
