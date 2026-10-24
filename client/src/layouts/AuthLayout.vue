<!-- client/src/layouts/AuthLayout.vue -->
<template>
  <div class="auth-layout min-vh-100 d-flex flex-column">
    <!-- Header с логотипом -->
    <header class="auth-header py-4 text-center">
      <div class="container">
        <router-link to="/" class="text-decoration-none">
          <div class="d-inline-flex align-items-center">
            <i class="bi bi-shield-check text-civic fs-1 me-2"></i>
            <h1 class="h3 mb-0 text-dark fw-bold">Город под контролем</h1>
          </div>
        </router-link>
        <p class="text-muted small mt-2 mb-0">Муниципальный сервис обращений граждан</p>
      </div>
    </header>

    <!-- Main content -->
    <main class="auth-main flex-grow-1 d-flex align-items-center justify-content-center py-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-12 col-sm-10 col-md-8 col-lg-6 col-xl-5">
            <div class="auth-card card shadow-sm border-0">
              <div class="card-body p-4 p-md-5">
                <!-- ИСПРАВЛЕНО: router-view вместо slot -->
                <router-view />
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="auth-footer py-4 text-center text-muted small">
      <div class="container">
        <p class="mb-2">
          <router-link to="/" class="text-muted text-decoration-none me-3">О сервисе</router-link>
          <router-link to="/privacy" class="text-muted text-decoration-none me-3">Конфиденциальность</router-link>
          <router-link to="/terms" class="text-muted text-decoration-none">Условия</router-link>
        </p>
        <p class="mb-0">© 2024 Город под контролем. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout'
}
</script>

<style scoped>
.auth-layout {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.auth-header {
  background-color: white;
  border-bottom: 1px solid #e9ecef;
}

.auth-card {
  background-color: white;
  border-radius: 12px;
}

.auth-footer {
  background-color: white;
  border-top: 1px solid #e9ecef;
}

.auth-footer a:hover {
  color: var(--civic-primary, #00A896) !important;
}

@media (max-width: 768px) {
  .auth-header h1 {
    font-size: 1.5rem;
  }

  .auth-card .card-body {
    padding: 1.5rem !important;
  }
}
</style>