<!-- client/src/views/public/ContactsView.vue -->
<template>
  <div class="contacts-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">Контакты</h1>
      <p class="page-subtitle">Свяжитесь с нами любым удобным способом</p>
    </div>

    <!-- Карточки контактов -->
    <div class="contacts-grid">
      <div class="contact-card">
        <div class="contact-icon-wrapper contact-icon--blue">
          <i class="fas fa-envelope"></i>
        </div>
        <h3 class="contact-title">Email</h3>
        <p class="contact-description">Напишите нам на почту</p>
        <a href="mailto:info@city-pc.ru" class="contact-link">
          info@city-pc.ru
          <i class="fas fa-arrow-right ms-2"></i>
        </a>
      </div>

      <div class="contact-card">
        <div class="contact-icon-wrapper contact-icon--green">
          <i class="fas fa-phone"></i>
        </div>
        <h3 class="contact-title">Телефон</h3>
        <p class="contact-description">Позвоните нам в рабочее время</p>
        <a href="tel:+74951234567" class="contact-link">
          +7 (949) 374 90 56
          <i class="fas fa-arrow-right ms-2"></i>
        </a>
      </div>

      <div class="contact-card">
        <div class="contact-icon-wrapper contact-icon--purple">
          <i class="fas fa-map-marker-alt"></i>
        </div>
        <h3 class="contact-title">Адрес</h3>
        <p class="contact-description">Приходите к нам в офис</p>
        <div class="contact-address">
          г. Донецк,<br>
          пр. Театральный, 13, ауд. 416
        </div>
      </div>
    </div>

    <!-- Часы работы и дополнительная информация -->
    <div class="info-grid">
      <div class="info-card">
        <div class="info-header">
          <i class="fas fa-clock info-icon"></i>
          <h3 class="info-title">Часы работы</h3>
        </div>
        <div class="info-content">
          <div class="schedule-row">
            <span class="schedule-day">Понедельник - Пятница</span>
            <span class="schedule-time">9:00 - 17:00</span>
          </div>
          <div class="schedule-row">
            <span class="schedule-day">Суббота - Воскресенье</span>
            <span class="schedule-time schedule-closed">Выходной</span>
          </div>
        </div>
      </div>

      <div class="info-card">
        <div class="info-header">
          <i class="fas fa-info-circle info-icon"></i>
          <h3 class="info-title">Важная информация</h3>
        </div>
        <div class="info-content">
          <p class="info-text">
            Мы отвечаем на все обращения в течение 24 часов в рабочие дни.
            Для срочных вопросов используйте телефон горячей линии.
          </p>
          <a href="tel:+74951234567" class="info-link">
            <i class="fas fa-phone-alt me-2"></i>
            Горячая линия
          </a>
        </div>
      </div>
    </div>

    <!-- Карта (опционально) -->
    <div class="map-section">
      <div class="map-header">
        <i class="fas fa-map-marked-alt map-icon"></i>
        <h3 class="map-title">Как нас найти</h3>
      </div>
      <div class="map-container">
        <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2259.1234567890123!2d37.5460!3d55.4315!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNTXCsDI1JzUzLjQiTiAzN8KwMzInNDUuNiJF!5e0!3m2!1sru!2sru!4v1234567890123!5m2!1sru!2sru"
            width="100%"
            height="100%"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ContactsView'
}
</script>

<style scoped>
/* === Дизайн-система === */
.contacts-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #172f40;
  letter-spacing: -0.03em;
  margin: 0 0 0.5rem;
}

.page-subtitle {
  color: #70808c;
  font-size: 1.1rem;
  margin: 0;
}

/* === Сетка контактов === */
.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.contact-card {
  background: #ffffff;
  border: 1px solid #e8edf0;
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
}

.contact-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(23, 47, 64, 0.1);
}

.contact-icon-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 1.75rem;
  color: white;
}

.contact-icon--blue {
  background: linear-gradient(135deg, #0dcaf0, #0aa2c0);
  box-shadow: 0 8px 20px rgba(13, 202, 240, 0.3);
}

.contact-icon--green {
  background: linear-gradient(135deg, #00a896, #087e8b);
  box-shadow: 0 8px 20px rgba(0, 168, 150, 0.3);
}

.contact-icon--purple {
  background: linear-gradient(135deg, #6f42c1, #5a32a3);
  box-shadow: 0 8px 20px rgba(111, 66, 193, 0.3);
}

.contact-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #172f40;
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}

.contact-description {
  color: #70808c;
  font-size: 0.9rem;
  margin: 0 0 1rem;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  color: #00a896;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.contact-link:hover {
  color: #008f80;
  transform: translateX(4px);
}

.contact-address {
  color: #172f40;
  font-weight: 600;
  font-size: 1rem;
  line-height: 1.5;
}

/* === Сетка информации === */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.info-card {
  background: #ffffff;
  border: 1px solid #e8edf0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
}

.info-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(0, 168, 150, 0.1);
  color: #00a896;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.info-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #172f40;
  margin: 0;
  letter-spacing: -0.02em;
}

.info-content {
  color: #172f40;
}

.schedule-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e8edf0;
}

.schedule-row:last-child {
  border-bottom: none;
}

.schedule-day {
  font-weight: 600;
  color: #172f40;
}

.schedule-time {
  font-weight: 700;
  color: #00a896;
}

.schedule-closed {
  color: #c64752;
}

.info-text {
  color: #70808c;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0 0 1rem;
}

.info-link {
  display: inline-flex;
  align-items: center;
  color: #00a896;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
}

.info-link:hover {
  color: #008f80;
}

/* === Секция карты === */
.map-section {
  background: #ffffff;
  border: 1px solid #e8edf0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(23, 47, 64, 0.04);
}

.map-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.map-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(111, 66, 193, 0.1);
  color: #6f42c1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.map-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #172f40;
  margin: 0;
  letter-spacing: -0.02em;
}

.map-container {
  width: 100%;
  height: 400px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e8edf0;
}

/* === Адаптивность === */
@media (max-width: 767.98px) {
  .contacts-page {
    padding: 2rem 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .contacts-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .map-container {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }

  .contact-card,
  .info-card,
  .map-section {
    padding: 1.5rem;
  }

  .contact-icon-wrapper {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
}
</style>