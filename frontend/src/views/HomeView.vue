<template>
  <div class="home-view" :class="theme">
    <header class="header">
      <div class="user-info">
        <div class="avatar" :style="{ backgroundColor: getAvatarColor() }">
          {{ getUserInitials() }}
        </div>
        <h2>{{ user.name }}</h2>
      </div>
      <div class="notifications-wrapper">
        <button class="notifications-button" @click="toggleNotifications">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 22C13.1 22 14 21.1 14 20H10C10 21.1 10.9 22 12 22ZM18 16V11C18 7.93 16.37 5.36 13.5 4.68V4C13.5 3.17 12.83 2.5 12 2.5C11.17 2.5 10.5 3.17 10.5 4V4.68C7.64 5.36 6 7.92 6 11V16L4 18V19H20V18L18 16ZM16 17H8V11C8 8.52 9.51 6.5 12 6.5C14.49 6.5 16 8.52 16 11V17Z" fill="currentColor"/>
          </svg>
          <span v-if="unreadNotificationsCount" class="notification-badge">{{ unreadNotificationsCount }}</span>
        </button>
        
        <!-- Notifications Popup -->
        <div v-if="showNotifications" class="notifications-popup">
          <div class="notifications-header">
            <h3>Уведомления</h3>
            <button @click="closeNotifications">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          <div class="notifications-list">
            <div v-for="notification in notifications" 
                :key="notification.id"
                class="notification-item"
                :class="{ unread: !notification.read }"
                @click="markAsRead(notification.id)">
              <div class="notification-icon" :class="notification.type">
                <svg v-if="notification.type === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else-if="notification.type === 'info'" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M12 9V11M12 15H12.01M5.07183 19H18.9282C20.4678 19 21.4301 17.3333 20.6603 16L13.7321 4C12.9623 2.66667 11.0377 2.66667 10.2679 4L3.33975 16C2.56998 17.3333 3.53223 19 5.07183 19ZM16 17H8V11C8 8.52 9.51 6.5 12 6.5C14.49 6.5 16 8.52 16 11V17Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="notification-content">
                <p>{{ notification.text }}</p>
                <span class="notification-time">{{ formatNotificationTime(notification.time) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <section v-for="category in categories" :key="category.id" class="events-section">
        <div class="section-header">
          <h2>{{ category.name }}</h2>
        </div>
        
        <div class="events-container">
          <div class="events-scroll" :ref="el => categoryScrollRefs[category.id] = el">
            <div class="events-grid">
              <div 
                v-for="event in getEventsByCategory(category.id)" 
                :key="event.id"
                class="event-card"
                @click="router.push(`/hackathons/${event.id}`)"
              >
                <div class="event-image" :style="{ backgroundImage: `url(${event.backgroundImage || getDefaultBackground(event.type)})` }">
                  <div class="event-overlay">
                    <div class="event-header">
                      <span class="event-status" :class="event.status">
                        {{ getStatusLabel(event.status) }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="event-content">
                  <h3>{{ event.title }}</h3>
                  <div class="event-info">
                    <span class="event-date">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M8 7V3M16 7V3M7 11H17M5 21H19C20.1046 21 21 20.1046 21 19V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V19C3 20.1046 3.89543 21 5 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      {{ formatDate(event.date) }}
                    </span>
                    <span class="event-participants">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.3503 17.623 3.8507 18.1676 4.55231C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89317 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      {{ event.participants }}
                    </span>
                  </div>
                  <div class="event-tags">
                    <span v-for="tag in event.tags" :key="tag" class="tag">
                      {{ tag }}
                    </span>
                  </div>
                  <div v-if="event.prize" class="event-prize">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M12 15C8.13401 15 5 11.866 5 8V7C5 6.44772 5.44772 6 6 6H18C18.5523 6 19 6.44772 19 7V8C19 11.866 15.866 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M8.5 14.5V17C8.5 17 8.5 19 12 19C15.5 19 15.5 17 15.5 17V14.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M19 8H20C21.1046 8 22 7.10457 22 6V5C22 3.89543 21.1046 3 20 3H4C2.89543 3 2 3.89543 2 5V6C2 7.10457 2.89543 8 4 8H5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    {{ event.prize }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button 
            v-if="canScrollLeft(category.id)"
            class="scroll-button left" 
            @click="scrollCategory('left', category.id)"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M15 19L8 12L15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button 
            v-if="canScrollRight(category.id)"
            class="scroll-button right" 
            @click="scrollCategory('right', category.id)"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M9 5L16 12L9 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </section>

      <section class="news-section">
        <div class="section-header">
          <h2>Новости</h2>
          <div class="news-filters">
            <button 
              v-for="filter in newsFilters" 
              :key="filter.value"
              :class="['filter-btn', { active: currentNewsFilter === filter.value }]"
              @click="currentNewsFilter = filter.value"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>

        <div class="news-search">
          <input 
            type="text" 
            v-model="newsSearchQuery" 
            placeholder="Поиск новостей..."
            class="search-input"
          >
        </div>

        <div class="news-list">
          <div 
            v-for="news in filteredNews" 
            :key="news.id" 
            class="news-card"
            :class="{ 'has-image': news.image }"
          >
            <div class="news-image" v-if="news.image">
              <img :src="news.image" :alt="news.title" loading="lazy">
            </div>
            <div v-else class="news-icon">
              {{ getNewsIcon(news.type) }}
            </div>
            
            <div class="news-content">
              <div class="news-meta">
                <span :class="['news-type', news.type]">
                  {{ getNewsTypeLabel(news.type) }}
                </span>
                <span class="news-date">{{ formatDate(news.date) }}</span>
              </div>
              
              <h3>{{ news.title }}</h3>
              <p>{{ news.description }}</p>
              
              <div class="news-actions">
                <button class="action-btn like-btn" @click.stop="toggleLike(news.id)" :class="{ 'active': news.isLiked }" :aria-label="news.isLiked ? 'Убрать лайк' : 'Поставить лайк'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                  <span class="count" v-if="news.likes">{{ news.likes }}</span>
                </button>
                <button class="action-btn" @click.stop="openComments(news)" aria-label="Комментарии">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
                  </svg>
                  <span class="count" v-if="news.comments">{{ news.comments }}</span>
                </button>
                <button class="action-btn" @click.stop="shareNews(news)" aria-label="Поделиться">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="18" cy="5" r="3" />
                    <circle cx="6" cy="12" r="3" />
                    <circle cx="18" cy="19" r="3" />
                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
                  </svg>
                </button>
                <button class="details-btn" @click.stop="openNewsDetails(news)">
                  Подробнее
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Notifications popup -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import { TransitionGroup } from 'vue'

const { theme, toggleTheme } = useTheme()

const router = useRouter()

// Categories
const categories = [
  { id: 'hackathons', name: 'Хакатоны', icon: 'hackathon' },
  { id: 'webinars', name: 'Вебинары', icon: 'webinar' },
  { id: 'cases', name: 'Кейс-чемпионаты', icon: 'case' }
]

// Events
const events = ref([
  // Хакатоны
  {
    id: 1,
    title: 'AI Хакатон 2025',
    type: 'hackathons',
    status: 'upcoming',
    date: '2025-03-20',
    participants: 128,
    tags: ['Python', 'AI/ML', 'Computer Vision'],
    prize: '1 000 000 ₸',
    backgroundImage: '/images/event1.jpg'
  },
  {
    id: 2,
    title: 'Mobile Dev Hack',
    type: 'hackathons',
    status: 'active',
    date: '2025-03-17',
    participants: 96,
    tags: ['React Native', 'Flutter', 'Mobile'],
    prize: '500 000 ₸',
    backgroundImage: '/images/event2.jpg'
  },
  {
    id: 3,
    title: 'GameDev Hackathon',
    type: 'hackathons',
    status: 'upcoming',
    date: '2025-03-25',
    participants: 64,
    tags: ['Unity', 'Unreal Engine', 'C#'],
    prize: '750 000 ₸',
    backgroundImage: '/images/event3.jpg'
  },
  {
    id: 4,
    title: 'Web3 Hack',
    type: 'hackathons',
    status: 'upcoming',
    date: '2025-03-30',
    participants: 80,
    tags: ['Blockchain', 'Smart Contracts', 'DeFi'],
    prize: '800 000 ₸',
    backgroundImage: '/images/event4.jpg'
  },

  // Вебинары
  {
    id: 5,
    title: 'Web3 Development',
    type: 'webinars',
    status: 'active',
    date: '2025-03-17',
    participants: 256,
    tags: ['Blockchain', 'Smart Contracts'],
    speaker: 'Виталик Бутерин',
    backgroundImage: '/images/event5.jpg'
  },
  {
    id: 6,
    title: 'Cloud Computing',
    type: 'webinars',
    status: 'upcoming',
    date: '2025-03-22',
    participants: 180,
    tags: ['AWS', 'Azure', 'DevOps'],
    speaker: 'Джефф Безос',
    backgroundImage: '/images/event6.jpg'
  },
  {
    id: 7,
    title: 'Machine Learning',
    type: 'webinars',
    status: 'upcoming',
    date: '2025-03-24',
    participants: 150,
    tags: ['Python', 'TensorFlow', 'Deep Learning'],
    speaker: 'Ян ЛеКун',
    backgroundImage: '/images/event7.jpg'
  },
  {
    id: 8,
    title: 'Mobile Development',
    type: 'webinars',
    status: 'upcoming',
    date: '2025-03-26',
    participants: 120,
    tags: ['iOS', 'Android', 'Cross-platform'],
    speaker: 'Крис Латтнер',
    backgroundImage: '/images/event8.jpg'
  },

  // Кейс-чемпионаты
  {
    id: 9,
    title: 'Green Energy Case',
    type: 'cases',
    status: 'upcoming',
    date: '2025-03-25',
    participants: 64,
    tags: ['Sustainability', 'Innovation'],
    company: 'GreenTech',
    backgroundImage: '/images/event9.jpg'
  },
  {
    id: 10,
    title: 'FinTech Innovation',
    type: 'cases',
    status: 'active',
    date: '2025-03-19',
    participants: 75,
    tags: ['Finance', 'Blockchain', 'AI'],
    company: 'Tinkoff',
    backgroundImage: '/images/event10.jpg'
  },
  {
    id: 11,
    title: 'Smart City',
    type: 'cases',
    status: 'upcoming',
    date: '2025-03-28',
    participants: 90,
    tags: ['IoT', 'Big Data', 'Urban Planning'],
    company: 'Siemens',
    backgroundImage: '/images/event11.jpg'
  },
  {
    id: 12,
    title: 'E-commerce Future',
    type: 'cases',
    status: 'upcoming',
    date: '2025-03-31',
    participants: 85,
    tags: ['Retail', 'Digital Marketing', 'UX'],
    company: 'Ozon',
    backgroundImage: '/images/event12.jpg'
  }
])

// Search and filter functionality
const searchQuery = ref('')
const selectedTags = ref([])

// Formatting functions
const formatDate = (date) => {
  const options = { day: 'numeric', month: 'long' }
  return new Date(date).toLocaleDateString('ru-RU', options)
}

const formatNotificationTime = (time) => {
  const now = new Date()
  const diff = now - new Date(time)
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days} д. назад`
  if (hours > 0) return `${hours} ч. назад`
  if (minutes > 0) return `${minutes} мин. назад`
  return 'только что'
}

const formatStatus = (status) => {
  const statusMap = {
    'upcoming': 'Скоро',
    'active': 'Идет сейчас',
    'finished': 'Завершен'
  }
  return statusMap[status] || status
}

// Event filtering and search
const isFilteredOut = (event) => {
  const query = searchQuery.value.toLowerCase()
  const tags = selectedTags.value
  
  const matchesQuery = event.title.toLowerCase().includes(query) ||
                      event.type.toLowerCase().includes(query) ||
                      event.tags.some(tag => tag.toLowerCase().includes(query))
  
  const matchesTags = tags.length === 0 || 
                     tags.every(tag => event.tags.includes(tag))
  
  return !(matchesQuery && matchesTags)
}

const filterEvents = () => {
  return events.value.filter(event => !isFilteredOut(event))
}

// Color functions
const getEventTypeColor = (type) => {
  const colors = {
    hackathons: '#6366F1',
    webinars: '#10B981',
    cases: '#F59E0B'
  }
  return colors[type] || '#6B7280'
}

const getNewsColor = (type) => {
  const colors = {
    announcement: '#6366F1',
    update: '#2ECC71',
    event: '#F59E0B'
  }
  return colors[type] || '#6B7280'
}

// Navigation and interaction
const navigateToEvent = (id) => {
  router.push(`/hackathons/${id}`)
}

const openNews = (news) => {
  // Implement news opening logic
}

const viewAllNews = () => {
  // Implement view all news logic
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
}

const closeNotifications = () => {
  showNotifications.value = false
}

// Helper functions
const getRandomDelay = () => {
  return Math.random() * 0.3 // Случайная задержка до 0.3 секунды
}

// User data and functions
const user = ref({
  name: 'Сейтжанов Темирлан',
  level: 42,
  rating: 1250,
  avatar: null,
  achievements: ['🏆', '⭐', '🚀']
})

const getAvatarColor = () => {
  const colors = ['#3498db', '#f1c40f', '#2ecc71', '#e74c3c', '#9b59b6', '#1abc9c']
  const hash = user.value.name.split('').reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc)
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const getUserInitials = () => {
  const name = user.value.name
  return name.split(' ').map(word => word[0]).join('')
}

// Computed property for filtered events
const filteredEvents = computed(() => {
  if (!searchQuery.value && selectedTags.value.length === 0) {
    return events.value
  }
  return filterEvents()
})

// Events by category
const getEventsByCategory = (categoryId) => {
  return events.value.filter(event => event.type === categoryId)
}

// Filter events by category
const filteredEventsByCategory = computed(() => {
  const events = filteredEvents.value
  if (activeCategory.value === 'all') return events
  return events.filter(event => event.type === activeCategory.value.slice(0, -1))
})

// Get all unique tags
const allTags = computed(() => {
  const tags = new Set()
  events.value.forEach(event => {
    event.tags.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

// News
const newsItems = ref([
  {
    id: 1,
    type: 'announcement',
    title: 'Открыт набор на AI Хакатон 2025',
    description: 'Регистрация участников открыта до 19 марта. Призовой фонд составляет 1 000 000 ₸',
    date: '2025-03-15',
    image: '/images/ai-hackathon.jpg',
    likes: 42,
    isLiked: false,
    isFavorite: false,
    hasDeadline: true,
    hasReminder: false,
    deadline: '2025-03-19'
  },
  {
    id: 2,
    type: 'update',
    title: 'Обновление платформы',
    description: 'Добавлены новые функции: уведомления в Telegram, улучшенный поиск и фильтрация',
    date: '2025-03-16',
    image: null,
    likes: 28,
    isLiked: false,
    isFavorite: false,
    hasDeadline: false
  },
  {
    id: 3,
    type: 'event',
    title: 'Встреча победителей Web3 хакатона',
    description: 'Приглашаем на networking-сессию с презентацией проектов и обсуждением перспектив',
    date: '2025-03-20',
    image: '/images/web3-meetup.jpg',
    likes: 35,
    isLiked: false,
    isFavorite: false,
    hasDeadline: true,
    hasReminder: false,
    deadline: '2025-03-20'
  }
])

const newsFilters = [
  { label: 'Все', value: 'all' },
  { label: 'Анонсы', value: 'announcement' },
  { label: 'Обновления', value: 'update' },
  { label: 'События', value: 'event' }
]

const currentNewsFilter = ref('all')
const newsSearchQuery = ref('')

const filteredNews = computed(() => {
  let filtered = newsItems.value

  // Apply type filter
  if (currentNewsFilter.value !== 'all') {
    filtered = filtered.filter(news => news.type === currentNewsFilter.value)
  }

  // Apply search filter
  if (newsSearchQuery.value) {
    const query = newsSearchQuery.value.toLowerCase()
    filtered = filtered.filter(news => 
      news.title.toLowerCase().includes(query) || 
      news.description.toLowerCase().includes(query)
    )
  }

  return filtered
})

const getNewsIcon = (type) => {
  const icons = {
    announcement: '📢',
    update: '🔄',
    event: '🎉'
  }
  return icons[type] || '📄'
}

const getNewsTypeLabel = (type) => {
  const labels = {
    announcement: 'Анонс',
    update: 'Обновление',
    event: 'Событие'
  }
  return labels[type]
}

const toggleLike = (newsId) => {
  const news = newsItems.value.find(n => n.id === newsId)
  if (news) {
    if (news.isLiked) {
      news.likes--
    } else {
      news.likes++
    }
    news.isLiked = !news.isLiked
  }
}

const openComments = (news) => {
  // Implement comments opening logic
}

const shareNews = (news) => {
  // Implementation for sharing functionality
  const url = `${window.location.origin}/news/${news.id}`
  navigator.clipboard.writeText(url)
    .then(() => {
      // Show success message
    })
    .catch(() => {
      // Show error message
    })
}

const openNewsDetails = (news) => {
  router.push(`/news/${news.id}`)
}

// Notifications
const showNotifications = ref(false)
const activeCategory = ref('all')
const notifications = ref([
  {
    id: 1,
    type: 'success',
    text: 'Вы успешно зарегистрировались на хакатон AI Challenge 2025!',
    time: '2025-03-17T05:30:00',
    read: false
  },
  {
    id: 2,
    type: 'info',
    text: 'Новый вебинар по Web3 начнется через 2 часа',
    time: '2025-03-17T05:40:00',
    read: false
  },
  {
    id: 3,
    type: 'warning',
    text: 'Срок регистрации на кейс-чемпионат заканчивается завтра',
    time: '2025-03-17T05:45:00',
    read: true
  }
])

const unreadNotificationsCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
  }
}

// Scroll functionality
const categoryScrollRefs = ref({})
const categoryScrollStates = ref({})

const updateCategoryScrollState = (categoryId) => {
  const container = categoryScrollRefs.value[categoryId]
  if (!container) return
  
  categoryScrollStates.value[categoryId] = {
    canScrollLeft: container.scrollLeft > 0,
    canScrollRight: container.scrollLeft < (container.scrollWidth - container.clientWidth)
  }
}

const canScrollLeft = (categoryId) => categoryScrollStates.value[categoryId]?.canScrollLeft
const canScrollRight = (categoryId) => categoryScrollStates.value[categoryId]?.canScrollRight

const scrollCategory = (direction, categoryId) => {
  const container = categoryScrollRefs.value[categoryId]
  if (!container) return
  
  const scrollAmount = container.clientWidth * 0.8
  const targetScroll = container.scrollLeft + (direction === 'right' ? scrollAmount : -scrollAmount)
  
  container.scrollTo({
    left: targetScroll,
    behavior: 'smooth'
  })
}

// Event type styles
const getEventTypeStyle = (type) => {
  const colors = {
    hackathons: '#6366F1',
    webinars: '#10B981',
    cases: '#F59E0B'
  }
  return { backgroundColor: colors[type] }
}

const getEventTypeLabel = (type) => {
  const labels = {
    hackathons: 'Хакатон',
    webinars: 'Вебинар',
    cases: 'Кейс'
  }
  return labels[type]
}

// Status labels
const getStatusLabel = (status) => {
  const labels = {
    active: 'Идет сейчас',
    upcoming: 'Скоро',
    finished: 'Завершен'
  }
  return labels[status]
}

// Default background images
const getDefaultBackground = (type) => {
  const backgrounds = {
    hackathons: '/images/default-hackathon.jpg',
    webinars: '/images/default-webinar.jpg',
    cases: '/images/default-case.jpg'
  }
  return backgrounds[type] || backgrounds.hackathons
}

// Lifecycle hooks
onMounted(() => {
  Object.keys(categoryScrollRefs.value).forEach(categoryId => {
    const container = categoryScrollRefs.value[categoryId]
    if (container) {
      updateCategoryScrollState(categoryId)
      container.addEventListener('scroll', () => updateCategoryScrollState(categoryId))
    }
  })
})
</script>

<style scoped>
:root {
  --background-color: #ffffff;
  --surface-color: #f3f4f6;
  --surface-color-hover: #e5e7eb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --primary-color: #6366f1;
  --border-color: #e5e7eb;
}

[data-theme="dark"] {
  --background-color: #111827;
  --surface-color: #1f2937;
  --surface-color-hover: #374151;
  --text-primary: #f9fafb;
  --text-secondary: #9ca3af;
  --primary-color: #818cf8;
  --border-color: #374151;
}

.home-view {
  padding: 20px;
  margin-bottom: 70px; /* Для мобильной навигации */
  background-color: var(--background-color);
  min-height: calc(100vh - 70px);
}

@media (min-width: 768px) {
  .home-view {
    margin-top: 70px; /* Для десктопной навигации */
    margin-bottom: 0;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  border-radius: 12px;
  background: var(--surface-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info h2 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
}

.notifications-wrapper {
  position: relative;
}

.notifications-button {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: var(--text-primary);
  border-radius: 8px;
  transition: background-color 0.2s;
}

.notifications-button:hover {
  background: var(--surface-color-hover);
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #EF4444;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--surface-color);
}

.notifications-popup {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 320px;
  background: var(--surface-color);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
  border: 1px solid var(--border-color);
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.notifications-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.notifications-header button {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  color: var(--text-secondary);
  border-radius: 4px;
}

.notifications-header button:hover {
  background: var(--surface-color-hover);
  color: var(--text-primary);
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem;
}

.notification-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background: var(--surface-color-hover);
}

.notification-item.unread {
  background: var(--surface-color-hover);
}

.notification-icon {
  padding: 0.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-icon.success {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.notification-icon.info {
  background: rgba(99, 102, 241, 0.1);
  color: #6366F1;
}

.notification-icon.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #F59E0B;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-content p {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notification-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.events-section {
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.events-container {
  position: relative;
  margin: 0 -20px; /* Компенсируем паддинг контейнера для полной ширины */
  padding: 0 20px;
}

@media (min-width: 768px) {
  .events-container {
    margin: 0;
    padding: 0;
  }

  .event-card {
    flex: 0 0 300px;
  }

  .scroll-button {
    display: flex;
  }
}

.events-scroll {
  overflow-x: auto;
  scroll-behavior: smooth;
  -ms-overflow-style: none;
  scrollbar-width: none;
  padding: 0.5rem 0;
  margin: 0 -0.5rem; /* Компенсируем паддинг сетки */
}

.events-scroll::-webkit-scrollbar {
  display: none;
}

.events-grid {
  display: flex;
  gap: 1rem;
  padding: 0 0.5rem;
}

.scroll-button {
  display: none; /* Скрываем кнопки на мобильных */
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--surface-color);
  border: none;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  z-index: 1;
  color: var(--text-primary);
}

.scroll-button:hover {
  background: var(--surface-color-hover);
}

.scroll-button.left {
  left: -8px;
}

.scroll-button.right {
  right: -8px;
}

.event-card {
  position: relative;
  width: 100%;
  min-width: 280px;
  max-width: 400px;
  height: 320px;
  border-radius: 12px;
  overflow: hidden;
  background: var(--card-bg);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
  }
}

.event-image {
  position: relative;
  width: 100%;
  height: 160px;
  background-size: cover;
  background-position: center;
}

.event-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%);
  padding: 16px;
}

.event-content {
  padding: 16px;
  background: var(--card-bg);
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.event-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9);

  &.upcoming {
    color: var(--color-info);
  }

  &.active {
    color: var(--color-success);
  }

  &.ended {
    color: var(--color-error);
  }
}

.event-content h3 {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-primary);
}

.event-info {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 14px;
  color: var(--text-secondary);

  span {
    display: flex;
    align-items: center;
    gap: 4px;

    svg {
      color: var(--text-tertiary);
    }
  }
}

.event-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;

  .tag {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    background: var(--tag-bg);
    color: var(--text-secondary);
  }
}

.event-prize {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-success);

  svg {
    color: var(--color-success);
  }
}

@media (min-width: 768px) {
  .event-card {
    min-width: 320px;
  }
}

.news-section {
  margin-top: 2rem;
}

.news-filters {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: var(--surface-color);
  color: var(--text-secondary);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.filter-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.news-search {
  margin: 1rem 0;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--surface-color);
  color: var(--text-primary);
}

.news-list {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.news-card {
  background: var(--surface-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.news-image {
  height: 200px;
  overflow: hidden;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  background: var(--surface-variant);
}

.news-content {
  padding: 1rem;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.news-type {
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.75rem;
  font-weight: 500;
}

.news-type.announcement {
  background: #4A90E2;
  color: white;
}

.news-type.update {
  background: #2ECC71;
  color: white;
}

.news-type.event {
  background: #F39C12;
  color: white;
}

.news-date {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.news-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.4;
  color: var(--text-primary);
}

.news-content p {
  margin: 0 0 1rem 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-secondary);
}

.news-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: none;
  background: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--surface-variant);
}

.action-btn.like-btn {
  color: #666;
}

.action-btn.like-btn:hover {
  color: #ff4b4b;
}

.action-btn.like-btn.active {
  color: #ff4b4b;
}

.action-btn.like-btn.active svg {
  fill: currentColor;
}

.action-btn svg {
  transition: all 0.2s ease;
}

.action-btn .count {
  font-size: 0.875rem;
  min-width: 1rem;
}

.details-btn {
  margin-left: auto;
  padding: 0.5rem 1rem;
  border: none;
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.details-btn:hover {
  background: var(--primary-color-dark);
}

@media (max-width: 768px) {
  .news-list {
    grid-template-columns: 1fr;
  }
  
  .news-card {
    max-width: none;
  }
}
</style>