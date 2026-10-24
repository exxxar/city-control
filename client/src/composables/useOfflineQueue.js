// client/src/composables/useOfflineQueue.js
import { computed } from 'vue'
import { useOfflineQueueStore } from '@/stores/offlineQueue.store'

export function useOfflineQueue() {
  const queueStore = useOfflineQueueStore()

  const pendingCount = computed(() => queueStore.pendingItems.length)
  const failedCount = computed(() => queueStore.failedItems.length)
  const isOnline = computed(() => queueStore.isOnline)
  const isSyncing = computed(() => queueStore.isSyncing)

  function addToQueue(actionType, data) {
    queueStore.addToQueue({
      type: actionType,
      data
    })
  }

  function addProblemToQueue(problemData) {
    addToQueue('create_problem', problemData)
  }

  function addMessageToQueue(problemId, content) {
    addToQueue('send_message', { problemId, content })
  }

  async function syncNow() {
    await queueStore.processQueue()
  }

  function retryFailed(itemId) {
    queueStore.retryItem(itemId)
  }

  function clearQueue() {
    queueStore.clearQueue()
  }

  return {
    pendingCount,
    failedCount,
    isOnline,
    isSyncing,
    addToQueue,
    addProblemToQueue,
    addMessageToQueue,
    syncNow,
    retryFailed,
    clearQueue
  }
}