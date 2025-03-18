<template>
  <div class="hackathon-detail">
    <div class="banner-container">
      <img :src="hackathon?.details?.banner_image || 'https://via.placeholder.com/1200x400'" alt="Banner" class="banner-image" />
      <div class="banner-overlay">
        <h1>{{ hackathon?.title || 'Название хакатона' }}</h1>
        <div class="header-info">
          <span class="status-badge" :class="hackathon?.status">{{ getStatusIcon(hackathon?.status) }} {{ getStatusText(hackathon?.status) }}</span>
          <span class="type-badge">{{ getFormatText(hackathon?.type) }}</span>
          <span class="participants-badge">👥 {{ hackathon?.participants_info?.current_participants || 0 }}/{{ hackathon?.participants_info?.max_participants || '∞' }}</span>
        </div>
      </div>
    </div>

    <div class="hackathon-content">
      <div v-if="canRegister" class="section">
        <button class="action-btn primary full-width" @click="openRegistrationModal">Регистрация</button>
      </div>
      <div v-else class="section">
        <p v-if="!isAuthenticated">Пожалуйста, войдите в систему, чтобы зарегистрироваться.</p>
        <p v-else-if="missingRequiredFields">Заполните все обязательные поля в профиле (имя, телефон, дата рождения).</p>
        <p v-else-if="hackathon?.is_participant">Вы уже зарегистрированы на этот хакатон.</p>
        <p v-else-if="hackathon?.status !== 'registration'">Регистрация на этот хакатон закрыта.</p>
        <p v-else-if="hackathon?.participants_info?.max_participants && hackathon?.participants_info.current_participants >= hackathon?.participants_info.max_participants">Достигнут лимит участников.</p>
        <p v-else>Период регистрации истёк.</p>
      </div>

      <div class="tabs">
        <button v-for="tab in tabs" :key="tab.id" :class="{ 'tab-btn': true, 'active': currentTab === tab.id }" @click="currentTab = tab.id">
          <span class="tab-icon">{{ tab.icon }}</span> {{ tab.name }}
        </button>
      </div>

      <div class="section" v-if="currentTab === 'about'">
        <h2>📝 О хакатоне</h2>
        <p>{{ hackathon?.details?.full_description || 'Описание отсутствует' }}</p>
      </div>

      <div class="section" v-if="currentTab === 'prizes'">
        <h2>🏆 Призы</h2>
        <div class="prizes-grid">
          <div v-for="prize in hackathon?.hackathon_prizes" :key="prize.place" class="prize-card">
            <span class="prize-medal">{{ getPrizeMedal(prize.place) }}</span>
            <div class="prize-value">{{ prize.prize_amount || 0 }}₸</div>
            <div class="xp-value">{{ prize.xp_reward }} XP</div>
          </div>
        </div>
      </div>

      <div class="section" v-if="currentTab === 'organizer'">
        <h2>🏢 Организатор</h2>
        <div class="organizer-card">
          <img :src="hackathon?.organization?.logo || 'https://via.placeholder.com/100'" alt="Logo" class="org-logo" />
          <div>
            <h3>{{ hackathon?.organization?.name }}</h3>
            <p>{{ hackathon?.organization?.description }}</p>
            <div class="org-links">
              <a :href="hackathon?.organization?.website" target="_blank" class="org-link">🌐 Сайт</a>
              <a :href="hackathon?.organization?.telegram" target="_blank" class="org-link">📩 Telegram</a>
            </div>
          </div>
        </div>
      </div>

      <div class="section" v-if="currentTab === 'rules'">
        <h2>📜 FAQ и Правила</h2>
        <div v-html="formatFAQ(hackathon?.details?.faq)"></div>
        <div v-html="formatRules(hackathon?.details?.rules)"></div>
      </div>

      <div class="section" v-if="currentTab === 'registration'">
        <h2>✍️ Регистрация</h2>
        <p v-if="canRegister">Регистрация открыта до {{ formatDate(hackathon?.schedule?.registration_end_date) }}</p>
        <p v-else>Регистрация закрыта или вы уже участвуете.</p>
      </div>
    </div>

    <!-- Модальное окно -->
    <div v-if="showRegistrationModal" class="modal-overlay" @click.self="closeRegistrationModal">
      <div class="modal-content">
        <h2>Регистрация</h2>
        <div v-if="isLoading" class="loading-state">
          <div class="loader"></div>
          <p>Регистрация...</p>
        </div>
        <div v-else-if="showSuccess" class="message-card">
          <span class="message-icon">✅</span>
          <p>{{ successMessage }}</p>
          <button class="action-btn primary" @click="closeRegistrationModal">Закрыть</button>
        </div>
        <div v-else-if="!registrationStep">
          <div class="registration-options">
            <button class="option-btn" @click="registerAsSolo">Одиночная регистрация</button>
            <button class="option-btn" @click="registerAsTeam">Создать команду</button>
            <button class="option-btn" @click="joinTeamModal">Присоединиться к команде</button>
          </div>
        </div>
        <div v-else-if="registrationStep === 'create-team'">
          <div class="create-team-form">
            <label>Название команды</label>
            <input v-model="teamName" placeholder="Введите название" @input="updateTeamCode" />
            <div v-if="teamName" class="team-code">
              <p>Код для приглашения участников:</p>
              <div class="code-display">
                {{ generatedTeamCode }}
                <button class="copy-btn" @click="copyCode">📋</button>
              </div>
            </div>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <button class="submit-btn" @click="createTeam">Создать</button>
          </div>
        </div>
        <div v-else-if="registrationStep === 'join-team'">
          <div class="team-code-input">
            <label>Код команды</label>
            <input v-model="joinCode" placeholder="Введите код" />
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <button class="submit-btn" @click="joinTeam">Присоединиться</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useHackathonStore } from '../stores/hackathon';
import { useAuthStore } from '../stores/auth';

