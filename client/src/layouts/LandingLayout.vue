<!-- client/src/layouts/LandingLayout.vue -->
<template>
  <div class="landing-layout">
    <!-- Верхняя панель -->
    <header class="topbar">
      <div class="topbar-brand">
        <button
            class="icon-button sidebar-toggle d-lg-none"
            type="button"
            aria-label="Открыть меню"
            :aria-expanded="isSidebarOpen"
            @click="isSidebarOpen = !isSidebarOpen"
        >
          <IconFa name="bars" size="1.2rem" />
        </button>

        <router-link to="/" class="brand-link">
          <span class="brand-mark">
            <IconFa name="shield-halved" size="1.35rem" />
          </span>
          <span class="brand-copy">
            <strong>Город под контролем</strong>
            <small>Муниципальный сервис</small>
          </span>
        </router-link>
      </div>

      <div class="topbar-actions">
        <router-link to="/map" class="topbar-map-link d-none d-sm-inline-flex">
          <IconFa name="map" class="me-2" />
          Карта города
        </router-link>

        <router-link
            to="/notifications"
            class="icon-button notification-button"
            aria-label="Уведомления"
            title="Уведомления"
        >
          <IconFa name="bell" size="1.15rem" />
        </router-link>

        <router-link to="/profile" class="profile-link">
          <span class="profile-avatar">
            <IconFa name="user" size="1.1rem" />
          </span>
          <span class="profile-label d-none d-md-inline">Мой профиль</span>
        </router-link>
      </div>
    </header>

    <div
        v-if="isSidebarOpen"
        class="sidebar-backdrop d-lg-none"
        @click="isSidebarOpen = false"
    ></div>

    <div class="app-shell">
      <!-- Боковая навигация -->
      <aside class="sidebar" :class="{ 'sidebar-open': isSidebarOpen }">
        <div class="sidebar-section-label">РАБОТА С ГОРОДОМ</div>

        <nav class="sidebar-nav" aria-label="Основная навигация">
          <router-link
              to="/"
              class="sidebar-link"
              exact-active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="house" />
            <span>Главная</span>
          </router-link>

          <router-link
              to="/map"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="map" />
            <span>Карта проблем</span>
          </router-link>

          <router-link
              to="/create"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="circle-plus" />
            <span>Сообщить о проблеме</span>
          </router-link>

          <router-link
              to="/problems"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="list-check" />
            <span>Мои обращения</span>
          </router-link>

          <router-link
              to="/initiatives/create"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="lightbulb" />
            <span>Инициативы</span>
          </router-link>

          <router-link
              to="/events/create"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="calendar" />
            <span>Мероприятия</span>
          </router-link>
        </nav>

        <div class="sidebar-section-label sidebar-section-label--secondary">
          АККАУНТ
        </div>

        <nav class="sidebar-nav" aria-label="Навигация по аккаунту">
          <router-link
              to="/notifications"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="bell" />
            <span>Уведомления</span>
          </router-link>

          <router-link
              to="/profile"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="user" />
            <span>Профиль</span>
          </router-link>

          <router-link
              to="/settings"
              class="sidebar-link"
              active-class="active"
              @click="isSidebarOpen = false"
          >
            <IconFa name="gear" />
            <span>Настройки</span>
          </router-link>
        </nav>

        <div class="sidebar-help">
          <span class="help-icon">
            <IconFa name="circle-question" />
          </span>
          <strong>Нужна помощь?</strong>
          <p>Мы поможем разобраться с сервисом.</p>
          <router-link to="/contacts" @click="isSidebarOpen = false">
            Связаться с нами <IconFa name="arrow-right" class="ms-1" />
          </router-link>
        </div>
      </aside>

      <!-- Контент растёт, футер прижимается вниз при коротких страницах -->
      <div class="content-column">
        <main class="landing-main" id="main-content">
          <router-view />
        </main>

        <footer class="app-footer">
          <div class="footer-inner">
            <div class="footer-brand">
              <span class="footer-mark">
                <IconFa name="shield-halved" />
              </span>
              <span>© {{ currentYear }} Город под контролем</span>
            </div>

            <nav class="footer-links" aria-label="Информация и обратная связь">
              <router-link to="/about">О сервисе</router-link>
              <router-link to="/contacts">Обратная связь</router-link>
              <router-link to="/privacy">Политика конфиденциальности</router-link>
              <router-link to="/terms">Условия использования</router-link>
            </nav>
          </div>
          <div class="footer-privacy-note">
            Персональные данные обрабатываются в соответствии с
            <router-link to="/privacy">Политикой конфиденциальности</router-link>.
            Используйте форму обратной связи, если у вас есть вопросы о работе сервиса или обработке данных.
          </div>
        </footer>
      </div>
    </div>

    <!-- Нижняя навигация для мобильных устройств (Font Awesome 5) -->
    <nav class="mobile-bottom-nav d-lg-none" aria-label="Мобильная навигация">
      <router-link to="/" class="mobile-nav-item" exact-active-class="active">
        <i class="fa-solid fa-home"></i>
        <span>Главная</span>
      </router-link>

      <router-link to="/map" class="mobile-nav-item" active-class="active">
        <i class="fas fa-map"></i>
        <span>Карта</span>
      </router-link>

      <router-link to="/create" class="mobile-nav-item mobile-create-item" active-class="active">
    <span class="mobile-create-button">
      <i class="fas fa-plus"></i>
    </span>
        <span>Создать</span>
      </router-link>

      <router-link to="/problems" class="mobile-nav-item" active-class="active">
        <i class="fas fa-clipboard-list"></i>
        <span>Обращения</span>
      </router-link>

      <router-link to="/profile" class="mobile-nav-item" active-class="active">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'LandingLayout',
  components: { IconFa },
  data() {
    return {
      isSidebarOpen: false
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  },
  watch: {
    '$route.path'() {
      this.isSidebarOpen = false
    }
  }
}
</script>

