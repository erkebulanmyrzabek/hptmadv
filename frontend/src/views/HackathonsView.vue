<template>
  <div class="hackathons-view">
    <!-- Поиск и фильтры -->
    <div class="search-section">
      <div class="search-bar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск хакатонов..." 
          @input="filterHackathons"
        />
      </div>
      
      <div class="filters-sort">
        <div class="filters-scroll" ref="filtersScroll">
          <button 
            v-for="filter in filters" 
            :key="filter.value"
            :class="['filter-btn', { active: currentFilter === filter.value }]"
            @click="currentFilter = filter.value"
          >
            {{ filter.label }}
          </button>
        </div>
        
        <div class="sort-dropdown">
          <button @click="showSortOptions = !showSortOptions" class="sort-btn">
            <span>{{ getCurrentSortLabel() }}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
          <div v-if="showSortOptions" class="sort-options">
            <button 
              v-for="option in sortOptions" 
              :key="option.value"
              :class="{ active: currentSort === option.value }"
              @click="setSort(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Сетка хакатонов -->
    <div v-if="loading" class="loading-state">
      <svg class="spinner" viewBox="0 0 50 50">
        <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
      </svg>
      <p>Загрузка хакатонов...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <p>{{ error }}</p>
      <button @click="loadHackathons" class="retry-btn">Попробовать снова</button>
    </div>

    <div v-else class="hackathons-grid">
      <div 
        v-for="hackathon in filteredHackathons" 
        :key="hackathon.id" 
        class="hackathon-card"
      >
        <div class="card-header">
          <div 
            class="hackathon-cover" 
            :style="{ backgroundImage: `url(${hackathon.cover_image || getDefaultBackground(hackathon.tracks && hackathon.tracks.length > 0 ? hackathon.tracks[0].title.toLowerCase() : 'default')})` }"
          >
            <div class="cover-overlay">
              <div class="status-tags">
                <span :class="['status-tag', hackathon.status]">
                  {{ getStatusLabel(hackathon.status) }}
                </span>
                <span v-if="hackathon.featured" class="featured-tag">
                  Рекомендуем
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="card-content">
          <div class="card-main">
            <h3>{{ hackathon.title }}</h3>
            <p>{{ hackathon.description }}</p>
            
            <div class="tags-container">
              <span v-for="tag in getHackathonTags(hackathon)" :key="tag" class="tag">
                {{ tag }}
              </span>
            </div>
          </div>

          <div class="card-details">
            <div class="detail-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <span>{{ formatDate(hackathon.start_date) }}</span>
            </div>
            
            <div class="detail-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
              <span>{{ formatPrize(hackathon.prize_pool) }}</span>
            </div>

            <div class="detail-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              <span>{{ hackathon.participants ? hackathon.participants.length : 0 }}</span>
            </div>
          </div>

          <div class="card-actions">
            <button 
              class="action-btn favorite-btn" 
              :class="{ active: hackathon.isFavorite }"
              @click.stop="toggleFavorite(hackathon.id)"
              :aria-label="hackathon.isFavorite ? 'Удалить из избранного' : 'Добавить в избранное'"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
              </svg>
            </button>

            <button 
              class="action-btn share-btn"
              @click.stop="shareHackathon(hackathon)"
              aria-label="Поделиться"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="18" cy="5" r="3"/>
                <circle cx="6" cy="12" r="3"/>
                <circle cx="18" cy="19" r="3"/>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
              </svg>
            </button>

            <div class="main-buttons">
              <router-link 
                v-if="hackathon.id && canRegister(hackathon)"
                :to="{ name: 'hackathon-details', params: { id: hackathon.id }, hash: '#registration' }" 
                class="register-btn"
              >
                Зарегистрироваться
              </router-link>
              <router-link 
                v-if="hackathon.id"
                :to="{ name: 'hackathon-details', params: { id: hackathon.id }}" 
                class="details-btn"
              >
                Подробнее
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios' // Импортируем настроенный axios

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const currentFilter = ref('all')
const currentSort = ref('date')
const showSortOptions = ref(false)

