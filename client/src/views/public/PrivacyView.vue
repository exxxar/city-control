<!-- client/src/views/public/PrivacyView.vue -->
<template>
  <PublicLayout>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-md-8">
          <h1 class="fw-bold mb-4">Политика конфиденциальности</h1>

          <div class="privacy-content">
            <section class="mb-4">
              <h3 class="h5 fw-bold">1. Общие положения</h3>
              <p class="text-muted">
                Настоящая Политика конфиденциальности описывает, как муниципальный сервис
                «Город под контролем» собирает, использует и защищает персональные данные пользователей.
              </p>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">2. Какие данные мы собираем</h3>
              <ul class="text-muted">
                <li>Имя и контактные данные при регистрации</li>
                <li>Геолокация при создании обращений</li>
                <li>Фотографии и видео, загруженные пользователями</li>
                <li>История обращений и активность в системе</li>
              </ul>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">3. Как мы используем данные</h3>
              <p class="text-muted">
                Данные используются исключительно для обработки обращений граждан,
                улучшения качества муниципальных услуг и статистического анализа.
              </p>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">4. Защита данных</h3>
              <p class="text-muted">
                Мы применяем современные методы шифрования и защиты данных.
                Фотографии автоматически обрабатываются для размытия лиц и номеров автомобилей.
              </p>
            </section>

            <section class="mb-4">
              <h3 class="h5 fw-bold">5. Контакты</h3>
              <p class="text-muted">
                По вопросам обработки персональных данных обращайтесь:
                <a href="mailto:privacy@city-pc.ru">privacy@city-pc.ru</a>
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  </PublicLayout>
</template>

<script>
import PublicLayout from '@/layouts/PublicLayout.vue'

export default {
  name: 'PrivacyView',
  components: { PublicLayout }
}
</script>