<style scoped>
.landing-layout {
  --layout-ink: #172f40;
  --layout-muted: #70808c;
  --layout-line: #e8edf0;
  --layout-accent: var(--civic-primary, #00a896);
  --sidebar-width: 264px;

  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  color: var(--layout-ink);
  background: #f6f8fa;
}

/* Верхняя панель */
.topbar {
  position: sticky;
  top: 0;
  z-index: 1030;
  display: flex;
  min-height: 76px;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem clamp(1rem, 3vw, 2rem);
  border-bottom: 1px solid var(--layout-line);
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(18px);
}

.topbar-brand,
.topbar-actions,
.brand-link,
.profile-link {
  display: flex;
  align-items: center;
}

.topbar-brand {
  min-width: 0;
  gap: 0.75rem;
}

.brand-link {
  min-width: 0;
  gap: 0.75rem;
  color: inherit;
  text-decoration: none;
}

.brand-mark,
.footer-mark {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  color: white;
  background: linear-gradient(135deg, #00a896, #087e8b);
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.2);
}

.brand-copy {
  display: flex;
  min-width: 0;
  flex-direction: column;
  line-height: 1.3;
}

.brand-copy strong {
  overflow: hidden;
  font-size: 0.98rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.brand-copy small {
  margin-top: 0.2rem;
  color: var(--layout-muted);
  font-size: 0.75rem;
}

.topbar-actions {
  gap: 0.75rem;
}

.icon-button {
  display: inline-flex;
  width: 42px;
  height: 42px;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--layout-line);
  border-radius: 13px;
  background: white;
  color: #526571;
  text-decoration: none;
  transition: background 180ms ease, color 180ms ease, border-color 180ms ease;
}

.icon-button:hover,
.icon-button:focus-visible {
  border-color: rgba(0, 168, 150, 0.35);
  background: rgba(0, 168, 150, 0.07);
  color: var(--layout-accent);
}

.topbar-map-link {
  align-items: center;
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  color: #405562;
  font-size: 0.88rem;
  font-weight: 650;
  text-decoration: none;
}

.topbar-map-link:hover {
  background: #f1f7f7;
  color: var(--layout-accent);
}

.profile-link {
  gap: 0.55rem;
  color: var(--layout-ink);
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
}

.profile-avatar {
  display: inline-flex;
  width: 42px;
  height: 42px;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 168, 150, 0.15);
  border-radius: 50%;
  background: #e8f7f4;
  color: #008f80;
}

