<!-- client/src/views/public/TermsView.vue -->
<template>

    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-md-8">
          <h1 class="fw-bold mb-4">Условия использования</h1>

          <div class="terms-content">
            <section class="mb-4">
              <h3 class="h5 fw-bold">1. Принятие условий</h3>
              <p class="text-muted">
                Используя сервис «Город под контролем», вы соглашаетесь с настоящими Условиями использования.
              </p>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">2. Правила использования</h3>
              <ul class="text-muted">
                <li>Предоставляйте достоверную информацию</li>
                <li>Не публикуйте оскорбительный контент</li>
                <li>Уважайте других пользователей</li>
                <li>Используйте сервис по назначению</li>
              </ul>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">3. Ответственность</h3>
              <p class="text-muted">
                Пользователь несёт ответственность за достоверность предоставленной информации
                и соблюдение законодательства РФ.
              </p>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">4. Изменение условий</h3>
              <p class="text-muted">
                Администрация оставляет за собой право изменять условия использования.
                Актуальная версия всегда доступна на этой странице.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>

</template>

<script>
import PublicLayout from '@/layouts/PublicLayout.vue'

export default {
  name: 'TermsView',
  components: { PublicLayout }
}
</script>