export default {
  data() {
    return {
      showRegistrationModal: false,
      registrationStep: '',
      teamName: '',
      joinCode: '',
      generatedTeamCode: '', // Реактивная переменная для кода команды
      errorMessage: '',
      currentTab: 'about',
      tabs: [
        { id: 'about', name: 'О хакатоне', icon: '📝' },
        { id: 'prizes', name: 'Призы', icon: '🏆' },
        { id: 'organizer', name: 'Организатор', icon: '🏢' },
        { id: 'rules', name: 'FAQ и Правила', icon: '📜' },
        { id: 'registration', name: 'Регистрация', icon: '✍️' }
      ],
      isLoading: false,
      showSuccess: false,
      successMessage: '',
      userLoaded: false
    };
  },
  computed: {
    hackathon() {
      const hackathonStore = useHackathonStore();
      return hackathonStore.currentHackathon;
    },
    isAuthenticated() {
      const authStore = useAuthStore();
      console.log('Token:', authStore.token);
      return !!authStore.token;
    },
    user() {
      const authStore = useAuthStore();
      return authStore.user;
    },
    missingRequiredFields() {
      if (!this.userLoaded) return true;
      const missing = !this.user?.first_name || !this.user?.phone_number || !this.user?.birth_date;
      console.log('Missing required fields:', {
        first_name: this.user?.first_name,
        phone_number: this.user?.phone_number,
        birth_date: this.user?.birth_date,
        result: missing
      });
      return missing;
    },
    canRegister() {
      if (!this.hackathon || !this.isAuthenticated || this.missingRequiredFields) {
        console.log('Initial checks failed:', {
          hackathon: !!this.hackathon,
          isAuthenticated: this.isAuthenticated,
          missingRequiredFields: this.missingRequiredFields
        });
        return false;
      }
      const now = new Date();
      const regEnd = new Date(this.hackathon.schedule?.registration_end_date);
      
      const nowUTC = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds());
      const regEndUTC = Date.UTC(regEnd.getUTCFullYear(), regEnd.getUTCMonth(), regEnd.getUTCDate(), regEnd.getUTCHours(), regEnd.getUTCMinutes(), regEnd.getUTCSeconds());

      console.log('Now (UTC):', new Date(nowUTC));
      console.log('Registration end date (UTC):', new Date(regEndUTC));
      console.log('Can register:', {
        status: this.hackathon.status === 'registration',
        dateCheck: nowUTC <= regEndUTC,
        participantsCheck: !this.hackathon.participants_info?.max_participants || 
          this.hackathon.participants_info.current_participants < this.hackathon.participants_info.max_participants,
        isParticipant: !this.hackathon.is_participant
      });

      return (
        this.hackathon.status === 'registration' &&
        nowUTC <= regEndUTC &&
        (!this.hackathon.participants_info?.max_participants || 
         this.hackathon.participants_info.current_participants < this.hackathon.participants_info.max_participants) &&
        !this.hackathon.is_participant
      );
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return 'Не указано';
      return new Date(date).toLocaleDateString('ru-RU', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    },
    getStatusText(status) {
      const statusMap = { 
        'archived': 'Архив', 
        'anounce': 'Анонс', 
        'registration': 'Регистрация', 
        'in_progress': 'В процессе', 
        'finished': 'Завершен', 
        'results_announced': 'Результаты объявлены' 
      };
      return statusMap[status] || status;
    },
    getStatusIcon(status) {
      const iconMap = { 
        'archived': '📦', 
        'anounce': '📢', 
        'registration': '✍️', 
        'in_progress': '🔥', 
        'finished': '🏁', 
        'results_announced': '📊' 
      };
      return iconMap[status] || '❓';
    },
    getFormatText(type) {
      const formatMap = { 'online': 'Онлайн 💻', 'offline': 'Офлайн 🏢', 'hybrid': 'Гибрид 🔄' };
      return formatMap[type] || type;
    },
    getPrizeMedal(place) {
      const medals = { 1: '🥇', 2: '🥈', 3: '🥉' };
      return medals[place] || '🏅';
    },
    formatFAQ(faq) {
      return faq ? faq.split('\n').map(line => `<p>${line}</p>`).join('') : '<p>FAQ отсутствует</p>';
    },
    formatRules(rules) {
      return rules ? rules.split('\n').map(line => `<p>${line}</p>`).join('') : '<p>Правила отсутствуют</p>';
    },
    openRegistrationModal() {
      this.showRegistrationModal = true;
      this.registrationStep = '';
      this.errorMessage = '';
      this.showSuccess = false;
    },
    closeRegistrationModal() {
      this.showRegistrationModal = false;
      this.registrationStep = '';
      this.teamName = '';
      this.joinCode = '';
      this.generatedTeamCode = ''; // Сбрасываем код
      this.errorMessage = '';
      this.showSuccess = false;
    },
    async registerAsSolo() {
      this.isLoading = true;
      try {
        const hackathonStore = useHackathonStore();
        const response = await hackathonStore.registerForHackathon(this.$route.params.id);
        this.successMessage = response.detail;
        this.showSuccess = true;
      } catch (error) {
        this.errorMessage = error.detail || 'Ошибка при регистрации';
      } finally {
        this.isLoading = false;
      }
    },
    registerAsTeam() {
      this.registrationStep = 'create-team';
      this.generatedTeamCode = this.generateTeamCode(); // Генерируем код при открытии формы
    },
    joinTeamModal() {
      this.registrationStep = 'join-team';
    },
    generateTeamCode() {
      // Генерируем уникальный код команды
      return 'TEAM' + Math.random().toString(36).substring(2, 8).toUpperCase();
    },
    updateTeamCode() {
      // Обновляем код при изменении названия команды
      if (this.teamName) {
        this.generatedTeamCode = this.generateTeamCode();
      } else {
        this.generatedTeamCode = '';
      }
    },
    async createTeam() {
      if (!this.teamName) {
        this.errorMessage = 'Укажите название команды';
        return;
      }
      this.isLoading = true;
      try {
        const hackathonStore = useHackathonStore();
        const response = await hackathonStore.createTeam(this.$route.params.id, this.teamName, this.generatedTeamCode);
        this.successMessage = response.detail;
        this.showSuccess = true;
      } catch (error) {
        this.errorMessage = error.detail || 'Ошибка при создании команды';
      } finally {
        this.isLoading = false;
      }
    },
    async joinTeam() {
      if (!this.joinCode) {
        this.errorMessage = 'Укажите код команды';
        return;
      }
      this.isLoading = true;
      try {
        const hackathonStore = useHackathonStore();
        const response = await hackathonStore.joinTeam(this.$route.params.id, this.joinCode);
        this.successMessage = response.detail;
        this.showSuccess = true;
      } catch (error) {
        this.errorMessage = error.detail || 'Ошибка при присоединении';
      } finally {
        this.isLoading = false;
      }
    },
    copyCode() {
      if (!this.generatedTeamCode) return;
      navigator.clipboard.writeText(this.generatedTeamCode);
      this.successMessage = 'Код скопирован!';
    }
  },
  async created() {
    const hackathonStore = useHackathonStore();
    const authStore = useAuthStore();
    await hackathonStore.fetchHackathonDetail(this.$route.params.id);
    if (this.isAuthenticated && !this.user) {
      await authStore.fetchUser();
    }
    this.userLoaded = true;
    console.log('User data:', this.user);
    console.log('Hackathon data:', this.hackathon);
  }
};
</script>

