import { http } from '@/api/http'

export const taskUpdateAPI = (project_id, task_id, data, params) =>
  http.patch(`/projects/${project_id}/tasks/${task_id}/`, data, {
    params,
  })

export const taskAddAPI = (project_id, data, params = {}) =>
  http.post(`/projects/${project_id}/tasks/`, data, {
    params,
  })

export const taskDetailAPI = (projectId, taskId, params = {}) =>
  http.get(`/projects/${projectId}/tasks/${taskId}/`, params)

export const attachmentListAPI = (projectId, taskId) =>
  http.get(`/projects/${projectId}/tasks/${taskId}/attachments/`)

export const commentListAPI = (projectId, taskId) =>
  http.get(`/projects/${projectId}/tasks/${taskId}/comments/`)
