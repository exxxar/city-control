<!-- client/src/layouts/PublicLayout.vue -->
<template>
  <div class="public-layout min-vh-100 d-flex flex-column">
    <!-- Header -->
    <header class="public-header bg-white border-bottom shadow-sm">
      <div class="container">
        <div class="d-flex align-items-center justify-content-between py-3">
          <!-- Logo -->
          <router-link to="/" class="text-decoration-none d-flex align-items-center">
            <i class="bi bi-shield-check text-civic fs-3 me-2"></i>
            <span class="fw-bold text-dark">Город под контролем</span>
          </router-link>

          <!-- Navigation -->
          <nav class="d-none d-md-flex align-items-center gap-3">
            <router-link to="/map" class="text-decoration-none text-secondary">
              <i class="bi bi-map me-1"></i> Карта
            </router-link>
            <router-link to="/about" class="text-decoration-none text-secondary">
              О проекте
            </router-link>
          </nav>

          <!-- Auth buttons -->
          <div class="d-flex align-items-center gap-2">
            <router-link to="/login" class="btn btn-outline-civic btn-sm">
              Войти
            </router-link>
            <router-link to="/register" class="btn btn-civic btn-sm d-none d-sm-inline-block">
              Регистрация
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="public-main flex-grow-1">
      <!-- ИСПРАВЛЕНО: router-view вместо slot -->
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="public-footer bg-white border-top py-4">
      <div class="container">
        <div class="row">
          <div class="col-12 col-md-6 mb-3 mb-md-0">
            <h6 class="fw-bold mb-2">Город под контролем</h6>
            <p class="text-muted small mb-0">
              Муниципальный сервис обработки обращений граждан, инициатив и заявок на мероприятия.
            </p>
          </div>
          <div class="col-6 col-md-3">
            <h6 class="fw-bold mb-2">Сервис</h6>
            <ul class="list-unstyled small mb-0">
              <li><router-link to="/map" class="text-muted text-decoration-none">Карта проблем</router-link></li>
              <li><router-link to="/about" class="text-muted text-decoration-none">О проекте</router-link></li>
              <li><router-link to="/contacts" class="text-muted text-decoration-none">Контакты</router-link></li>
            </ul>
          </div>
          <div class="col-6 col-md-3">
            <h6 class="fw-bold mb-2">Правовая информация</h6>
            <ul class="list-unstyled small mb-0">
              <li><router-link to="/privacy" class="text-muted text-decoration-none">Конфиденциальность</router-link></li>
              <li><router-link to="/terms" class="text-muted text-decoration-none">Условия использования</router-link></li>
            </ul>
          </div>
        </div>
        <hr class="my-3">
        <div class="text-center text-muted small">
          © 2024 Город под контролем. Все права защищены.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'PublicLayout'
}
</script>

<style scoped>
.public-layout {
  background-color: #f8f9fa;
}

.public-header {
  position: sticky;
  top: 0;
  z-index: 1000;
}

.public-main {
  min-height: calc(100vh - 200px);
}

.public-footer a:hover {
  color: var(--civic-primary, #00A896) !important;
}

.btn-outline-civic {
  color: var(--civic-primary, #00A896);
  border-color: var(--civic-primary, #00A896);
}

.btn-outline-civic:hover {
  background-color: var(--civic-primary, #00A896);
  color: white;
}

@media (max-width: 768px) {
  .public-header .btn-sm {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
  }
}
</style>