<style scoped>
.hackathon-detail {
  min-height: 100vh;
  background: #1a1a1a;
}

.banner-container {
  position: relative;
  height: 400px;
  overflow: hidden;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
}

.banner-overlay h1 {
  font-size: 42px;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.header-info {
  display: flex;
  gap: 20px;
  align-items: center;
}

.status-badge, .type-badge, .participants-badge {
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  backdrop-filter: blur(5px);
}

.status-badge {
  background: rgba(0, 191, 255, 0.2);
}

.status-badge.registration {
  background: rgba(46, 213, 115, 0.8);
}

.status-badge.in_progress {
  background: rgba(255, 71, 87, 0.8);
}

.hackathon-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: rgba(0, 191, 255, 0.1);
  color: #ccc;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.tab-btn:hover {
  background: rgba(0, 191, 255, 0.2);
  color: #fff;
}

.tab-btn.active {
  background: #00BFFF;
  color: white;
}

.tab-icon {
  font-size: 20px;
}

.section {
  background: rgba(42, 52, 53, 0.7);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
}

.section h2 {
  font-size: 24px;
  color: #00BFFF;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.prizes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.prize-card {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease;
}

.prize-card:hover {
  transform: translateY(-5px);
}

.prize-medal {
  font-size: 40px;
  margin-bottom: 15px;
}

