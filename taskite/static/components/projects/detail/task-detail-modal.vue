<script setup>
import { ref, onMounted } from 'vue'
import { generateAvatar } from '@/utils/generators'
import { message } from 'ant-design-vue'

import LoadingSpinner from '@/components/common/loading-spinner.vue'
import BaseEditor from '@/components/common/base-editor.vue'

import {
  taskUpdateAPI,
  taskDetailAPI,
  attachmentListAPI,
  commentListAPI,
} from '@/api/tasks'

const props = defineProps([
  'taskId',
  'projectId',
  'projectSlug',
  'projectName',
  'members',
  'priorities',
])
const emit = defineEmits(['updated'])

const bordered = ref(false)
const name = ref(null)

const task = ref(null)
const fetchTaskDetail = async () => {
  try {
    const { data } = await taskDetailAPI(props.projectId, props.taskId)
    task.value = data

    description.value = data.description
    assigneeIds.value = data.assignees.map((assignee) => assignee.id)
  } catch (error) {
    message.error(error.data.detail)
  }
}

const attachments = ref([])
const fetchAttachments = async () => {
  try {
    const { data } = await attachmentListAPI(props.projectId, props.taskId)
    attachments.value = data
  } catch (error) {
    message.error(error.data.detail)
  }
}

const comments = ref([])
const fetchComments = async () => {
  try {
    const { data } = await commentListAPI(props.projectId, props.taskId)
    comments.value = data
  } catch (error) {
    message.error(error.data.detail)
  }
}

const updateTask = async (payload) => {
  try {
    const { data } = await taskUpdateAPI(
      props.projectId,
      task.value.id,
      payload,
      {}
    )
    return data
  } catch (error) {
    message.error(error.data.detail)
  }
}

const handleNameUpdate = async () => {
  if (name.value.innerText !== task.value.name) {
    updateTask({ name: name.value.innerText })
    task.value.name = name.value.innerText

    emit('updated', { name: name.value.innerText })
  }
}

const description = ref('')
const handleDescriptionUpdate = async () => {
  if (description.value !== task.value.description) {
    updateTask({ description: description.value })
    task.value.description = description.value
  }
}

const handlePriorityChange = (value) => {
  const priority = props.priorities.find((priority) => priority.id === value)

  updateTask({ priorityId: value })
  emit('updated', { priority })
}

const handleTaskTypeChange = (value) => {
  updateTask({ taskType: value })
  emit('updated', { taskType: value })
}

const assigneeIds = ref([])
const handleAssigneeChange = (values) => {
  updateTask({ assigneeIds: values })
  emit('updated', {
    assignees: props.members.filter((member) => values.includes(member.id)),
  })
}

const assigneeOptions = props.members.map((member) => {
  return {
    ...member,
    value: member.id,
    label: member.displayName,
    avatar: !!member.avatar ? member.avatar : generateAvatar(member.fullName),
  }
})

onMounted(async () => {
  fetchTaskDetail()
  fetchAttachments()
  fetchComments()
})
</script>

<template>
  <div v-if="!!task">
    <a-breadcrumb>
      <a-breadcrumb-item>
        <a :href="`/${props.projectSlug}/`">{{ props.projectName }}</a>
      </a-breadcrumb-item>
      <a-breadcrumb-item>
        <a :href="`/${props.projectSlug}/${task.taskId}/`">{{ task.taskId }}</a>
      </a-breadcrumb-item>
    </a-breadcrumb>

    <div contenteditable="true" ref="name" @blur="handleNameUpdate" class="text-lg my-1 py-2 focus:px-1">{{ task.name }}</div>

    <a-row :gutter="16">
      <a-col :span="16">
        <div>Description</div>
        <base-editor
          v-model="description"
          @blur="handleDescriptionUpdate"
        ></base-editor>
      </a-col>
      <a-col :span="8">
        <a-flex>
          <a-form
            layout="vertical"
            :wrapper-col="{
              span: 14,
            }"
            :label-col="{
              style: {
                width: '120px',
              },
            }"
          >
            <a-form-item label="Priority">
              <a-select
                v-if="task.priority"
                ref="select"
                v-model:value="task.priority.id"
                @change="handlePriorityChange"
              >
                <a-select-option
                  :value="priority.id"
                  v-for="priority in props.priorities"
                  :key="priority.id"
                  >{{ priority.name }}</a-select-option
                >
              </a-select>
              <a-select v-else ref="select" @change="handlePriorityChange">
                <a-select-option
                  :value="priority.id"
                  v-for="priority in props.priorities"
                  :key="priority.id"
                  >{{ priority.name }}</a-select-option
                >
              </a-select>
            </a-form-item>

            <a-form-item label="Task type">
              <a-select
                ref="select"
                v-model:value="task.taskType"
                @change="handleTaskTypeChange"
              >
                <a-select-option value="issue">Issue</a-select-option>
                <a-select-option value="task">Task</a-select-option>
                <a-select-option value="story">Story</a-select-option>
                <a-select-option value="bug">Bug</a-select-option>
                <a-select-option value="epic">Epic</a-select-option>
              </a-select>
            </a-form-item>

            <a-form-item label="Assignee">
              <a-select
                v-model:value="assigneeIds"
                mode="multiple"
                @change="handleAssigneeChange"
                style="width: 150px"
                :options="assigneeOptions"
              >
                <template #option="{ value: val, label, avatar }">
                  <a-avatar :src="avatar" size="small"></a-avatar>
                  <span style="margin-left: 7px">{{ label }}</span>
                </template>
                <template
                  #tagRender="{ value: val, label, closable, onClose, option }"
                >
                  <a-avatar-group :closable="closable" @close="onClose">
                    <a-avatar :src="option.avatar" size="small"></a-avatar>
                  </a-avatar-group>
                </template>
              </a-select>
            </a-form-item>
          </a-form>
        </a-flex>
      </a-col>
    </a-row>
  </div>
  <div v-else>
    <a-flex justify="center" align="center" style="height: 40vh">
      <loading-spinner />
    </a-flex>
  </div>
</template>
