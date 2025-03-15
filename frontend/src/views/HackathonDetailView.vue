<template>
    <div class="hackathon-detail">
      <div v-if="hackathon" class="hackathon-header">
        <div class="banner-container">
          <img
            :src="hackathon.details.banner_image || hackathon.details.preview_image"
            alt="Hackathon Banner"
            class="banner-image"
          />
          <div class="banner-overlay">
            <h1>{{ hackathon.title }}</h1>
            <div class="header-info">
              <div class="status-badge" :class="hackathon.status">
                {{ getStatusText(hackathon.status) }}
                <span class="status-icon">{{ getStatusIcon(hackathon.status) }}</span>
              </div>
              <div class="type-badge">
                {{ getFormatText(hackathon.type) }}
              </div>
              <div class="participants-badge">
                <span class="icon">👥</span>
                {{ hackathon.participants_info.participants_count }}/{{ hackathon.participants_info.max_participants || '∞' }}
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <div v-if="hackathon" class="hackathon-content">
        <div class="tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['tab-btn', { active: currentTab === tab.id }]"
            @click="currentTab = tab.id"
          >
            <span class="tab-icon">{{ tab.icon }}</span>
            {{ tab.name }}
          </button>
        </div>
  
        <div class="tab-content">
          <!-- Вкладка "О хакатоне" -->
          <div v-if="currentTab === 'about'" class="tab-pane">
            <section class="section description-section">
              <h2>📝 Описание</h2>
              <p>{{ hackathon.full_description || hackathon.details.full_description || 'Описание отсутствует' }}</p>
            </section>
  
            <section class="section schedule-section">
              <h2>📅 Расписание</h2>
              <div class="timeline">
                <div class="timeline-item">
                  <div class="timeline-icon">📋</div>
                  <div class="timeline-content">
                    <h3>Регистрация</h3>
                    <p>{{ formatDate(hackathon.schedule.registration_start_date) }} - {{ formatDate(hackathon.schedule.registration_end_date) }}</p>
                  </div>
                </div>
                <div class="timeline-item">
                  <div class="timeline-icon">🚀</div>
                  <div class="timeline-content">
                    <h3>Хакатон</h3>
                    <p>{{ formatDate(hackathon.schedule.start_date) }} - {{ formatDate(hackathon.schedule.end_date) }}</p>
                  </div>
                </div>
              </div>
            </section>
  
            <section v-if="hackathon.type !== 'online'" class="section location-section">
              <h2>�� Место проведения</h2>
              <div class="location-card">
                <span class="location-icon">🏢</span>
                <div class="location-info">
                  <p class="location-name">{{ hackathon.location || 'Не указано' }}</p>
                  <p class="location-address">{{ hackathon.address || 'Адрес не указан' }}</p>
                </div>
              </div>
            </section>
          </div>
  
          <!-- Вкладка "Призы" -->
          <div v-if="currentTab === 'prizes'" class="tab-pane">
            <section class="section prizes-section">
              <div class="prize-header">
                <h2>🏆 Призовой фонд</h2>
                <div class="total-prize">
                  <span class="prize-amount">{{ hackathon.total_prize_amount }}₸</span>
                  <span class="prize-places">{{ hackathon.total_prize_places }} призовых мест</span>
                </div>
              </div>
  
              <div class="prizes-grid">
                <div 
                  v-for="prize in hackathon.hackathon_prizes" 
                  :key="prize.place"
                  class="prize-card"
                  :class="'place-' + prize.place"
                >
                  <div class="prize-medal">
                    {{ getPrizeMedal(prize.place) }}
                  </div>
                  <div class="prize-details">
                    <h3>{{ prize.place }} место</h3>
                    <p class="prize-value">{{ prize.prize_amount }}₸</p>
                    <p class="xp-value">+{{ prize.xp_reward }} XP</p>
                    <p class="winners-count">{{ prize.number_of_winners }} победителей</p>
                  </div>
                </div>
              </div>
            </section>
          </div>
  
          <!-- Вкладка "Организатор" -->
          <div v-if="currentTab === 'organizer'" class="tab-pane">
            <section class="section organizer-section">
              <div class="organizer-card">
                <img 
                  v-if="hackathon.organization.logo"
                  :src="hackathon.organization.logo"
                  alt="Organization Logo"
                  class="org-logo"
                />
                <div class="org-info">
                  <h2>{{ hackathon.organization.name }}</h2>
                  <p>{{ hackathon.organization.description }}</p>
                  <div class="org-links">
                    <a v-if="hackathon.organization.website" :href="hackathon.organization.website" target="_blank" class="org-link">
                      <span class="link-icon">🌐</span> Сайт
                    </a>
                    <a v-if="hackathon.organization.telegram" :href="hackathon.organization.telegram" target="_blank" class="org-link">
                      <span class="link-icon">📱</span> Telegram
                    </a>
                    <a v-if="hackathon.organization.instagram" :href="hackathon.organization.instagram" target="_blank" class="org-link">
                      <span class="link-icon">📸</span> Instagram
                    </a>
                  </div>
                </div>
              </div>
            </section>
          </div>
  
          <!-- Вкладка "FAQ и Правила" -->
          <div v-if="currentTab === 'rules'" class="tab-pane">
            <section v-if="hackathon.details.faq" class="section faq-section">
              <h2>❓ FAQ</h2>
              <div class="faq-content" v-html="formatFAQ(hackathon.details.faq)"></div>
            </section>
  
            <section v-if="hackathon.details.rules" class="section rules-section">
              <h2>📜 Правила</h2>
              <div class="rules-content" v-html="formatRules(hackathon.details.rules)"></div>
            </section>
          </div>
  
          <!-- Вкладка "Регистрация" -->
          <div v-if="currentTab === 'registration'" class="tab-pane">
            <section class="section registration-section">
              <h2>✍️ Регистрация</h2>
              
              <div v-if="!isAuthenticated" class="auth-required">
                <div class="message-card">
                  <span class="message-icon">🔒</span>
                  <p>Пожалуйста, авторизуйтесь, чтобы зарегистрироваться.</p>
                  <router-link to="/" class="action-btn">Войти</router-link>
                </div>
              </div>
  
              <div v-else-if="hackathon.is_participant" class="already-registered">
                <div class="message-card success">
                  <span class="message-icon">✅</span>
                  <p>Вы уже зарегистрированы на этот хакатон!</p>
                </div>
              </div>
  
              <div v-else-if="hackathon.status !== 'registration'" class="registration-closed">
                <div class="message-card warning">
                  <span class="message-icon">⚠️</span>
                  <p>Регистрация на этот хакатон сейчас недоступна.</p>
                </div>
              </div>
  
              <div v-else-if="missingRequiredFields" class="missing-fields">
                <div class="message-card error">
                  <span class="message-icon">⚠️</span>
                  <p>Для участия необходимо заполнить профиль:</p>
                  <ul class="required-fields-list">
                    <li v-if="!user.first_name">• Имя</li>
                    <li v-if="!user.phone_number">• Номер телефона</li>
                    <li v-if="!user.birth_date">• Дата рождения</li>
                  </ul>
                  <router-link to="/profile/settings" class="action-btn">
                    Заполнить профиль
                  </router-link>
                </div>
              </div>
  
              <div v-else class="registration-form">
                <div v-if="hackathon.type === 'team' || hackathon.type === 'hybrid'" class="team-options">
                  <div class="option-card create-team">
                    <h3>🎯 Создать команду</h3>
                    <div class="input-group">
                      <input
                        v-model="teamName"
                        type="text"
                        placeholder="Название команды"
                        class="styled-input"
                      />
                      <button @click="createTeam" class="action-btn primary">
                        Создать команду 🚀
                      </button>
                    </div>
                    <div v-if="teamCreated" class="team-code">
                      <p>Код для приглашения участников:</p>
                      <div class="code-display">
                        {{ teamJoinCode }}
                        <button @click="copyCode" class="copy-btn">📋</button>
                      </div>
                    </div>
                  </div>
  
                  <div class="option-card join-team">
                    <h3>🤝 Присоединиться к команде</h3>
                    <div class="input-group">
                      <input
                        v-model="joinCode"
                        type="text"
                        placeholder="Введите код команды"
                        class="styled-input"
                      />
                      <button @click="joinTeam" class="action-btn secondary">
                        Присоединиться 🎯
                      </button>
                    </div>
                  </div>
                </div>
  
                <div v-if="hackathon.type === 'solo' || hackathon.type === 'hybrid'" class="solo-registration">
                  <div class="option-card">
                    <h3>👤 Индивидуальное участие</h3>
                    <button @click="registerSolo" class="action-btn primary full-width">
                      Зарегистрироваться 🚀
                    </button>
                  </div>
                </div>
  
                <div v-if="errorMessage" class="error-message">
                  <span class="error-icon">❌</span>
                  {{ errorMessage }}
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
  
      <div v-else class="loading-state">
        <div class="loader"></div>
        <p>Загрузка хакатона... 🔄</p>
      </div>
    </div>
  </template>
  
  <script>
  import { useHackathonStore } from '../stores/hackathon';
  import { useAuthStore } from '../stores/auth';
  import { ref } from 'vue';
  
  export default {
    data() {
      return {
        showRegistrationForm: false,
        teamName: '',
        joinCode: '',
        teamCreated: false,
        teamJoinCode: '',
        errorMessage: '',
        currentTab: 'about',
        tabs: [
          { id: 'about', name: 'О хакатоне', icon: '📝' },
          { id: 'prizes', name: 'Призы', icon: '🏆' },
          { id: 'organizer', name: 'Организатор', icon: '🏢' },
          { id: 'rules', name: 'FAQ и Правила', icon: '📜' },
          { id: 'registration', name: 'Регистрация', icon: '✍️' }
        ]
      };
    },
    computed: {
      hackathon() {
        const hackathonStore = useHackathonStore();
        return hackathonStore.currentHackathon;
      },
      isAuthenticated() {
        const authStore = useAuthStore();
        return !!authStore.token;
      },
      user() {
        const authStore = useAuthStore();
        return authStore.user;
      },
      missingRequiredFields() {
        return !this.user.first_name || !this.user.phone_number || !this.user.birth_date;
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
          'finished': 'Завершен'
        };
        return statusMap[status] || status;
      },
      getStatusIcon(status) {
        const iconMap = {
          'archived': '📦',
          'anounce': '📢',
          'registration': '✍️',
          'in_progress': '🔥',
          'finished': '🏁'
        };
        return iconMap[status] || '❓';
      },
      getFormatText(type) {
        const formatMap = {
          'online': 'Онлайн 💻',
          'offline': 'Офлайн 🏢',
          'hybrid': 'Гибрид 🔄'
        };
        return formatMap[type] || type;
      },
      getPrizeMedal(place) {
        const medals = {
          1: '🥇',
          2: '🥈',
          3: '🥉'
        };
        return medals[place] || '🏅';
      },
      formatFAQ(faq) {
        return faq.split('\n').map(line => `<p>${line}</p>`).join('');
      },
      formatRules(rules) {
        return rules.split('\n').map(line => `<p>${line}</p>`).join('');
      },
      async registerSolo() {
        try {
          this.errorMessage = '';
          const hackathonStore = useHackathonStore();
          const response = await hackathonStore.registerForHackathon(this.$route.params.id);
          this.showSuccessMessage(response.detail);
          this.showRegistrationForm = false;
        } catch (error) {
          this.errorMessage = error.detail || 'Ошибка при регистрации';
        }
      },
      async createTeam() {
        try {
          this.errorMessage = '';
          if (!this.teamName) {
            this.errorMessage = 'Укажите название команды';
            return;
          }
          const hackathonStore = useHackathonStore();
          const response = await hackathonStore.createTeam(this.$route.params.id, this.teamName);
          this.teamCreated = true;
          this.teamJoinCode = response.team.join_code;
          this.showSuccessMessage(response.detail);
        } catch (error) {
          this.errorMessage = error.detail || 'Ошибка при создании команды';
        }
      },
      async joinTeam() {
        try {
          this.errorMessage = '';
          if (!this.joinCode) {
            this.errorMessage = 'Укажите код команды';
            return;
          }
          const hackathonStore = useHackathonStore();
          const response = await hackathonStore.joinTeam(this.$route.params.id, this.joinCode);
          this.showSuccessMessage(response.detail);
          this.showRegistrationForm = false;
        } catch (error) {
          this.errorMessage = error.detail || 'Ошибка при присоединении к команде';
        }
      },
      copyCode() {
        navigator.clipboard.writeText(this.teamJoinCode);
        this.showSuccessMessage('Код скопирован!');
      },
      showSuccessMessage(message) {
        alert(message);
      }
    },
    async created() {
      const hackathonStore = useHackathonStore();
      await hackathonStore.fetchHackathonDetail(this.$route.params.id);
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
  
  /* Timeline стили */
  .timeline {
    position: relative;
    padding: 20px 0;
  }
  
  .timeline-item {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .timeline-icon {
    width: 40px;
    height: 40px;
    background: rgba(0, 191, 255, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
  }
  
  .timeline-content h3 {
    color: #00BFFF;
    margin-bottom: 5px;
  }
  
  /* Призы стили */
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
  
  /* Организатор стили */
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
  
  /* Регистрация стили */
  .registration-form {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  
  .option-card {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 15px;
    padding: 25px;
  }
  
  .styled-input {
    width: 100%;
    padding: 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(0, 191, 255, 0.2);
    border-radius: 10px;
    color: white;
    margin-bottom: 15px;
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
  
  .action-btn.secondary {
    background: rgba(0, 191, 255, 0.1);
    color: #00BFFF;
  }
  
  .action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 191, 255, 0.2);
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
  }
  
  .error-message {
    color: #FF5555;
    padding: 15px;
    border-radius: 10px;
    background: rgba(255, 85, 85, 0.1);
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .team-code {
    margin-top: 20px;
    padding: 15px;
    background: rgba(0, 191, 255, 0.1);
    border-radius: 10px;
  }
  
  .code-display {
    font-family: monospace;
    font-size: 20px;
    color: #00BFFF;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }
  
  .copy-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 20px;
    padding: 5px;
    transition: transform 0.3s ease;
  }
  
  .copy-btn:hover {
    transform: scale(1.1);
  }
  
  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
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
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
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