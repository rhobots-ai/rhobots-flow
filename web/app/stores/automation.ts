import { defineStore } from 'pinia'
import type { 
  AutomationTask, 
  RunHistory, 
  CreateTaskData 
} from '~/types/automation'
import { TaskStatus, RunStatus, StepType, StepAction } from '~/types/automation'
import { HttpClient } from '~/api/http'

const ENABLE_RUNS_API = false

interface AutomationState {
  tasks: AutomationTask[]
  selectedTask: AutomationTask | null
  isRunning: boolean
  currentSessionId: string | null
  runHistory: RunHistory[]
  isLoading: boolean
  searchQuery: string
  filterStatus: TaskStatus | 'all'
}

export const useAutomationStore = defineStore('automation', {
  state: (): AutomationState => ({
    tasks: [],
    selectedTask: null,
    isRunning: false,
    currentSessionId: null,
    runHistory: [],
    isLoading: false,
    searchQuery: '',
    filterStatus: 'all'
  }),

  getters: {
    filteredTasks: (state) => {
      let filtered = state.tasks

      // Filter by search query
      if (state.searchQuery) {
        const query = state.searchQuery.toLowerCase()
        filtered = filtered.filter(task => 
          task.name.toLowerCase().includes(query) ||
          task.description.toLowerCase().includes(query)
        )
      }

      // Filter by status
      if (state.filterStatus !== 'all') {
        filtered = filtered.filter(task => task.status === state.filterStatus)
      }

      return filtered.sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    },

    taskById: (state) => (id: string) => {
      return state.tasks.find(task => task.id === id)
    },

    runHistoryForTask: (state) => (taskId: string) => {
      return state.runHistory
        .filter(run => run.taskId === taskId)
        .sort((a, b) => new Date(b.startTime).getTime() - new Date(a.startTime).getTime())
    },

    recentRuns: (state) => {
      return state.runHistory
        .slice(0, 10)
        .sort((a, b) => new Date(b.startTime).getTime() - new Date(a.startTime).getTime())
    }
  },

  actions: {
    // Task Management
    async fetchTasks() {
      this.isLoading = true
      try {
        const http = new HttpClient('/api')
        const { data, error } = await http.get<{ data: AutomationTask[] }>('/system/automations/tasks')
        if (error) throw error
        this.tasks = (data as unknown as { data: AutomationTask[] })?.data || []
      } catch (error) {
        console.error('Failed to fetch tasks:', error)
        // Set mock data for development
        this.tasks = this.getMockTasks()
      } finally {
        this.isLoading = false
      }
    },

    async createTask(taskData: CreateTaskData): Promise<AutomationTask> {
      this.isLoading = true
      try {
        const http = new HttpClient('/api')
        const { data, error } = await http.post<{ data: AutomationTask }>('/system/automations/tasks', taskData)
        if (error) throw error

        const newTask = (data as unknown as { data: AutomationTask })?.data
        if (!newTask) throw new Error('Invalid response while creating task')

        this.tasks.push(newTask)
        return newTask
      } catch (error) {
        console.error('Failed to create task:', error)
        // Create mock task for development
        const mockTask = this.createMockTask(taskData)
        this.tasks.push(mockTask)
        return mockTask
      } finally {
        this.isLoading = false
      }
    },

    async updateTask(taskId: string, updates: Partial<AutomationTask>) {
      this.isLoading = true
      try {
        const http = new HttpClient('/api')
        const { data, error } = await http.patch<{ data: AutomationTask }>(`/system/automations/tasks/${taskId}`, updates)
        if (error) throw error

        const updatedTask = (data as unknown as { data: AutomationTask })?.data
        const index = this.tasks.findIndex(task => task.id === taskId)
        if (updatedTask && index !== -1) {
          this.tasks[index] = updatedTask
          if (this.selectedTask?.id === taskId) {
            this.selectedTask = updatedTask
          }
        }
      } catch (error) {
        console.error('Failed to update task:', error)
        // Update mock task for development
        const index = this.tasks.findIndex(task => task.id === taskId)
        if (index !== -1) {
          this.tasks[index] = { 
            ...this.tasks[index], 
            ...updates, 
            updatedAt: new Date().toISOString() 
          } as AutomationTask
          if (this.selectedTask?.id === taskId) {
            this.selectedTask = this.tasks[index]
          }
        }
      } finally {
        this.isLoading = false
      }
    },

    async deleteTask(taskId: string) {
      this.isLoading = true
      try {
        const http = new HttpClient('/api')
        const { error } = await http.delete(`/system/automations/tasks/${taskId}`)
        if (error) throw error
        
        this.tasks = this.tasks.filter(task => task.id !== taskId)
        if (this.selectedTask?.id === taskId) {
          this.selectedTask = null
        }
      } catch (error) {
        console.error('Failed to delete task:', error)
        // Delete mock task for development
        this.tasks = this.tasks.filter(task => task.id !== taskId)
        if (this.selectedTask?.id === taskId) {
          this.selectedTask = null
        }
      } finally {
        this.isLoading = false
      }
    },

    async duplicateTask(taskId: string) {
      const originalTask = this.taskById(taskId)
      if (!originalTask) return

      const duplicateData: CreateTaskData = {
        name: `${originalTask.name} (Copy)`,
        description: originalTask.description,
        prerequisites: originalTask.prerequisites.map(p => ({ ...p, value: undefined })),
        steps: originalTask.steps,
        settings: originalTask.settings
      }

      return await this.createTask(duplicateData)
    },

    // Task Execution
    async runTask(taskId: string) {
      const task = this.taskById(taskId)
      if (!task) return

      this.isRunning = true
      this.currentSessionId = `session_${Date.now()}`
      
      try {
        if (taskId === 'task_test') {
          // For test task, use the live automation endpoint with auth headers
          const http = new HttpClient('/api')
          const { data, error } = await http.post<{ status: string }>(
            '/system/automations/start/',
            { sessionId: this.currentSessionId }
          )
          if (error) throw error

          // Update task status
          await this.updateTask(taskId, { status: TaskStatus.RUNNING })

          // Simulate run completion for demo
          setTimeout(() => {
            this.isRunning = false
            this.currentSessionId = null
            this.updateTask(taskId, { 
              status: TaskStatus.COMPLETED,
              lastRun: new Date().toISOString()
            })
          }, 30000) // 30 seconds demo
          
          return data
        } else {
          // If runs API is not implemented on backend, simulate behavior
          if (!ENABLE_RUNS_API) {
            await this.updateTask(taskId, { status: TaskStatus.RUNNING })
            setTimeout(async () => {
              this.isRunning = false
              this.currentSessionId = null
              await this.updateTask(taskId, { 
                status: TaskStatus.COMPLETED,
                lastRun: new Date().toISOString()
              })
            }, 5000)
            return { runId: `run_${Date.now()}` } as unknown as { runId: string }
          }

          // Actual API call (requires backend support)
          const http = new HttpClient('/api')
          const { data, error } = await http.post<{ runId: string }>(
            `/system/automations/tasks/${taskId}/run`,
            { sessionId: this.currentSessionId }
          )
          if (error) throw error

          // Update task status
          await this.updateTask(taskId, { status: TaskStatus.RUNNING })

          // Start polling for run status
          this.pollRunStatus(taskId, (data as unknown as { runId: string }).runId)
          
          return data
        }
      } catch (error) {
        console.error('Failed to start task:', error)
        this.isRunning = false
        this.currentSessionId = null
        await this.updateTask(taskId, { status: TaskStatus.FAILED })
        throw error
      }
    },

    async stopTask(taskId: string) {
      try {
        if (taskId === 'task_test') {
          const http = new HttpClient('/api')
          if (this.currentSessionId) {
            await http.post('/system/automations/stop/', { sessionId: this.currentSessionId })
          }
        } else {
          if (ENABLE_RUNS_API) {
            const http = new HttpClient('/api')
            await http.post(`/system/automations/tasks/${taskId}/stop`, {})
          }
        }
        
        this.isRunning = false
        this.currentSessionId = null
        await this.updateTask(taskId, { status: TaskStatus.PAUSED })
      } catch (error) {
        console.error('Failed to stop task:', error)
        throw error
      }
    },

    // Run History
    async fetchRunHistory(taskId?: string) {
      try {
        if (!ENABLE_RUNS_API) {
          this.runHistory = this.getMockRunHistory(taskId)
          return
        }
        const http = new HttpClient('/api')
        const endpoint = taskId ? `/system/automations/runs?taskId=${taskId}` : '/system/automations/runs'
        const { data, error } = await http.get<{ data: RunHistory[] }>(endpoint, undefined, undefined, true)
        if (error) throw error
        this.runHistory = (data as unknown as { data: RunHistory[] })?.data || []
      } catch (error) {
        console.error('Failed to fetch run history:', error)
        // Set mock data for development
        this.runHistory = this.getMockRunHistory(taskId)
      }
    },

    // UI State Management
    selectTask(task: AutomationTask | null) {
      this.selectedTask = task
      if (task) {
        this.fetchRunHistory(task.id)
      }
    },

    setSearchQuery(query: string) {
      this.searchQuery = query
    },

    setFilterStatus(status: TaskStatus | 'all') {
      this.filterStatus = status
    },

    // Utility Methods
    async pollRunStatus(taskId: string, runId: string) {
      if (!ENABLE_RUNS_API) return

      const poll = async () => {
        try {
          const http = new HttpClient('/api')
          const { data, error } = await http.get<{ data: RunHistory }>(`/system/automations/runs/${runId}`)
          if (error) throw error
          const run = (data as unknown as { data: RunHistory })?.data
          
          if (run && (run.status === RunStatus.COMPLETED || run.status === RunStatus.FAILED)) {
            this.isRunning = false
            this.currentSessionId = null
            
            const newStatus = run.status === RunStatus.COMPLETED 
              ? TaskStatus.COMPLETED 
              : TaskStatus.FAILED
            
            await this.updateTask(taskId, { 
              status: newStatus,
              lastRun: new Date().toISOString()
            })
            
            await this.fetchRunHistory(taskId)
          } else {
            setTimeout(poll, 2000) // Poll every 2 seconds
          }
        } catch (error) {
          console.error('Failed to poll run status:', error)
          setTimeout(poll, 5000) // Retry after 5 seconds on error
        }
      }
      
      poll()
    },

    createMockTask(taskData: CreateTaskData): AutomationTask {
      return {
        id: `task_${Date.now()}`,
        ...taskData,
        status: TaskStatus.DRAFT,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        prerequisites: taskData.prerequisites.map((p, index) => ({
          ...p,
          id: `prereq_${Date.now()}_${index}`
        })),
        steps: taskData.steps.map((s, index) => ({
          ...s,
          id: `step_${Date.now()}_${index}`
        }))
      }
    },

    getMockTasks(): AutomationTask[] {
      return [
        {
          id: 'task_1',
          name: 'Data Entry Automation',
          description: 'Automates data entry from Excel to web forms',
          status: TaskStatus.READY,
          lastRun: '2024-01-15T10:30:00Z',
          createdAt: '2024-01-10T09:00:00Z',
          updatedAt: '2024-01-15T10:30:00Z',
          steps: [],
          prerequisites: [],
          settings: {
            headless: false,
            takeScreenshots: true,
            timeout: 30000,
            retryAttempts: 3,
            waitBetweenSteps: 1000
          }
        },
        {
          id: 'task_2',
          name: 'Invoice Processing',
          description: 'Processes invoices from uploaded PDFs',
          status: TaskStatus.COMPLETED,
          lastRun: '2024-01-14T15:45:00Z',
          createdAt: '2024-01-08T14:00:00Z',
          updatedAt: '2024-01-14T15:45:00Z',
          steps: [],
          prerequisites: [],
          settings: {
            headless: true,
            takeScreenshots: false,
            timeout: 60000,
            retryAttempts: 2,
            waitBetweenSteps: 500
          }
        },
        {
          id: 'task_test',
          name: 'Live Browser Test',
          description: 'Interactive test automation with live browser view using Playwright + VNC',
          status: TaskStatus.READY,
          lastRun: '2024-01-16T11:20:00Z',
          createdAt: '2024-01-16T09:00:00Z',
          updatedAt: '2024-01-16T11:20:00Z',
          steps: [
            {
              id: 'step_1',
              type: StepType.NAVIGATE,
              action: StepAction.NAVIGATE_TO,
              value: 'https://angularformadd.netlify.app/',
              description: 'Navigate to test form website',
              order: 1
            },
            {
              id: 'step_2',
              type: StepType.WAIT,
              action: StepAction.WAIT_FOR_ELEMENT,
              selector: 'form',
              description: 'Wait for form to load',
              order: 2
            },
            {
              id: 'step_3',
              type: StepType.CUSTOM,
              action: StepAction.INTERACTIVE_PAUSE,
              description: 'Hand over control for user interaction',
              order: 3
            },
            {
              id: 'step_4',
              type: StepType.CLICK,
              action: StepAction.CLICK_ELEMENT,
              selector: 'text=Add Route',
              description: 'Click Add Route button',
              order: 4
            }
          ],
          prerequisites: [],
          settings: {
            headless: false,
            takeScreenshots: true,
            timeout: 30000,
            retryAttempts: 1,
            waitBetweenSteps: 2000
          }
        }
      ]
    },

    getMockRunHistory(taskId?: string): RunHistory[] {
      const mockRuns = [
        {
          id: 'run_1',
          taskId: 'task_1',
          status: RunStatus.COMPLETED,
          startTime: '2024-01-15T10:30:00Z',
          endTime: '2024-01-15T10:35:00Z',
          duration: '5m 23s',
          screenshots: [],
          logs: []
        },
        {
          id: 'run_2',
          taskId: 'task_1',
          status: RunStatus.FAILED,
          startTime: '2024-01-15T09:15:00Z',
          endTime: '2024-01-15T09:18:00Z',
          duration: '2m 45s',
          screenshots: [],
          logs: [],
          error: 'Element not found: #submit-button'
        }
      ]

      return taskId ? mockRuns.filter(run => run.taskId === taskId) : mockRuns
    }
  }
})
