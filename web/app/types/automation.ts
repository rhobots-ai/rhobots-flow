export interface AutomationTask {
  id: string
  name: string
  description: string
  status: TaskStatus
  lastRun?: string
  createdAt: string
  updatedAt: string
  steps: AutomationStep[]
  prerequisites: Prerequisite[]
  settings: TaskSettings
}

export interface AutomationStep {
  id: string
  type: StepType
  selector?: string
  action: StepAction
  value?: string
  waitTime?: number
  screenshot?: boolean
  description: string
  order: number
}

export interface Prerequisite {
  id: string
  type: PrerequisiteType
  label: string
  required: boolean
  value?: any
  validation?: ValidationRule[]
}

export interface TaskSettings {
  headless: boolean
  takeScreenshots: boolean
  timeout: number
  retryAttempts: number
  waitBetweenSteps: number
}

export interface RunHistory {
  id: string
  taskId: string
  status: RunStatus
  startTime: string
  endTime?: string
  duration?: string
  screenshots: string[]
  logs: RunLog[]
  error?: string
}

export interface RunLog {
  id: string
  timestamp: string
  level: LogLevel
  message: string
  stepId?: string
}

export interface ValidationRule {
  type: 'required' | 'minLength' | 'maxLength' | 'pattern' | 'email' | 'url'
  value?: any
  message: string
}

export interface CreateTaskData {
  name: string
  description: string
  prerequisites: Omit<Prerequisite, 'id'>[]
  steps: Omit<AutomationStep, 'id'>[]
  settings: TaskSettings
}

export interface DynamicField {
  id: string
  type: 'text' | 'email' | 'url' | 'number' | 'select' | 'file'
  label: string
  placeholder?: string
  required: boolean
  options?: string[]
  value?: any
}

// Enums
export enum TaskStatus {
  DRAFT = 'draft',
  READY = 'ready',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  PAUSED = 'paused'
}

export enum RunStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum StepType {
  NAVIGATE = 'navigate',
  CLICK = 'click',
  TYPE = 'type',
  WAIT = 'wait',
  SCROLL = 'scroll',
  SCREENSHOT = 'screenshot',
  EXTRACT = 'extract',
  CUSTOM = 'custom'
}

export enum StepAction {
  NAVIGATE_TO = 'navigate_to',
  CLICK_ELEMENT = 'click_element',
  TYPE_TEXT = 'type_text',
  WAIT_FOR_ELEMENT = 'wait_for_element',
  WAIT_FOR_TIME = 'wait_for_time',
  SCROLL_TO = 'scroll_to',
  TAKE_SCREENSHOT = 'take_screenshot',
  EXTRACT_TEXT = 'extract_text',
  EXTRACT_ATTRIBUTE = 'extract_attribute',
  EXECUTE_SCRIPT = 'execute_script',
  INTERACTIVE_PAUSE = 'interactive_pause'
}

export enum PrerequisiteType {
  FILE_UPLOAD = 'file_upload',
  TEXT_INPUT = 'text_input',
  URL_INPUT = 'url_input',
  SELECT = 'select',
  NUMBER_INPUT = 'number_input'
}

export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error'
}
