<!-- client/src/views/notifications/NotificationsView.vue -->
<template>
  <AppPageContainer title="Уведомления">
    <template #actions>
      <UiButton
        v-if="notifications.length > 0"
        variant="link"
        size="sm"
        @click="markAllAsRead"
      >
        Прочитать все
      </UiButton>
    </template>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-civic"></div>
    </div>

    <div v-else-if="notifications.length === 0" class="py-5">
      <UiEmptyState
        icon="bell-slash"
        title="Нет уведомлений"
        description="У вас пока нет уведомлений"
      />
    </div>

    <div v-else class="notifications-list">
      <NotificationItem
        v-for="notif in notifications"
        :key="notif.id"
        :notification="notif"
        @click="openNotification"
      />
    </div>
  </AppPageContainer>
</template>

<script>
import AppPageContainer from '@/components/layout/AppPageContainer.vue'
import UiButton from '@/components/ui/UiButton.vue'
import UiEmptyState from '@/components/ui/UiEmptyState.vue'
import NotificationItem from '@/components/notifications/NotificationItem.vue'
import { useNotifications } from '@/composables/useNotifications'

export default {
  name: 'NotificationsView',
  components: { AppPageContainer, UiButton, UiEmptyState, NotificationItem },
  computed: {
    notificationsStore() {
      const { notifications, isLoading } = useNotifications()
      return { notifications: notifications.value, isLoading: isLoading.value }
    },
    notifications() {
      return this.notificationsStore.notifications
    },
    isLoading() {
      return this.notificationsStore.isLoading
    }
  },
  methods: {
    async markAllAsRead() {
      const { markAllAsRead } = useNotifications()
      await markAllAsRead()
    },

    openNotification(notif) {
      const { markAsRead } = useNotifications()
      markAsRead([notif.id])

      if (notif.linked_entity_type === 'problem' && notif.linked_entity_id) {
        this.$router.push({ name: 'ProblemDetails', params: { id: notif.linked_entity_id } })
      }
    }
  }
}
</script>