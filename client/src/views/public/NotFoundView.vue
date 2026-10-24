<!-- client/src/views/public/NotFoundView.vue -->
<template>
  <PublicLayout>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-6 text-center">
          <div class="mb-4">
            <i class="bi bi-exclamation-triangle text-warning" style="font-size: 5rem;"></i>
          </div>
          <h1 class="display-4 fw-bold text-dark mb-3">404</h1>
          <h2 class="h4 text-muted mb-4">Страница не найдена</h2>
          <p class="text-secondary mb-4">
            К сожалению, страница, которую вы ищете, не существует или была перемещена.
          </p>
          <div class="d-flex gap-3 justify-content-center">
            <router-link to="/" class="btn btn-civic">
              <i class="bi bi-house-door me-2"></i>
              На главную
            </router-link>
            <button @click="$router.back()" class="btn btn-outline-secondary">
              <i class="bi bi-arrow-left me-2"></i>
              Назад
            </button>
          </div>
        </div>
      </div>
    </div>
  </PublicLayout>
</template>

<script>
import PublicLayout from '@/layouts/PublicLayout.vue'

export default {
  name: 'NotFoundView',
  components: { PublicLayout }
}
</script>