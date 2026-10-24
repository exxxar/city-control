// client/src/services/storage.service.js

class StorageService {
  // === LocalStorage ===
  setLocal(key, value) {
    try {
      const serialized = JSON.stringify(value)
      localStorage.setItem(key, serialized)
    } catch (err) {
      console.error('[StorageService] LocalStorage set error:', err)
    }
  }

  getLocal(key, defaultValue = null) {
    try {
      const serialized = localStorage.getItem(key)
      return serialized ? JSON.parse(serialized) : defaultValue
    } catch (err) {
      console.error('[StorageService] LocalStorage get error:', err)
      return defaultValue
    }
  }

  removeLocal(key) {
    localStorage.removeItem(key)
  }

  clearLocal() {
    localStorage.clear()
  }

  // === SessionStorage ===
  setSession(key, value) {
    try {
      const serialized = JSON.stringify(value)
      sessionStorage.setItem(key, serialized)
    } catch (err) {
      console.error('[StorageService] SessionStorage set error:', err)
    }
  }

  getSession(key, defaultValue = null) {
    try {
      const serialized = sessionStorage.getItem(key)
      return serialized ? JSON.parse(serialized) : defaultValue
    } catch (err) {
      console.error('[StorageService] SessionStorage get error:', err)
      return defaultValue
    }
  }

  removeSession(key) {
    sessionStorage.removeItem(key)
  }

  // === IndexedDB (для больших данных, например, фото в offline) ===
  async openDB(dbName = 'CityUnderControlDB', version = 1) {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(dbName, version)

      request.onupgradeneeded = (event) => {
        const db = event.target.result
        if (!db.objectStoreNames.contains('offline_media')) {
          db.createObjectStore('offline_media', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('offline_queue')) {
          db.createObjectStore('offline_queue', { keyPath: 'id', autoIncrement: true })
        }
      }

      request.onsuccess = (event) => resolve(event.target.result)
      request.onerror = (event) => reject(event.target.error)
    })
  }

  async saveToIndexedDB(storeName, data) {
    const db = await this.openDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([storeName], 'readwrite')
      const store = transaction.objectStore(storeName)
      const request = store.put(data)
      request.onsuccess = () => resolve()
      request.onerror = (event) => reject(event.target.error)
    })
  }

  async getFromIndexedDB(storeName, key) {
    const db = await this.openDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([storeName], 'readonly')
      const store = transaction.objectStore(storeName)
      const request = store.get(key)
      request.onsuccess = (event) => resolve(event.target.result)
      request.onerror = (event) => reject(event.target.error)
    })
  }

  async getAllFromIndexedDB(storeName) {
    const db = await this.openDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([storeName], 'readonly')
      const store = transaction.objectStore(storeName)
      const request = store.getAll()
      request.onsuccess = (event) => resolve(event.target.result)
      request.onerror = (event) => reject(event.target.error)
    })
  }

  async deleteFromIndexedDB(storeName, key) {
    const db = await this.openDB()
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([storeName], 'readwrite')
      const store = transaction.objectStore(storeName)
      const request = store.delete(key)
      request.onsuccess = () => resolve()
      request.onerror = (event) => reject(event.target.error)
    })
  }
}

export const storageService = new StorageService()