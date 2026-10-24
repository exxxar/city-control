<!-- client/src/views/public/LandingView.vue -->
<template>
  <div class="home-page">
    <section class="home-intro">
      <div class="intro-copy">
        <span class="eyebrow">
          <i class="fas fa-map-marker-alt me-2"></i>
          ГОРОД ПОД КОНТРОЛЕМ
        </span>
        <h1>Чем займёмся <span>сегодня?</span></h1>
        <p>Сообщайте о проблемах, предлагайте идеи и объединяйте соседей.</p>
      </div>

      <router-link to="/map" class="map-shortcut">
        <span class="map-shortcut-icon">
          <i class="fas fa-layer-group"></i>
        </span>
        <span class="map-shortcut-copy">
          <strong>Карта города</strong>
          <small>Проблемы и обращения</small>
        </span>
        <i class="fas fa-arrow-right map-shortcut-arrow"></i>
      </router-link>
    </section>

    <!-- БЫСТРЫЕ ДЕЙСТВИЯ (основные) -->
    <section class="actions-section" aria-labelledby="actions-title">
      <div class="section-heading">
        <div>
          <h2 id="actions-title">Быстрые действия</h2>
          <p>Выберите нужный раздел</p>
        </div>
      </div>

      <div class="row g-3 g-xl-4">
        <!-- Сообщить о проблеме -->
        <div class="col-12 col-md-6 col-xl-4">
          <router-link
              to="/create"
              class="action-card action-card--problem"
              aria-label="Сообщить о проблеме"
          >
            <div class="action-card-top">
              <span class="action-icon">
                <i class="fas fa-exclamation-triangle"></i>
              </span>
              <span class="action-arrow" aria-hidden="true">
                <i class="fas fa-external-link-alt"></i>
              </span>
            </div>
            <div class="action-card-content">
              <span class="action-label">ОБРАЩЕНИЕ</span>
              <h3>Сообщить о проблеме</h3>
              <p>Ямы, освещение, мусор и другие городские проблемы.</p>
            </div>
            <span class="action-link">
              Создать обращение
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>

        <!-- Предложить инициативу -->
        <div class="col-12 col-md-6 col-xl-4">
          <router-link
              to="/initiatives/create"
              class="action-card action-card--initiative"
              aria-label="Предложить инициативу"
          >
            <div class="action-card-top">
              <span class="action-icon">
                <i class="fas fa-lightbulb"></i>
              </span>
              <span class="action-arrow" aria-hidden="true">
                <i class="fas fa-external-link-alt"></i>
              </span>
            </div>
            <div class="action-card-content">
              <span class="action-label">ИДЕЯ</span>
              <h3>Предложить инициативу</h3>
              <p>Предложите, как сделать район удобнее и лучше.</p>
            </div>
            <span class="action-link">
              Предложить идею
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>

        <!-- Организовать мероприятие -->
        <div class="col-12 col-md-6 col-xl-4">
          <router-link
              to="/events/create"
              class="action-card action-card--event"
              aria-label="Организовать мероприятие"
          >
            <div class="action-card-top">
              <span class="action-icon">
                <i class="fas fa-calendar-check"></i>
              </span>
              <span class="action-arrow" aria-hidden="true">
                <i class="fas fa-external-link-alt"></i>
              </span>
            </div>
            <div class="action-card-content">
              <span class="action-label">СОБЫТИЕ</span>
              <h3>Организовать мероприятие</h3>
              <p>Создайте событие для соседей и жителей города.</p>
            </div>
            <span class="action-link">
              Создать мероприятие
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- НОВАЯ СЕКЦИЯ: Дополнительные возможности -->
    <section class="extra-section" aria-labelledby="extra-title">
      <div class="section-heading">
        <div>
          <h2 id="extra-title">Дополнительные возможности</h2>
          <p>Инструменты для активного участия в жизни города</p>
        </div>
      </div>

      <div class="row g-3 g-xl-4">
        <!-- Камера -->
        <div class="col-12 col-md-6 col-xl-3">
          <router-link to="/camera" class="extra-card extra-card--camera">
            <div class="extra-card-top">
              <span class="extra-icon">
                <i class="fas fa-camera"></i>
              </span>
              <span class="extra-badge">NEW</span>
            </div>
            <div class="extra-card-content">
              <h4>Камера</h4>
              <p>Сфотографируйте проблему прямо сейчас</p>
            </div>
            <span class="extra-link">
              Открыть камеру
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>

        <!-- AR-режим -->
        <div class="col-12 col-md-6 col-xl-3">
          <router-link to="/ar" class="extra-card extra-card--ar">
            <div class="extra-card-top">
              <span class="extra-icon">
                <i class="fas fa-cube"></i>
              </span>
              <span class="extra-badge extra-badge--purple">BETA</span>
            </div>
            <div class="extra-card-content">
              <h4>AR-режим</h4>
              <p>Дополненная реальность с маркерами</p>
            </div>
            <span class="extra-link">
              Запустить AR
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>

        <!-- Уведомления -->
        <div class="col-12 col-md-6 col-xl-3">
          <router-link to="/notifications" class="extra-card extra-card--notifications">
            <div class="extra-card-top">
              <span class="extra-icon">
                <i class="fas fa-bell"></i>
              </span>
            </div>
            <div class="extra-card-content">
              <h4>Уведомления</h4>
              <p>Статусы ваших обращений</p>
            </div>
            <span class="extra-link">
              Посмотреть
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>

        <!-- Профиль -->
        <div class="col-12 col-md-6 col-xl-3">
          <router-link to="/profile" class="extra-card extra-card--profile">
            <div class="extra-card-top">
              <span class="extra-icon">
                <i class="fas fa-user-circle"></i>
              </span>
            </div>
            <div class="extra-card-content">
              <h4>Профиль</h4>
              <p>Настройки и личная информация</p>
            </div>
            <span class="extra-link">
              Открыть профиль
              <i class="fas fa-arrow-right ms-2"></i>
            </span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Мои обращения -->
    <section class="my-space">
      <div class="my-space-heading">
        <span class="my-space-icon">
          <i class="fas fa-tasks"></i>
        </span>
        <div>
          <h2>Мои обращения</h2>
          <p>Следите за статусом и отчитывайтесь о выполнении</p>
        </div>
      </div>

      <div class="my-space-actions">
        <router-link to="/problems" class="my-space-link">
          Перейти к обращениям
          <i class="fas fa-arrow-right ms-2"></i>
        </router-link>

        <router-link to="/reports/result" class="my-space-link my-space-link--secondary">
          Отчёт о выполнении
          <i class="fas fa-clipboard-check ms-2"></i>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'LandingView'
}
</script>

