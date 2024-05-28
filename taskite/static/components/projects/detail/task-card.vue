<script setup>
import { ref, computed } from 'vue'
import { generateAvatar } from '@/utils/generators'

import TaskDetailModal from '@/components/projects/detail/task-detail-modal.vue'

const { task, project, members, priorities } = defineProps(['task', 'project', 'members', 'priorities'])
const emit = defineEmits(['updated'])

const showTaskDetailModal = ref(false)
function openTaskDetailModal() {
  showTaskDetailModal.value = true
}

const handleTaskUpdateFromModal = (payload) => {
  emit('updated', payload)

  Object.keys(payload).forEach((key) => {
    task[key] = payload[key]
  })
}

const getAvatar = (record) => {
  if (!record.avatar) {
    return generateAvatar(record.fullName)
  }

  return record.avatar
}

</script>

<template>
  <a-card id="task-card" size="small" @click="openTaskDetailModal">
    <a-flex justify="space-between">
      <div>
        <a-typography-text type="secondary" style="font-size: smaller">{{
          task.taskId
        }}</a-typography-text>
      </div>
      <a-tag :bordered="false" v-if="task.priority" class="flex flex-row items-center">
          <a-badge :color="task.priority.color" />
          <div class="text-xs">{{ task.priority.name }}</div>
      </a-tag>
    </a-flex>
    <div>{{ task.name }}</div>
    <a-flex justify="end">
      <a-avatar-group>
        <a-tooltip
          :title="assignee.displayName"
          placement="top"
          v-for="assignee in task.assignees"
          :key="assignee.id"
        >
          <a-avatar size="small" :src="getAvatar(assignee)"> </a-avatar>
        </a-tooltip>
      </a-avatar-group>
    </a-flex>
  </a-card>

  <a-modal
    v-model:open="showTaskDetailModal"
    width="1000px"
    :footer="null"
    :destroyOnClose="true"
  >
    <task-detail-modal
      :taskId="task.id"
      :projectId="project.id"
      :projectSlug="project.slug"
      :projectName="project.name"
      :members="members"
      :priorities="priorities"
      @updated="handleTaskUpdateFromModal"
    ></task-detail-modal>
  </a-modal>
</template>

<style scoped>
#task-card {
  width: 320px;
}
</style>
