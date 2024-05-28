<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { labelListAPI } from '@/api/labels'
import { priorityListAPI } from '@/api/priorities'
import { taskUpdateAPI } from '@/api/tasks'
import { stateTaskListAPI } from '@/api/states'
import { projectMembersAPI } from '@/api/projects'
import { VueDraggable } from 'vue-draggable-plus'
import draggable from 'vuedraggable'

import DashboardLayout from '@/components/layouts/dashboard-layout.vue'
import TaskCard from '@/components/projects/detail/task-card.vue'
import TaskFilters from '@/components/projects/detail/task-filters.vue'
import LoadingSpinner from '@/components/common/loading-spinner.vue'
import TaskAddForm from '@/components/projects/detail/task-add-form.vue'
import { message } from 'ant-design-vue'

const props = defineProps(['project'])

const loading = ref(false)
const project = ref(props.project)
const members = ref([])
const states = ref([])
const labels = ref([])
const priorities = ref([])
const selectedPriorities = ref([])
const selectedAssignees = ref([])
const selectedLabels = ref([])
const taskAddActiveForm = ref('')

const fetchStates = async (params = {}) => {
  try {
    loading.value = true
    const { data } = await stateTaskListAPI(project.value.id, params)

    states.value = data
  } catch (error) {
    message.warning(error.data.detail)
  } finally {
    loading.value = false
  }
}

const fetchMembers = async () => {
  try {
    const { data } = await projectMembersAPI(project.value.id)
    members.value = data
  } catch (error) {
    message.warning(error.data.detail)
  }
}

const fetchLabels = async () => {
  try {
    const { data } = await labelListAPI(project.value.id)
    labels.value = data
  } catch (error) {
    message.warning(error.data.detail)
  }
}

const fetchPriorities = async () => {
  try {
    const { data } = await priorityListAPI(project.value.id)
    priorities.value = data
  } catch (error) {
    message.warning(error.data.detail)
  }
}

onMounted(() => {
  fetchMembers()
  fetchPriorities()
  fetchLabels()
  fetchStates()
})

watch([selectedPriorities, selectedAssignees, selectedLabels], async () => {
  fetchStates()
})

function reloadTasksWithNewFilters(newFilters) {
  const params = {}
  if (newFilters.selectedPriorities.length > 0) {
    params['priorities'] = newFilters.selectedPriorities
  }

  if (newFilters.selectedAssignees.length > 0) {
    params['assignees'] = newFilters.selectedAssignees
  }

  if (newFilters.selectedLabels.length > 0) {
    params['labels'] = newFilters.selectedLabels
  }

  fetchStates(params)
}

function addNewTask(stateId, newTask) {
  const selectedState = states.value.find((s) => s.id === stateId)
  selectedState.tasks.push({
    ...newTask,
    assignees: [],
  })
}

function activateTaskAddForm(stateId) {
  taskAddActiveForm.value = stateId
}

const dragLog = async (state, event) => {
  const updatedData = {}

  // If the task is dragged within same state
  if (event.moved) {
    let newOrder = 0
    const task = event.moved.element

    if (event.moved.newIndex === 0) {
      // If the task dragged to top
      const nextTask = state.tasks[event.moved.newIndex + 1]
      newOrder = parseFloat(nextTask.order / 2)
      updatedData['order'] = newOrder
    } else if (event.moved.newIndex === state.tasks.length - 1) {
      // If the task dragged to bottom
      const previousTask = state.tasks[event.moved.newIndex - 1]
      newOrder = parseFloat(previousTask.order + 10000)
      updatedData['order'] = newOrder
    } else {
      // If the task dragged to any place in between
      const previousTask = state.tasks[event.moved.newIndex - 1]
      const nextTask = state.tasks[event.moved.newIndex + 1]
      newOrder =
        (parseFloat(previousTask.order) + parseFloat(nextTask.order)) / 2
      updatedData['order'] = newOrder
    }

    try {
      await taskUpdateAPI(project.value.id, task.id, updatedData)
      task.order = newOrder
    } catch (error) {
      message.error('Failed to update task order!')
    }
  }

  // If the task is dragged across state
  if (event.added) {
    updatedData['stateId'] = state.id

    const task = event.added.element
    let newOrder = 0

    if (event.added.newIndex === 0) {
      // If the task dragged to top
      const nextTask = state.tasks[event.added.newIndex + 1]
      newOrder = nextTask ? parseFloat(nextTask.order / 2) : 50000
      updatedData['order'] = newOrder
    } else if (event.added.newIndex === state.tasks.length - 1) {
      // If the task dragged to bottom
      const previousTask = state.tasks[event.added.newIndex - 1]
      newOrder = parseFloat(previousTask.order + 10000)
      updatedData['order'] = newOrder
    } else {
      // If the task dragged to any place in between
      const previousTask = state.tasks[event.added.newIndex - 1]
      const nextTask = state.tasks[event.added.newIndex + 1]
      newOrder =
        (parseFloat(previousTask.order) + parseFloat(nextTask.order)) / 2
      updatedData['order'] = newOrder
    }

    try {
      await taskUpdateAPI(project.value.id, task.id, updatedData)
      task.order = newOrder
    } catch (error) {
      message.error('Failed to update task order!')
    }
  }
}

const handleTaskDeactivate = () => {
  console.log('Outttt')
}
</script>

<template>
  <dashboard-layout page="projects" :themeColor="project.themeColor">
    <div class="tk-main-content">
      <a-flex justify="space-between" style="margin-bottom: 15px">
        <div>
          <a-typography-title :level="4">{{ project.name }}</a-typography-title>
        </div>
        <div>
          <a-space wrap>
            <a :href="`/${project.slug}/settings/general/`">
              <a-button>Settings</a-button>
            </a>
            <task-filters
              :members="members"
              :priorities="priorities"
              :labels="labels"
              @filterChange="reloadTasksWithNewFilters"
            />
            <a-button type="primary">+ Add Task</a-button>
          </a-space>
        </div>
      </a-flex>

      <hr />

      <a-flex
        justify="center"
        align="center"
        style="height: 90vh"
        v-if="loading"
      >
        <loading-spinner />
      </a-flex>
      <a-flex gap="middle" align="start" class="overflow-y-hidden" v-else>
        <div v-for="state in states" :key="state.id" style="min-width: 320px">
          <div>
            <a-typography-title :level="5">{{ state.name }}</a-typography-title>
            <draggable
              :list="state.tasks"
              group="states"
              item-key="id"
              @change="(event) => dragLog(state, event)"
            >
              <template #item="{ element: task }">
                <div class="my-1">
                  <task-card
                    :task="task"
                    :project="project"
                    :members="members"
                    :priorities="priorities"
                  ></task-card>
                </div>
              </template>

              <template #footer>
                <task-add-form
                  :projectId="project.id"
                  :stateId="state.id"
                  @close="() => (taskAddActiveForm = nil)"
                  @newTaskAdded="addNewTask"
                  v-if="taskAddActiveForm === state.id"
                ></task-add-form>
                <p
                  v-else
                  @click="() => activateTaskAddForm(state.id)"
                  class="text-blue-500 mt-3 ml-1"
                >
                  + Add Task
                </p>
              </template>
            </draggable>
          </div>
        </div>
      </a-flex>
    </div>
  </dashboard-layout>
</template>

<style scoped>
#tk-drag {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.add-task-popover {
  margin: 5px;
  padding: 5px;
}
</style>
