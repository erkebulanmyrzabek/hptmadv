<template>
  <div class="hackathon-details-view" :class="{ 'dark-theme': isDarkTheme }">
    <!-- Tabs Navigation -->
    <nav class="tabs-nav" ref="tabsNav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="setActiveTab(tab.id)"
      >
        <span class="tab-icon" v-html="tab.icon"></span>
        {{ tab.title }}
      </button>
    </nav>

    <!-- Tab Content -->
    <div class="tab-content">
      <GeneralInfo 
        v-if="activeTab === 'general'" 
        :hackathon="hackathonData"
        @openRegistration="openRegistrationModal"
      />
      <ParticipantsTab 
        v-if="activeTab === 'participants'" 
        :participants="hackathonData.participants || []"
      />
      <TeamsTab 
        v-if="activeTab === 'teams'" 
        :teams="hackathonData.teams || []"
        @team-created="handleTeamCreated"
        @join-team="handleJoinTeam"
      />
      <TracksTab 
        v-if="activeTab === 'tracks'" 
        :tracks="hackathonData.tracks || []"
      />
    </div>

    <!-- Registration Modal -->
    <div v-if="showRegistrationModal" class="modal-overlay" @click="closeRegistrationModal">
      <div class="modal-content" @click.stop>
        <h2>Регистрация на хакатон</h2>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <div v-if="!registrationStep" class="registration-options">
          <button class="option-btn team" @click="registerAsTeam">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span>Создать команду</span>
          </button>
          <button class="option-btn join" @click="joinTeam">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="8.5" cy="7" r="4"></circle>
              <line x1="20" y1="8" x2="20" y2="14"></line>
              <line x1="23" y1="11" x2="17" y2="11"></line>
            </svg>
            <span>Присоединиться к команде</span>
          </button>
        </div>
        <div v-if="registrationStep === 'join-team'" class="team-code-input">
          <label for="team-code">Введите код команды:</label>
          <input 
            type="text" 
            id="team-code" 
            v-model="teamCode"
            placeholder="Например: TEAM123"
            @input="clearError"
          />
          <button class="submit-btn" @click="submitTeamCode" :disabled="isJoiningTeam">
            {{ isJoiningTeam ? 'Присоединяемся...' : 'Присоединиться' }}
          </button>
        </div>
        <div v-if="registrationStep === 'create-team'" class="create-team-form">
          <label for="team-name">Название команды:</label>
          <input 
            type="text" 
            id="team-name" 
            v-model="teamName"
            placeholder="Введите название команды"
            @input="clearError"
          />
          <div v-if="generatedTeamCode" class="team-code">
            Код для приглашения участников:
            <div class="code-display">
              {{ generatedTeamCode }}
              <button type="button" class="copy-btn" @click="copyTeamCode">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="9" y="9" width="13" height="13" rx="2.18" ry="2.18"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
              </button>
            </div>
          </div>
          <button class="submit-btn" @click="submitTeamCreation" :disabled="isCreatingTeam">
            {{ isCreatingTeam ? 'Создаём...' : 'Создать команду' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GeneralInfo from '@/components/hackathon/GeneralInfo.vue'
import ParticipantsTab from '@/components/hackathon/ParticipantsTab.vue'
import TeamsTab from '@/components/hackathon/TeamsTab.vue'
import TracksTab from '@/components/hackathon/TracksTab.vue'
import apiClient from '@/api/axios'

const route = useRoute()
const router = useRouter()
const activeTab = ref('general')
const showRegistrationModal = ref(false)
const registrationStep = ref('')
const teamCode = ref('')
const teamName = ref('')
const generatedTeamCode = ref('')
const isDarkTheme = ref(false)
const hackathonData = ref({})
const errorMessage = ref('')
const isCreatingTeam = ref(false)
const isJoiningTeam = ref(false)

const tabs = [
  {
    id: 'general',
    title: 'Общая информация',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>'
  },
  {
    id: 'participants',
    title: 'Участники',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>'
  },
  {
    id: 'teams',
    title: 'Команды',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>'
  },
  {
    id: 'tracks',
    title: 'Треки',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>'
  }
]

const validateHackathonData = (data) => {
  const requiredFields = ['id', 'title', 'status', 'start_date', 'end_date', 'registration_start', 'location', 'prize_pool']
  requiredFields.forEach(field => {
    if (!(field in data)) {
      console.warn(`Хакатон не содержит обязательное поле ${field}:`, data)
    }
  })
  if (!Array.isArray(data.participants)) {
    console.warn('Поле participants должно быть массивом:', data.participants)
    data.participants = []
  }
  if (!Array.isArray(data.teams)) {
    console.warn('Поле teams должно быть массивом:', data.teams)
    data.teams = []
  }
  if (!Array.isArray(data.tracks)) {
    console.warn('Поле tracks должно быть массивом:', data.tracks)
    data.tracks = []
  }
  if (!Array.isArray(data.organizers)) {
    console.warn('Поле organizers должно быть массивом:', data.organizers)
    data.organizers = []
  }
  if (!Array.isArray(data.judges)) {
    console.warn('Поле judges должно быть массивом:', data.judges)
    data.judges = []
  }
  if (!Array.isArray(data.schedule)) {
    console.warn('Поле schedule должно быть массивом:', data.schedule)
    data.schedule = []
  }
  if (!Array.isArray(data.rules)) {
    console.warn('Поле rules должно быть массивом:', data.rules)
    data.rules = []
  }
}

const setActiveTab = (tabId) => {
  activeTab.value = tabId
}

const openRegistrationModal = () => {
  showRegistrationModal.value = true
  registrationStep.value = ''
}

const closeRegistrationModal = () => {
  showRegistrationModal.value = false
  registrationStep.value = ''
  teamCode.value = ''
  teamName.value = ''
  generatedTeamCode.value = ''
  errorMessage.value = ''
  isCreatingTeam.value = false
  isJoiningTeam.value = false
}

const clearError = () => {
  errorMessage.value = ''
}

const registerAsTeam = () => {
  registrationStep.value = 'create-team'
  generatedTeamCode.value = ''
}

const joinTeam = () => {
  registrationStep.value = 'join-team'
}

const copyTeamCode = () => {
  if (!generatedTeamCode.value) {
    console.warn('Попытка скопировать пустой код команды.')
    return
  }
  navigator.clipboard.writeText(generatedTeamCode.value)
    .then(() => {
      alert('Код скопирован!')
      console.log('Код команды скопирован:', generatedTeamCode.value)
    })
    .catch(err => {
      console.error('Ошибка при копировании кода:', err)
      alert('Не удалось скопировать код.')
    })
}

const submitTeamCode = async () => {
  if (!teamCode.value.trim()) {
    errorMessage.value = 'Введите код команды.'
    console.warn('Попытка присоединиться к команде без кода.')
    return
  }

  isJoiningTeam.value = true
  errorMessage.value = ''
  try {
    const response = await apiClient.post(`/api/hackathons/${route.params.id}/join-team/`, { teamCode: teamCode.value })
    console.log('Успешно присоединились к команде:', response.data)
    handleJoinTeam(response.data.id)
    closeRegistrationModal()
  } catch (error) {
    const errorMsg = error.response?.data?.error || 'Не удалось присоединиться к команде. Попробуйте позже.'
    errorMessage.value = errorMsg
    console.error('Ошибка при присоединении к команде:', errorMsg, error)
    if (error.response?.status === 401) {
      router.push('/login')
    }
  } finally {
    isJoiningTeam.value = false
  }
}

const submitTeamCreation = async () => {
  if (!teamName.value.trim()) {
    errorMessage.value = 'Введите название команды.'
    console.warn('Попытка создать команду без названия.')
    return
  }

  isCreatingTeam.value = true
  errorMessage.value = ''
  try {
    const response = await apiClient.post(`/api/hackathons/${route.params.id}/create-team/`, {
      name: teamName.value,
      stack: ['Unknown']
    })
    generatedTeamCode.value = response.data.invite_code
    console.log('Команда успешно создана:', response.data)
    handleTeamCreated(response.data)
  } catch (error) {
    const errorMsg = error.response?.data?.error || 'Не удалось создать команду. Попробуйте позже.'
    errorMessage.value = errorMsg
    console.error('Ошибка при создании команды:', errorMsg, error)
    if (error.response?.status === 401) {
      router.push('/login')
    }
  } finally {
    isCreatingTeam.value = false
  }
}

const handleTeamCreated = (team) => {
  if (!hackathonData.value.teams) {
    hackathonData.value.teams = []
  }
  hackathonData.value.teams.push(team)
  console.log('Команда добавлена в список:', team)
}

const handleJoinTeam = (teamId) => {
  console.log('Присоединились к команде с ID:', teamId)
  loadHackathonData()
}

const loadHackathonData = async () => {
  try {
    const response = await apiClient.get(`/api/hackathons/${route.params.id}/`)
    if (!response.data || typeof response.data !== 'object') {
      throw new Error('API вернуло некорректные данные: ожидался объект.')
    }
    hackathonData.value = response.data
    validateHackathonData(hackathonData.value)
    console.log('Данные хакатона загружены:', hackathonData.value)
  } catch (error) {
    console.error('Ошибка при загрузке данных хакатона:', error)
    if (error.response?.status === 401) {
      router.push('/login')
    }
    hackathonData.value = {}
  }
}

onMounted(() => {
  // Проверяем, авторизован ли пользователь
  const accessToken = localStorage.getItem('access_token')
  if (!accessToken) {
    console.warn('Пользователь не авторизован. Перенаправляем на страницу логина.')
    router.push('/login')
    return
  }
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
  loadHackathonData()
  if (route.hash === '#registration') {
    openRegistrationModal()
  }
})

watch(() => route.hash, (newHash) => {
  if (newHash === '#registration') {
    openRegistrationModal()
  }
})
</script>

<style scoped>
/* Стили остаются без изменений */
.hackathon-details-view {
  padding: 20px;
  margin-bottom: 70px;
  background: var(--surface-color);
}

@media (min-width: 768px) {
  .hackathon-details-view {
    margin-top: 70px;
    margin-bottom: 0;
  }
}

/* Tabs Navigation */
.tabs-nav {
  display: flex;
  gap: 8px;
  padding: 16px;
  margin: -20px -20px 20px;
  background: var(--surface-variant);
  border-bottom: 1px solid var(--border-color);
  overflow-x: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.tabs-nav::-webkit-scrollbar {
  display: none;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background: var(--surface-hover);
}

.tab-btn.active {
  background: var(--primary-color);
  color: white;
}

.tab-btn.active svg {
  color: white;
}

.tab-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-icon svg {
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.modal-content h2 {
  margin: 0 0 24px;
  font-size: 24px;
  color: var(--text-primary);
}

.error-message {
  color: var(--error-color);
  background: var(--error-color-light);
  padding: 12px;
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  font-size: 14px;
}

.registration-options {
  display: grid;
  gap: 16px;
  margin-bottom: 24px;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--surface-color);
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-btn:hover {
  background: var(--surface-variant);
  border-color: var(--primary-color);
}

.option-btn svg {
  width: 24px;
  height: 24px;
  color: var(--text-secondary);
}

.option-btn.team:hover {
  border-color: #3498DB;
}

.option-btn.join:hover {
  border-color: #9B59B6;
}

.team-code-input,
.create-team-form {
  margin-top: 24px;
}

.team-code-input label,
.create-team-form label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-size: 14px;
}

.team-code-input input,
.create-team-form input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--surface-color);
  color: var(--text-primary);
  font-size: 16px;
  margin-bottom: 16px;
}

.team-code-input input:focus,
.create-team-form input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.team-code {
  margin-bottom: 16px;
  color: var(--text-secondary);
  font-size: 14px;
}

.code-display {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  padding: 12px;
  background: var(--surface-variant);
  border-radius: var(--radius-md);
  font-family: monospace;
  font-size: 16px;
  color: var(--text-primary);
}

.copy-btn {
  padding: 8px;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: var(--surface-hover);
  color: var(--primary-color);
}

.copy-btn svg {
  width: 20px;
  height: 20px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--primary-color);
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background: var(--primary-color-dark);
}

.submit-btn:disabled {
  background: var(--text-tertiary);
  cursor: not-allowed;
}

/* Dark Theme */
.dark-theme {
  --surface-color: #1a1a1a;
  --surface-variant: #2d2d2d;
  --surface-hover: #333333;
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
  --text-tertiary: #808080;
  --border-color: #404040;
  --error-color: #ff5555;
  --error-color-light: #ff555522;
}
</style>