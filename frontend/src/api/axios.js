import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Замените на ваш URL бэкенда
  headers: {
    'Content-Type': 'application/json'
  }
})

// Интерцептор для добавления токена в запросы
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default apiClient