<style scoped>
.home-page {
  --home-ink: #172f40;
  --home-muted: #71818c;
  --home-accent: var(--civic-primary, #00a896);
  width: 100%;
  max-width: 1500px;
  min-height: 100%;
  margin-inline: auto;
  padding: clamp(1.1rem, 3vw, 2.5rem);
  color: var(--home-ink);
}

.home-intro {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  overflow: hidden;
  padding: clamp(1.5rem, 4vw, 3rem);
  border: 1px solid rgba(0, 168, 150, 0.12);
  border-radius: 26px;
  background:
      radial-gradient(circle at 88% 0%, rgba(0, 168, 150, 0.13), transparent 32%),
      linear-gradient(120deg, #fff 0%, #f2faf8 100%);
}

.intro-copy {
  position: relative;
  z-index: 1;
  max-width: 650px;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  margin-bottom: 1rem;
  color: #008f80;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.home-intro h1 {
  margin: 0;
  color: #172f40;
  font-size: clamp(2rem, 4.2vw, 3.5rem);
  font-weight: 800;
  letter-spacing: -0.055em;
  line-height: 1.08;
}

.home-intro h1 span {
  color: var(--home-accent);
}

.home-intro p {
  max-width: 540px;
  margin: 1rem 0 0;
  color: var(--home-muted);
  font-size: clamp(0.98rem, 1.4vw, 1.08rem);
  line-height: 1.7;
}

.map-shortcut {
  position: relative;
  z-index: 1;
  display: flex;
  min-width: 255px;
  align-items: center;
  gap: 0.85rem;
  padding: 1rem;
  border: 1px solid rgba(23, 47, 64, 0.07);
  border-radius: 17px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 8px 28px rgba(23, 47, 64, 0.06);
  color: var(--home-ink);
  text-decoration: none;
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.map-shortcut:hover {
  transform: translateY(-3px);
  border-color: rgba(0, 168, 150, 0.3);
  box-shadow: 0 14px 32px rgba(23, 47, 64, 0.1);
  color: var(--home-ink);
}

.map-shortcut-icon {
  display: inline-flex;
  width: 46px;
  height: 46px;
  flex: 0 0 46px;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: #e2f6f1;
  color: #008f80;
  font-size: 1.25rem;
}

.map-shortcut-copy {
  display: flex;
  min-width: 0;
  flex: 1;
  flex-direction: column;
  gap: 0.2rem;
}

.map-shortcut-copy strong {
  font-size: 0.9rem;
  font-weight: 750;
}

.map-shortcut-copy small {
  color: var(--home-muted);
  font-size: 0.75rem;
}

.map-shortcut-arrow {
  color: #7b8c95;
}

/* === Секции === */
.actions-section,
.extra-section {
  padding-top: clamp(2rem, 4vw, 3rem);
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.section-heading h2,
.my-space h2 {
  margin: 0;
  color: var(--home-ink);
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: -0.035em;
}

.section-heading p {
  margin: 0.35rem 0 0;
  color: var(--home-muted);
  font-size: 0.9rem;
}

/* === Основные карточки действий === */
.action-card {
  --action-accent: #c64752;
  --action-tint: #fff0f1;
  position: relative;
  display: flex;
  min-height: 285px;
  height: 100%;
  flex-direction: column;
  overflow: hidden;
  padding: 1.4rem;
  border: 1px solid #e8edf0;
  border-radius: 21px;
  background: #fff;
  color: inherit;
  text-decoration: none;
  box-shadow: 0 5px 20px rgba(23, 47, 64, 0.035);
  transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
}

.action-card::before {
  position: absolute;
  inset: 0 0 auto;
  height: 3px;
  background: var(--action-accent);
  content: "";
  opacity: 0.9;
}

.action-card::after {
  position: absolute;
  right: -55px;
  bottom: -70px;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: var(--action-tint);
  content: "";
  pointer-events: none;
  transition: transform 220ms ease;
}

.action-card--problem {
  --action-accent: #c64752;
  --action-tint: #fff0f1;
}

.action-card--initiative {
  --action-accent: #a66c00;
  --action-tint: #fff7df;
}

.action-card--event {
  --action-accent: #008f80;
  --action-tint: #e6f7f2;
}

.action-card:hover {
  transform: translateY(-5px);
  border-color: color-mix(in srgb, var(--action-accent) 30%, white);
  box-shadow: 0 17px 38px rgba(23, 47, 64, 0.09);
  color: inherit;
}

.action-card:hover::after {
  transform: scale(1.18);
}

.action-card:focus-visible,
.map-shortcut:focus-visible,
.my-space-link:focus-visible {
  outline: 3px solid rgba(0, 168, 150, 0.5);
  outline-offset: 4px;
}

.action-card-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.6rem;
}

.action-icon {
  display: inline-flex;
  width: 56px;
  height: 56px;
  align-items: center;
  justify-content: center;
  border-radius: 17px;
  background: var(--action-tint);
  color: var(--action-accent);
  font-size: 1.45rem;
  transition: transform 200ms ease;
}

.action-card:hover .action-icon {
  transform: scale(1.05) rotate(-3deg);
}

.action-arrow {
  display: inline-flex;
  width: 35px;
  height: 35px;
  align-items: center;
  justify-content: center;
  border: 1px solid #e9eef0;
  border-radius: 50%;
  color: #81909a;
  transition: color 180ms ease, background 180ms ease, border-color 180ms ease;
}

.action-card:hover .action-arrow {
  border-color: var(--action-accent);
  background: var(--action-accent);
  color: #fff;
}

.action-card-content {
  position: relative;
  z-index: 1;
}

.action-label {
  color: var(--action-accent);
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.action-card h3 {
  margin: 0.5rem 0 0.65rem;
  color: #172f40;
  font-size: 1.22rem;
  font-weight: 800;
  letter-spacing: -0.035em;
  line-height: 1.35;
}

.action-card p {
  margin: 0;
  color: var(--home-muted);
  font-size: 0.9rem;
  line-height: 1.65;
}

.action-link {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  margin-top: auto;
  padding-top: 1.5rem;
  color: var(--action-accent);
  font-size: 0.85rem;
  font-weight: 750;
}

.action-link i {
  transition: transform 180ms ease;
}

.action-card:hover .action-link i {
  transform: translateX(4px);
}

/* === НОВАЯ СЕКЦИЯ: Дополнительные карточки === */
.extra-card {
  --extra-accent: #00a896;
  --extra-tint: #e6f7f2;
  position: relative;
  display: flex;
  min-height: 220px;
  height: 100%;
  flex-direction: column;
  overflow: hidden;
  padding: 1.25rem;
  border: 1px solid #e8edf0;
  border-radius: 18px;
  background: #fff;
  color: inherit;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(23, 47, 64, 0.04);
  transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
}

.extra-card::before {
  position: absolute;
  inset: 0 0 auto;
  height: 3px;
  background: var(--extra-accent);
  content: "";
  opacity: 0.9;
}

.extra-card::after {
  position: absolute;
  right: -40px;
  bottom: -50px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: var(--extra-tint);
  content: "";
  pointer-events: none;
  transition: transform 220ms ease;
}

.extra-card--camera {
  --extra-accent: #0dcaf0;
  --extra-tint: #e0f7ff;
}

.extra-card--ar {
  --extra-accent: #6f42c1;
  --extra-tint: #f0e6ff;
}

.extra-card--notifications {
  --extra-accent: #fd7e14;
  --extra-tint: #fff4e6;
}

.extra-card--profile {
  --extra-accent: #4669b2;
  --extra-tint: #eef3ff;
}

.extra-card:hover {
  transform: translateY(-4px);
  border-color: color-mix(in srgb, var(--extra-accent) 30%, white);
  box-shadow: 0 12px 32px rgba(23, 47, 64, 0.08);
  color: inherit;
}

.extra-card:hover::after {
  transform: scale(1.15);
}

.extra-card-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.extra-icon {
  display: inline-flex;
  width: 48px;
  height: 48px;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: var(--extra-tint);
  color: var(--extra-accent);
  font-size: 1.35rem;
  transition: transform 200ms ease;
}

.extra-card:hover .extra-icon {
  transform: scale(1.05) rotate(-3deg);
}

.extra-badge {
  position: absolute;
  top: 0;
  right: 0;
  padding: 0.25rem 0.6rem;
  background: #00a896;
  color: white;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  border-radius: 20px;
}

.extra-badge--purple {
  background: #6f42c1;
}

.extra-card-content {
  position: relative;
  z-index: 1;
}

.extra-card h4 {
  margin: 0 0 0.5rem;
  color: #172f40;
  font-size: 1.1rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.3;
}

.extra-card p {
  margin: 0;
  color: var(--home-muted);
  font-size: 0.85rem;
  line-height: 1.5;
}

.extra-link {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  margin-top: auto;
  padding-top: 1.25rem;
  color: var(--extra-accent);
  font-size: 0.82rem;
  font-weight: 750;
}

.extra-link i {
  transition: transform 180ms ease;
}

.extra-card:hover .extra-link i {
  transform: translateX(4px);
}

/* === Мои обращения === */
.my-space {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
  margin-top: 1.5rem;
  padding: 1.25rem 1.4rem;
  border: 1px solid #e8edf0;
  border-radius: 20px;
  background: #fff;
}

.my-space-heading {
  display: flex;
  align-items: center;
  gap: 0.9rem;
}

.my-space-icon {
  display: inline-flex;
  width: 46px;
  height: 46px;
  flex: 0 0 46px;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: #eef3ff;
  color: #4669b2;
  font-size: 1.2rem;
}

.my-space h2 {
  font-size: 1rem;
}

.my-space p {
  margin: 0.3rem 0 0;
  color: var(--home-muted);
  font-size: 0.82rem;
}

.my-space-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: flex-end;
}

.my-space-link {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  color: #008f80;
  font-size: 0.84rem;
  font-weight: 750;
  text-decoration: none;
}

.my-space-link:hover {
  color: #006f65;
}

.my-space-link--secondary {
  color: var(--home-ink);
  border: 1px solid #e8edf0;
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  font-size: 0.84rem;
  font-weight: 750;
  text-decoration: none;
  transition: all 180ms ease;
  display: inline-flex;
  align-items: center;
}

.my-space-link--secondary:hover {
  border-color: var(--home-accent);
  color: var(--home-accent);
  background: rgba(0, 168, 150, 0.04);
}

/* === Адаптивность === */
@media (max-width: 991.98px) {
  .home-intro {
    align-items: flex-start;
    flex-direction: column;
  }

  .map-shortcut {
    width: 100%;
    min-width: 0;
  }

  .action-card {
    min-height: 270px;
  }
}

@media (max-width: 575.98px) {
  .home-page {
    padding: 1rem 0.85rem 1.5rem;
  }

  .home-intro {
    gap: 1.35rem;
    padding: 1.4rem 1.15rem;
    border-radius: 21px;
  }

  .eyebrow {
    margin-bottom: 0.8rem;
    font-size: 0.64rem;
  }

  .home-intro h1 {
    font-size: clamp(2rem, 9vw, 2.65rem);
  }

  .home-intro p {
    margin-top: 0.75rem;
    font-size: 0.92rem;
  }

  .actions-section,
  .extra-section {
    padding-top: 1.8rem;
  }

  .section-heading h2 {
    font-size: 1.2rem;
  }

  .section-heading p {
    font-size: 0.82rem;
  }

  .action-card {
    min-height: 255px;
    padding: 1.1rem;
    border-radius: 18px;
  }

  .action-card-top {
    margin-bottom: 1.2rem;
  }

  .action-icon {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    font-size: 1.25rem;
  }

  .action-card h3 {
    font-size: 1.05rem;
  }

  .action-card p {
    font-size: 0.83rem;
  }

  .action-link {
    padding-top: 1.2rem;
    font-size: 0.79rem;
  }

  .extra-card {
    min-height: 200px;
    padding: 1rem;
    border-radius: 16px;
  }

  .extra-icon {
    width: 42px;
    height: 42px;
    font-size: 1.2rem;
  }

  .extra-card h4 {
    font-size: 1rem;
  }

  .extra-card p {
    font-size: 0.8rem;
  }

  .extra-link {
    padding-top: 1rem;
    font-size: 0.78rem;
  }

  .my-space {
    align-items: flex-start;
    flex-direction: column;
    padding: 1rem;
  }

  .my-space-actions {
    width: 100%;
    align-items: stretch;
    margin-top: 0.5rem;
  }

  .my-space-link,
  .my-space-link--secondary {
    justify-content: center;
    padding: 0.85rem;
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .action-card,
  .action-card::after,
  .action-icon,
  .action-arrow,
  .action-link i,
  .extra-card,
  .extra-card::after,
  .extra-icon,
  .extra-link i,
  .map-shortcut {
    transition: none !important;
  }

  .action-card:hover,
  .extra-card:hover,
  .map-shortcut:hover {
    transform: none;
  }
}
</style>