.sidebar-toggle {
  display: inline-flex;
}

/* Sidebar + колонка контента */
.app-shell {
  display: flex;
  flex: 1 0 auto;
  align-items: stretch;
  min-height: 0;
}

.sidebar {
  position: sticky;
  top: 76px;
  display: flex;
  width: var(--sidebar-width);
  height: calc(100vh - 76px);
  height: calc(100dvh - 76px);
  flex: 0 0 var(--sidebar-width);
  flex-direction: column;
  overflow-y: auto;
  padding: 1.6rem 1rem 1.25rem;
  border-right: 1px solid var(--layout-line);
  background: #fff;
}

.sidebar-section-label {
  padding: 0 0.8rem;
  color: #95a2ab;
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.sidebar-section-label--secondary {
  margin-top: 1.8rem;
}

.sidebar-nav {
  display: grid;
  gap: 0.3rem;
  margin-top: 0.8rem;
}

.sidebar-link {
  display: flex;
  min-height: 46px;
  align-items: center;
  gap: 0.8rem;
  padding: 0.7rem 0.8rem;
  border: 1px solid transparent;
  border-radius: 12px;
  color: #586b77;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 180ms ease, background 180ms ease, border-color 180ms ease;
}

.sidebar-link :deep(svg) {
  width: 18px;
  flex: 0 0 18px;
  color: #84939c;
}

.sidebar-link:hover {
  background: #f5f9f9;
  color: var(--layout-accent);
}

.sidebar-link.active {
  border-color: rgba(0, 168, 150, 0.12);
  background: linear-gradient(100deg, rgba(0, 168, 150, 0.12), rgba(0, 168, 150, 0.045));
  color: #007f73;
  font-weight: 750;
}

.sidebar-link.active :deep(svg) {
  color: #008f80;
}

.sidebar-help {
  margin-top: auto;
  padding: 1rem;
  border: 1px solid #e3efed;
  border-radius: 16px;
  background: linear-gradient(145deg, #f2fbf9, #f8fbfc);
}

.help-icon {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  border-radius: 11px;
  background: #dff5f0;
  color: #008f80;
}

.sidebar-help strong {
  display: block;
  font-size: 0.88rem;
}

.sidebar-help p {
  margin: 0.4rem 0 0.7rem;
  color: var(--layout-muted);
  font-size: 0.78rem;
  line-height: 1.55;
}

.sidebar-help a {
  color: #008f80;
  font-size: 0.8rem;
  font-weight: 750;
  text-decoration: none;
}

.content-column {
  display: flex;
  min-width: 0;
  flex: 1 1 auto;
  flex-direction: column;
}

.landing-main {
  width: 100%;
  flex: 1 0 auto;
  min-width: 0;
}

/* Футер */
.app-footer {
  margin-top: auto;
  border-top: 1px solid var(--layout-line);
  background: #fff;
}

.footer-inner {
  display: flex;
  min-height: 76px;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.1rem clamp(1rem, 3vw, 2rem);
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: #7b8992;
  font-size: 0.78rem;
}

.footer-mark {
  width: 28px;
  height: 28px;
  border-radius: 9px;
  font-size: 0.8rem;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem 1.15rem;
}

.footer-links a {
  color: #6d7d87;
  font-size: 0.78rem;
  text-decoration: none;
  transition: color 180ms ease;
}

.footer-links a:hover {
  color: var(--layout-accent);
}

.footer-privacy-note {
  padding: 0 2rem 1rem;
  color: #84919a;
  font-size: 0.74rem;
  line-height: 1.65;
  text-align: center;
}

.footer-privacy-note a {
  color: #008f80;
  font-weight: 650;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* === Нижняя мобильная панель (ИСПРАВЛЕНО: нативные теги <i>) === */
.mobile-bottom-nav {
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1040;
  display: flex;
  justify-content: center;
  padding: 0.45rem 0.3rem calc(0.45rem + env(safe-area-inset-bottom, 0px));
  border-top: 1px solid rgba(226, 233, 237, 0.95);
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 -8px 28px rgba(23, 47, 64, 0.08);
  backdrop-filter: blur(18px);
}

.mobile-nav-item {
  display: flex;
  width: 20%;
  min-width: 0;
  max-width: 20%;
  flex: 0 0 20%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.25rem 0.05rem;
  color: #87949d;
  font-size: 0.7rem;
  font-weight: 650;
  text-align: center;
  text-decoration: none;
  -webkit-tap-highlight-color: transparent;
}

/* Явное увеличение иконок через нативный тег <i> */
.mobile-nav-item > i {
  display: block;
  width: 1.75rem;
  height: 1.75rem;
  font-size: 1.1rem !important;
  line-height: 1.75rem;
  text-align: center;
}

.mobile-nav-item > span:last-child {
  display: block;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mobile-nav-item.active {
  color: #008f80;
}

.mobile-create-item {
  margin-top: -1.2rem;
  color: #008f80;
}

/* Увеличенная и идеально круглая центральная кнопка */
.mobile-create-button {
  display: inline-flex;
  width: 56px;
  height: 56px;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.05rem;
  border: 4px solid #f6f8fa;
  border-radius: 50%;
  background: linear-gradient(145deg, #00b5a1, #087e8b);
  box-shadow: 0 6px 16px rgba(0, 168, 150, 0.3);
  color: white;
  transition: transform 180ms ease;
}

.mobile-create-button > i {
  font-size: 1.6rem !important;
  line-height: 1;
}

.mobile-create-item:active .mobile-create-button {
  transform: scale(0.94);
}

.sidebar-backdrop {
  position: fixed;
  inset: 76px 0 0;
  z-index: 1050;
  background: rgba(15, 31, 42, 0.42);
  backdrop-filter: blur(2px);
}

@media (max-width: 991.98px) {
  .sidebar {
    position: fixed;
    top: 76px;
    bottom: 0;
    left: 0;
    z-index: 1060;
    width: min(290px, 86vw);
    height: auto;
    transform: translateX(-105%);
    box-shadow: none;
    transition: transform 220ms ease, box-shadow 220ms ease;
  }

  .sidebar.sidebar-open {
    transform: translateX(0);
    box-shadow: 18px 0 45px rgba(23, 47, 64, 0.14);
  }

  .app-shell {
    display: block;
  }

  .content-column {
    min-height: calc(100vh - 76px);
    min-height: calc(100dvh - 76px);
  }

  .landing-main {
    padding-bottom: 1rem;
  }

  .footer-inner {
    justify-content: center;
    text-align: center;
  }

  .footer-brand,
  .footer-links {
    justify-content: center;
  }

  .landing-layout {
    padding-bottom: calc(76px + env(safe-area-inset-bottom, 0px));
  }
}

@media (max-width: 575.98px) {
  .topbar {
    min-height: 68px;
    padding: 0.65rem 0.8rem;
  }

  .brand-mark {
    width: 39px;
    height: 39px;
    border-radius: 12px;
  }

  .brand-copy strong {
    max-width: 47vw;
    font-size: 0.86rem;
  }

  .brand-copy small {
    font-size: 0.68rem;
  }

  .topbar-actions {
    gap: 0.45rem;
  }

  .icon-button,
  .profile-avatar {
    width: 38px;
    height: 38px;
    border-radius: 12px;
  }

  .profile-avatar {
    border-radius: 50%;
  }

  .sidebar {
    top: 68px;
  }

  .sidebar-backdrop {
    top: 68px;
  }

  .content-column {
    min-height: calc(100vh - 68px);
    min-height: calc(100dvh - 68px);
  }

  .footer-inner {
    padding: 1rem 0.8rem;
  }

  .footer-privacy-note {
    padding: 0 1rem 1rem;
    font-size: 0.7rem;
  }

  .footer-links {
    gap: 0.65rem 0.9rem;
  }

  .footer-links a,
  .footer-brand {
    font-size: 0.72rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
</style>