// Фильтры
const filters = [
  { label: 'Все', value: 'all' },
  { label: 'Активные', value: 'active' },
  { label: 'Скоро', value: 'upcoming' },
  { label: 'Завершенные', value: 'completed' },
  { label: 'AI & ML', value: 'ai & ml' },
  { label: 'Web3', value: 'web3' },
  { label: 'GameDev', value: 'gamedev' }
]

// Опции сортировки
const sortOptions = [
  { label: 'По дате', value: 'date' },
  { label: 'По призовому фонду', value: 'prize' },
  { label: 'По популярности', value: 'popularity' }
]

// Данные хакатонов
const hackathons = ref([])

// Загрузка хакатонов через API
const loadHackathons = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await apiClient.get('/api/hackathons/')
    const data = Array.isArray(response.data) ? response.data : [response.data]
    hackathons.value = data
      .filter(hackathon => {
        if (!hackathon.id) {
          console.warn('Хакатон без ID:', hackathon)
          return false
        }
        return true
      })
      .map(hackathon => ({
        ...hackathon,
        isFavorite: false,
        featured: hackathon.status === 'registration',
        tracks: hackathon.tracks || [],
        participants: hackathon.participants || []
      }))
  } catch (e) {
    error.value = 'Не удалось загрузить хакатоны. Попробуйте позже.'
    console.error('Ошибка при загрузке хакатонов:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadHackathons()
})

// Функции для фильтров и сортировки
const getCurrentSortLabel = () => {
  return sortOptions.find(option => option.value === currentSort.value)?.label || ''
}

const setSort = (value) => {
  currentSort.value = value
  showSortOptions.value = false
}

// Фильтрация хакатонов
const filteredHackathons = computed(() => {
  let filtered = hackathons.value

  // Фильтр по поиску
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(hackathon => 
      hackathon.title.toLowerCase().includes(query) ||
      hackathon.description.toLowerCase().includes(query) ||
      getHackathonTags(hackathon).some(tag => tag.toLowerCase().includes(query))
    )
  }

  // Фильтр по категории
  if (currentFilter.value !== 'all') {
    if (['active', 'upcoming', 'completed'].includes(currentFilter.value)) {
      filtered = filtered.filter(h => h.status === currentFilter.value)
    } else {
      filtered = filtered.filter(h => 
        h.tracks.some(track => track.title.toLowerCase() === currentFilter.value)
      )
    }
  }

  // Сортировка
  filtered.sort((a, b) => {
    switch (currentSort.value) {
      case 'prize':
        return b.prize_pool - a.prize_pool
      case 'popularity':
        return (b.participants ? b.participants.length : 0) - (a.participants ? a.participants.length : 0)
      case 'date':
      default:
        return new Date(a.start_date) - new Date(b.start_date)
    }
  })

  return filtered
})

const filterHackathons = () => {
  // Фильтрация выполняется автоматически через computed
}

// Форматирование
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const formatPrize = (prize) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'KZT',
    maximumFractionDigits: 0
  }).format(prize)
}

const getStatusLabel = (status) => {
  const labels = {
    registration: 'Регистрация',
    upcoming: 'Скоро',
    active: 'Активный',
    completed: 'Завершен'
  }
  return labels[status] || status
}

const getDefaultBackground = (type) => {
  const backgrounds = {
    'ai & ml': '/images/default-ai.jpg',
    'web3': '/images/default-web3.jpg',
    'gamedev': '/images/default-gamedev.jpg',
    'default': '/images/default-hackathon.jpg'
  }
  return backgrounds[type] || '/images/default-hackathon.jpg'
}

const getHackathonTags = (hackathon) => {
  const tags = []
  hackathon.tracks.forEach(track => {
    tags.push(track.title)
  })
  return tags
}

// Действия с карточками
const toggleFavorite = (id) => {
  const hackathon = hackathons.value.find(h => h.id === id)
  if (hackathon) {
    hackathon.isFavorite = !hackathon.isFavorite
  }
}

