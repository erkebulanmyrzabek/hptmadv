<template>
  <div class="general-info">
    <!-- Cover Image and Status -->
    <div class="cover-section">
      <img :src="hackathon.coverImage" :alt="hackathon.title" class="cover-image">
      <div class="status-badge" :class="hackathon.status">
        {{ getStatusText(hackathon.status) }}
      </div>
    </div>

    <!-- Title and Description -->
    <div class="content-section">
      <h1>{{ hackathon.title }}</h1>
      <p class="description">{{ hackathon.description }}</p>

      <!-- Key Information -->
      <div class="key-info">
        <div class="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <div class="info-text">
            <span class="label">Даты проведения</span>
            <span class="value">{{ formatDate(hackathon.startDate) }} - {{ formatDate(hackathon.endDate) }}</span>
          </div>
        </div>

        <div class="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3"></circle>
          </svg>
          <div class="info-text">
            <span class="label">Место проведения</span>
            <span class="value">{{ hackathon.location }}</span>
          </div>
        </div>

        <div class="info-item">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="8" r="7"></circle>
            <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
          </svg>
          <div class="info-text">
            <span class="label">Призовой фонд</span>
            <span class="value">{{ formatPrize(hackathon.prizePool) }}</span>
          </div>
        </div>
      </div>

      <!-- Registration Progress -->
      <div class="registration-section">
        <div class="progress-bar">
          <div class="progress-text">
            <span>Регистрация открыта</span>
            <span>{{ getDaysLeft(hackathon.registrationStart) }} дней осталось</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: getRegistrationProgress() + '%' }"></div>
          </div>
        </div>
        <button class="register-btn" @click="$emit('openRegistration')">
          Зарегистрироваться
        </button>
      </div>

      <!-- Content Cards -->
      <div class="content-cards">
        <!-- Organizers -->
        <div class="content-card">
          <h2>Организаторы</h2>
          <div class="organizers-list">
            <div v-for="org in hackathon.organizers" :key="org.id" class="organizer-item">
              <img :src="org.logo" :alt="org.name">
              <span>{{ org.name }}</span>
            </div>
          </div>
        </div>

        <!-- Judges -->
        <div class="content-card">
          <h2>Судьи</h2>
          <div class="judges-list">
            <div v-for="judge in hackathon.judges" :key="judge.id" class="judge-item">
              <img :src="judge.avatar" :alt="judge.name">
              <div class="judge-info">
                <strong>{{ judge.name }}</strong>
                <span>{{ judge.position }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Schedule -->
        <div class="content-card">
          <h2>Расписание</h2>
          <div class="schedule-list">
            <div v-for="event in hackathon.schedule" :key="event.id" class="schedule-item">
              <div class="event-time">{{ formatEventTime(event.time) }}</div>
              <div class="event-info">
                <strong>{{ event.title }}</strong>
                <p>{{ event.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Rules -->
        <div class="content-card">
          <h2>Правила</h2>
          <ul class="rules-list">
            <li v-for="(rule, index) in hackathon.rules" :key="index">
              {{ rule }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  hackathon: {
    type: Object,
    required: true
  }
})

const getStatusText = (status) => {
  const statusMap = {
    registration: 'Регистрация',
    active: 'В процессе',
    completed: 'Завершён',
    upcoming: 'Скоро'
  }
  return statusMap[status] || status
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const formatEventTime = (time) => {
  return new Date(time).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatPrize = (prize) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(prize)
}

const getDaysLeft = (date) => {
  const diff = new Date(date) - new Date()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

const getRegistrationProgress = () => {
  const start = new Date(props.hackathon.registrationStart)
  const end = new Date(props.hackathon.startDate)
  const now = new Date()
  const total = end - start
  const current = now - start
  return Math.min(100, Math.max(0, (current / total) * 100))
}
</script>

<style scoped>
.general-info {
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.3s ease;
}

.cover-section {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
  box-shadow: var(--shadow-md);
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.cover-section:hover .cover-image {
  transform: scale(1.05);
}

.status-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  color: white;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.status-badge.registration {
  background: linear-gradient(135deg, #2ECC71, #27AE60);
}

.status-badge.active {
  background: linear-gradient(135deg, #3498DB, #2980B9);
}

.status-badge.completed {
  background: linear-gradient(135deg, #95A5A6, #7F8C8D);
}

.status-badge.upcoming {
  background: linear-gradient(135deg, #E74C3C, #C0392B);
}

.content-section {
  padding: 0 16px;
}

@media (min-width: 768px) {
  .content-section {
    padding: 0;
  }
}

h1 {
  margin: 0 0 16px;
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
}

.description {
  margin: 0 0 32px;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.key-info {
  display: grid;
  gap: 16px;
  margin-bottom: 32px;
}

@media (min-width: 768px) {
  .key-info {
    grid-template-columns: repeat(3, 1fr);
  }
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: var(--surface-variant);
  border-radius: var(--radius-lg);
  transition: transform 0.2s ease;
}

.info-item:hover {
  transform: translateY(-2px);
}

.info-item svg {
  width: 24px;
  height: 24px;
  color: var(--primary-color);
  flex-shrink: 0;
}

.info-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-text .label {
  font-size: 14px;
  color: var(--text-secondary);
}

.info-text .value {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

.registration-section {
  margin-bottom: 40px;
  padding: 24px;
  background: var(--surface-variant);
  border-radius: var(--radius-lg);
}

.progress-bar {
  margin-bottom: 16px;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.progress-track {
  height: 8px;
  background: var(--surface-color);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-color-light));
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

.register-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--primary-color);
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.register-btn:hover {
  background: var(--primary-color-dark);
  transform: translateY(-1px);
}

.content-cards {
  display: grid;
  gap: 24px;
}

@media (min-width: 768px) {
  .content-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

.content-card {
  padding: 24px;
  background: var(--surface-variant);
  border-radius: var(--radius-lg);
}

.content-card h2 {
  margin: 0 0 20px;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.organizers-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.organizer-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.organizer-item img {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  object-fit: cover;
}

.organizer-item span {
  font-size: 14px;
  color: var(--text-secondary);
}

.judges-list {
  display: grid;
  gap: 16px;
}

.judge-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.judge-item img {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  object-fit: cover;
}

.judge-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.judge-info strong {
  font-size: 16px;
  color: var(--text-primary);
}

.judge-info span {
  font-size: 14px;
  color: var(--text-secondary);
}

.schedule-list {
  display: grid;
  gap: 16px;
}

.schedule-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.schedule-item:last-child {
  padding-bottom: 0;
  border-bottom: none;
}

.event-time {
  font-size: 14px;
  font-weight: 500;
  color: var(--primary-color);
  white-space: nowrap;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.event-info strong {
  font-size: 16px;
  color: var(--text-primary);
}

.event-info p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.rules-list {
  margin: 0;
  padding-left: 20px;
}

.rules-list li {
  margin-bottom: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.rules-list li:last-child {
  margin-bottom: 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
