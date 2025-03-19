<template>
    <div class="login-view">
      <h1>Авторизация</h1>
      <button class="login-btn" @click="loginWithTelegram" :disabled="isLoggingIn">
        {{ isLoggingIn ? 'Авторизация...' : 'Войти через Telegram' }}
      </button>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/api/axios'
  
  const router = useRouter()
  const isLoggingIn = ref(false)
  const errorMessage = ref('')
  
  const loginWithTelegram = async () => {
    if (!window.Telegram || !window.Telegram.WebApp) {
      errorMessage.value = 'Telegram Web App не доступен. Откройте приложение через Telegram.'
      console.error('Telegram Web App не инициализирован.')
      return
    }
  
    const initData = window.Telegram.WebApp.initData
    if (!initData) {
      errorMessage.value = 'Не удалось получить initData от Telegram.'
      console.error('initData отсутствует.')
      return
    }
  
    isLoggingIn.value = true
    errorMessage.value = ''
    try {
      const response = await apiClient.post('/api/login/telegram/', { initData })
      const { access_token, refresh_token, user } = response.data
  
      // Сохраняем токены и данные пользователя
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify(user))
  
      // Настраиваем заголовок авторизации для последующих запросов
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
  
      console.log('Успешная авторизация:', user)
      router.push('/profile') // Перенаправляем на страницу профиля
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Ошибка авторизации. Попробуйте снова.'
      errorMessage.value = errorMsg
      console.error('Ошибка авторизации:', errorMsg, error)
    } finally {
      isLoggingIn.value = false
    }
  }
  </script>
  
  <style scoped>
  .login-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: var(--surface-color);
    padding: 20px;
  }
  
  h1 {
    font-size: 24px;
    color: var(--text-primary);
    margin-bottom: 24px;
  }
  
  .login-btn {
    padding: 12px 24px;
    border: none;
    border-radius: var(--radius-md);
    background: var(--primary-color);
    color: white;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
  }
  
  .login-btn:hover {
    background: var(--primary-color-dark);
  }
  
  .login-btn:disabled {
    background: var(--text-tertiary);
    cursor: not-allowed;
  }
  
  .error-message {
    color: var(--error-color);
    background: var(--error-color-light);
    padding: 12px;
    border-radius: var(--radius-md);
    margin-top: 16px;
    font-size: 14px;
  }
  </style>