const shareHackathon = (hackathon) => {
  const url = `${window.location.origin}/hackathons/${hackathon.id}`
  navigator.clipboard.writeText(url)
    .then(() => {
      alert('Ссылка скопирована!')
    })
    .catch(() => {
      alert('Не удалось скопировать ссылку.')
    })
}

const canRegister = (hackathon) => {
  return hackathon.status === 'registration' && 
    new Date(hackathon.registration_start) <= new Date() &&
    new Date(hackathon.start_date) > new Date()
}
</script>

<style scoped>
/* Стили остаются без изменений */
.hackathons-view {
  padding: 20px;
  margin-bottom: 70px;
}

@media (min-width: 768px) {
  .hackathons-view {
    margin-top: 70px;
    margin-bottom: 0;
  }
}

/* Поиск и фильтры */
.search-section {
  margin-bottom: 24px;
}

.search-bar {
  position: relative;
  margin-bottom: 16px;
}

.search-bar svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
}

.search-bar input {
  width: 100%;
  padding: 12px 12px 12px 44px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  background: var(--surface-color);
  color: var(--text-primary);
  font-size: 16px;
  transition: all 0.2s ease;
}

.search-bar input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-color-light);
}

.filters-sort {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.filters-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 8px;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.filters-scroll::-webkit-scrollbar {
  display: none;
}

.filter-btn {
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: var(--surface-color);
  color: var(--text-secondary);
  font-size: 14px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: var(--surface-variant);
}

.filter-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.sort-dropdown {
  position: relative;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--surface-color);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-btn:hover {
  background: var(--surface-variant);
}

.sort-options {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  padding: 8px 0;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.sort-options button {
  display: block;
  width: 100%;
  padding: 8px 16px;
  text-align: left;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-options button:hover {
  background: var(--surface-variant);
}

.sort-options button.active {
  color: var(--primary-color);
  font-weight: 500;
}

/* Состояния загрузки и ошибки */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  text-align: center;
  color: var(--text-secondary);
}

.spinner {
  width: 50px;
  height: 50px;
  animation: rotate 2s linear infinite;
}

.spinner .path {
  stroke: var(--primary-color);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

.error-state svg {
  color: var(--error-color);
  margin-bottom: 16px;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 16px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: var(--primary-color-dark);
}

/* Сетка хакатонов */
.hackathons-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}

/* Карточка хакатона */
.hackathon-card {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hackathon-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.card-header {
  position: relative;
}

.hackathon-cover {
  height: 200px;
  background-size: cover;
  background-position: center;
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.4));
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.status-tags {
  display: flex;
  gap: 8px;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.status-tag.registration {
  background: #2ECC71;
}

.status-tag.upcoming {
  background: #F39C12;
}

.status-tag.active {
  background: #3498DB;
}

.status-tag.completed {
  background: #95A5A6;
}

.featured-tag {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  color: white;
  background: rgba(0, 0, 0, 0.5);
}

.card-content {
  padding: 20px;
}

.card-main h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.card-main p {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  padding: 4px 12px;
  background: var(--surface-variant);
  color: var(--text-secondary);
  border-radius: 16px;
  font-size: 12px;
}

.card-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
}

.detail-item svg {
  color: var(--text-tertiary);
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  color: var(--primary-color);
}

.action-btn.active {
  color: var(--primary-color);
}

.action-btn svg {
  width: 20px;
  height: 20px;
}

.favorite-btn.active svg {
  fill: currentColor;
}

.main-buttons {
  flex: 1;
  display: flex;
  gap: 8px;
}

.register-btn,
.details-btn {
  flex: 1;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.register-btn {
  background: #2ECC71;
  color: white;
  border: none;
}

.register-btn:hover {
  background: #27AE60;
}

.details-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  text-decoration: none;
}

.details-btn:hover {
  background: var(--primary-color-dark);
}

@media (max-width: 768px) {
  .filters-sort {
    flex-direction: column;
    align-items: stretch;
  }

  .sort-dropdown {
    width: 100%;
  }

  .sort-btn {
    width: 100%;
    justify-content: space-between;
  }

  .sort-options {
    width: 100%;
  }

  .hackathons-grid {
    grid-template-columns: 1fr;
  }
}
</style>