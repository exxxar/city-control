<!-- client/src/views/public/AboutView.vue -->
<template>
  <PublicLayout>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-md-8 text-center">
          <div class="mb-4">
            <IconFa name="shield-check" size="4rem" color="var(--civic-primary)" />
          </div>

          <h1 class="fw-bold mb-3">О проекте «Город под контролем»</h1>
          <p class="lead text-muted mb-5">
            Муниципальный сервис для взаимодействия граждан с органами власти
          </p>

          <div class="row g-4 mb-5">
            <div class="col-12 col-md-4">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center p-4">
                  <IconFa name="graduation-cap" size="2rem" color="var(--civic-primary)" />
                  <h5 class="mt-3 fw-bold">Разработчик</h5>
                  <p class="text-muted small mb-0">
                    Студенческий проект, созданный в рамках выпускной квалификационной работы
                  </p>
                </div>
              </div>
            </div>
            <div class="col-12 col-md-4">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center p-4">
                  <IconFa name="code" size="2rem" color="var(--civic-primary)" />
                  <h5 class="mt-3 fw-bold">Технологии</h5>
                  <p class="text-muted small mb-0">
                    Vue 3, FastAPI, PostgreSQL, Leaflet, Pusher
                  </p>
                </div>
              </div>
            </div>
            <div class="col-12 col-md-4">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center p-4">
                  <IconFa name="calendar-alt" size="2rem" color="var(--civic-primary)" />
                  <h5 class="mt-3 fw-bold">Год</h5>
                  <p class="text-muted small mb-0">
                    2024-2025 учебный год
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="card bg-light border-0">
            <div class="card-body p-4">
              <h4 class="fw-bold mb-3">Контакты разработчика</h4>
              <div class="row g-3">
                <div class="col-12 col-md-4">
                  <IconFa name="envelope" class="me-2" color="var(--civic-primary)" />
                  <a href="mailto:dev@city-pc.ru" class="text-decoration-none">dev@city-pc.ru</a>
                </div>
                <div class="col-12 col-md-4">
                  <IconFa name="github" class="me-2" color="var(--civic-primary)" />
                  <a href="#" class="text-decoration-none">GitHub</a>
                </div>
                <div class="col-12 col-md-4">
                  <IconFa name="telegram" class="me-2" color="var(--civic-primary)" />
                  <a href="#" class="text-decoration-none">Telegram</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </PublicLayout>
</template>

<script>
import PublicLayout from '@/layouts/PublicLayout.vue'
import IconFa from '@/components/ui/IconFa.vue'

export default {
  name: 'AboutView',
  components: { PublicLayout, IconFa }
}
</script>