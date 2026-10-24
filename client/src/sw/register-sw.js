// client/src/sw/register-sw.js

/**
 * Регистрация Service Worker для PWA
 * Интеграция с vite-plugin-pwa
 */

export async function registerServiceWorker() {
  // Проверяем поддержку Service Worker
  if (!('serviceWorker' in navigator)) {
    console.warn('[SW] Service Worker не поддерживается браузером')
    return null
  }

  try {
    // Регистрация Service Worker
    // vite-plugin-pwa автоматически генерирует sw.js в папке dist
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/'
    })

    console.log('[SW] Service Worker успешно зарегистрирован:', registration.scope)

    // Обработка обновлений
    handleUpdates(registration)

    // Обработка активации
    handleActivation(registration)

    return registration
  } catch (error) {
    console.error('[SW] Ошибка регистрации Service Worker:', error)
    return null
  }
}

/**
 * Обработка обновлений Service Worker
 */
function handleUpdates(registration) {
  // Проверяем наличие новой версии SW
  registration.addEventListener('updatefound', () => {
    const newWorker = registration.installing

    console.log('[SW] Найдена новая версия Service Worker')

    newWorker.addEventListener('statechange', () => {
      if (newWorker.state === 'installed') {
        // Новая версия установлена и готова к активации
        if (navigator.serviceWorker.controller) {
          // Есть активный SW, значит это обновление
          console.log('[SW] Новая версия готова. Показать уведомление об обновлении?')

          // Здесь можно показать UI-уведомление пользователю
          // Например: "Доступна новая версия приложения. Обновить?"
          showUpdateNotification()
        } else {
          // Первая установка, просто активируем
          console.log('[SW] Контент кэширован для оффлайн-использования')
        }
      }
    })
  })
}

/**
 * Обработка активации Service Worker
 */
function handleActivation(registration) {
  // Слушаем событие контроллера (когда SW начинает управлять страницей)
  let currentWorker = registration.installing || registration.waiting || registration.active

  if (currentWorker) {
    currentWorker.addEventListener('statechange', (event) => {
      if (event.target.state === 'activated') {
        console.log('[SW] Service Worker активирован и контролирует страницу')
      }
    })
  }
}

/**
 * Показать уведомление об обновлении
 * В реальном приложении здесь будет вызов UI-компонента
 */
function showUpdateNotification() {
  // Временное решение через confirm
  // В продакшене использовать кастомный UI-компонент (UiModal или UiToast)
  const shouldUpdate = window.confirm(
    'Доступна новая версия приложения. Обновить сейчас?'
  )

  if (shouldUpdate) {
    skipWaiting()
  }
}

/**
 * Принудительная активация нового Service Worker
 */
export async function skipWaiting() {
  const registration = await navigator.serviceWorker.ready

  if (registration.waiting) {
    registration.waiting.postMessage({ type: 'SKIP_WAITING' })
    window.location.reload()
  }
}

/**
 * Отмена регистрации Service Worker (для разработки)
 */
export async function unregisterServiceWorker() {
  if (!('serviceWorker' in navigator)) {
    console.warn('[SW] Service Worker не поддерживается')
    return false
  }

  try {
    const registration = await navigator.serviceWorker.ready
    const success = await registration.unregister()

    if (success) {
      console.log('[SW] Service Worker успешно удалён')
      window.location.reload()
    }

    return success
  } catch (error) {
    console.error('[SW] Ошибка удаления Service Worker:', error)
    return false
  }
}

/**
 * Проверка статуса Service Worker
 */
export async function checkServiceWorkerStatus() {
  if (!('serviceWorker' in navigator)) {
    return { supported: false, registered: false }
  }

  try {
    const registration = await navigator.serviceWorker.getRegistration()

    return {
      supported: true,
      registered: !!registration,
      scope: registration?.scope || null,
      active: !!registration?.active,
      waiting: !!registration?.waiting,
      installing: !!registration?.installing
    }
  } catch (error) {
    console.error('[SW] Ошибка проверки статуса:', error)
    return { supported: true, registered: false, error: error.message }
  }
}

/**
 * Отправка сообщения в Service Worker
 */
export async function sendMessageToSW(message) {
  if (!navigator.serviceWorker.controller) {
    console.warn('[SW] Нет активного Service Worker для отправки сообщения')
    return null
  }

  return new Promise((resolve) => {
    const messageChannel = new MessageChannel()

    messageChannel.port1.onmessage = (event) => {
      resolve(event.data)
    }

    navigator.serviceWorker.controller.postMessage(message, [messageChannel.port2])
  })
}

/**
 * Инициализация PWA при загрузке приложения
 */
export async function initPWA() {
  console.log('[PWA] Инициализация...')

  // Регистрируем Service Worker
  const registration = await registerServiceWorker()

  if (registration) {
    console.log('[PWA] Service Worker готов')

    // Проверяем, можно ли установить приложение
    checkInstallPrompt()
  }

  return registration
}

/**
 * Проверка возможности установки PWA
 */
let deferredPrompt = null

function checkInstallPrompt() {
  window.addEventListener('beforeinstallprompt', (e) => {
    console.log('[PWA] Событие beforeinstallprompt получено')
    e.preventDefault()
    deferredPrompt = e

    // Здесь можно показать кнопку "Установить приложение"
    // showInstallButton()
  })

  window.addEventListener('appinstalled', () => {
    console.log('[PWA] Приложение успешно установлено')
    deferredPrompt = null
    // hideInstallButton()
  })
}

/**
 * Показать промпт установки PWA
 */
export async function showInstallPrompt() {
  if (!deferredPrompt) {
    console.warn('[PWA] Промпт установки недоступен')
    return false
  }

  try {
    deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice

    console.log(`[PWA] Пользователь ${outcome === 'accepted' ? 'принял' : 'отклонил'} установку`)
    deferredPrompt = null

    return outcome === 'accepted'
  } catch (error) {
    console.error('[PWA] Ошибка показа промпта установки:', error)
    return false
  }
}

/**
 * Проверка, запущено ли приложение как PWA
 */
export function isStandalone() {
  return (
    window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true
  )
}