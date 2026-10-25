import { ref } from 'vue'

const DRAFTS_KEY = 'city_under_control_drafts'

export function useOfflineQueue() {
  const getDrafts = () => {
    try {
      const data = localStorage.getItem(DRAFTS_KEY)
      return data ? JSON.parse(data) : []
    } catch (e) {
      console.error('Failed to parse drafts', e)
      return []
    }
  }

  const addProblemToQueue = (problemData) => {
    const drafts = getDrafts()

    // Убираем файлы из черновика, так как их нельзя сериализовать в JSON
    const { files, ...dataWithoutFiles } = problemData

    const newDraft = {
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
      ...dataWithoutFiles
    }

    // Добавляем в начало списка
    drafts.unshift(newDraft)

    // Храним не более 5 черновиков, чтобы не засорять память
    if (drafts.length > 5) drafts.pop()

    localStorage.setItem(DRAFTS_KEY, JSON.stringify(drafts))
  }

  const removeDraft = (id) => {
    const drafts = getDrafts().filter(d => d.id !== id)
    localStorage.setItem(DRAFTS_KEY, JSON.stringify(drafts))
  }

  return { getDrafts, addProblemToQueue, removeDraft }
}