.prize-value {
  font-size: 24px;
  color: #00BFFF;
  margin: 10px 0;
}

.xp-value {
  color: #FFD700;
}

.organizer-card {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.org-logo {
  width: 100px;
  height: 100px;
  border-radius: 15px;
  object-fit: cover;
}

.org-links {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.org-link {
  padding: 8px 16px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 20px;
  color: #00BFFF;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.org-link:hover {
  background: rgba(0, 191, 255, 0.2);
  transform: translateY(-2px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: rgba(42, 52, 53, 0.7);
  border-radius: 15px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.3s ease;
  color: #fff;
}

.modal-content h2 {
  margin: 0 0 24px;
  color: #00BFFF;
  font-size: 24px;
}

.registration-options {
  display: grid;
  gap: 16px;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(0, 191, 255, 0.1);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-btn:hover {
  background: rgba(0, 191, 255, 0.2);
  transform: translateY(-2px);
}

.team-code-input,
.create-team-form {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.team-code-input label,
.create-team-form label {
  color: #ccc;
  font-size: 14px;
}

.team-code-input input,
.create-team-form input {
  padding: 12px;
  border: 1px solid rgba(0, 191, 255, 0.2);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-size: 16px;
}

.team-code-input input:focus,
.create-team-form input:focus {
  outline: none;
  border-color: #00BFFF;
}

.team-code {
  margin-top: 10px;
}

.code-display {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 10px;
  font-family: monospace;
  font-size: 16px;
  color: #00BFFF;
}

.copy-btn {
  padding: 4px;
  background: transparent;
  border: none;
  color: #ccc;
  cursor: pointer;
  transition: color 0.2s ease;
}

.copy-btn:hover {
  color: #00BFFF;
}

.submit-btn {
  margin-top: 12px;
  padding: 12px 24px;
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.submit-btn:hover {
  background: linear-gradient(45deg, #0099cc, #007acc);
}

.message-card {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  margin-bottom: 20px;
}

.message-icon {
  font-size: 40px;
  margin-bottom: 15px;
  display: block;
  animation: bounce 0.5s ease;
}

.action-btn {
  padding: 12px 24px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.action-btn.primary {
  background: linear-gradient(45deg, #00BFFF, #0099cc);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 191, 255, 0.2);
}

.full-width {
  width: 100%;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #ccc;
}

.loader {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 191, 255, 0.1);
  border-top-color: #00BFFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.error {
  color: #ff4757;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

@media (max-width: 768px) {
  .banner-container {
    height: 300px;
  }
  
  .banner-overlay {
    padding: 20px;
  }
  
  .banner-overlay h1 {
    font-size: 28px;
  }
  
  .header-info {
    flex-direction: column;
    gap: 10px;
  }
  
  .tabs {
    flex-wrap: nowrap;
    overflow-x: auto;
  }
  
  .organizer-card {
    flex-direction: column;
    text-align: center;
  }
  
  .org-logo {
    margin: 0 auto;
  }
  
  .org-links {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>