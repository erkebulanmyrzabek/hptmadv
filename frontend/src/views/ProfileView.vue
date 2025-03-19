<template>
  <div class="profile-view">
    <h1>Профиль</h1>
    <div v-if="user" class="profile-card">
      <img v-if="user.photo_url" :src="user.photo_url" alt="Аватар" class="avatar" />
      <div class="user-info">
        <h2>{{ user.first_name }} {{ user.last_name || '' }}</h2>
        <p>Username: @{{ user.username }}</p>
        <p>Кристаллы: {{ user.crystals }}</p>
        <p>Уровень: {{ user.level }}</p>
      </div>
    </div>
    <div v-else class="error-message">
      Не удалось загрузить данные пользователя.
    </div>
    <button class="logout-btn" @click="logout">Выйти</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
    console.log('Данные пользователя загружены:', user.value)
  } else {
    console.warn('Данные пользователя отсутствуют в localStorage.')
    router.push('/login')
  }
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  delete apiClient.defaults.headers.common['Authorization']
  console.log('Пользователь вышел из системы.')
  router.push('/login')
}
</script>

<style scoped>
.profile-view {
  padding: 20px;
  background: var(--surface-color);
  min-height: 100vh;
}

h1 {
  font-size: 24px;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: var(--surface-variant);
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-full);
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-info h2 {
  font-size: 20px;
  color: var(--text-primary);
  margin: 0;
}

.user-info p {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0;
}

.error-message {
  color: var(--error-color);
  background: var(--error-color-light);
  padding: 12px;
  border-radius: var(--radius-md);
  font-size: 14px;
}

.logout-btn {
  padding: 12px 24px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--error-color);
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #cc4444;
}
</style>