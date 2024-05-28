import { http } from '@/api/http'

export const priorityListAPI = (project_id) =>
  http.get(`/projects/${project_id}/priorities/`)
