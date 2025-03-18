<template>
  <div class="tracks-tab">
    <!-- Статистика треков -->
    <div class="stats-section">
      <div class="stat-item">
        <h4>Всего треков</h4>
        <p>{{ tracks.length }}</p>
      </div>
      <div class="stat-item">
        <h4>Участников</h4>
        <p>{{ totalParticipants }}</p>
      </div>
    </div>

    <!-- Список треков -->
    <div class="tracks-list">
      <div v-for="track in tracks" :key="track.id" class="track-card">
        <div class="track-header">
          <div class="track-icon">{{ track.icon }}</div>
          <h3>{{ track.name }}</h3>
        </div>

        <p class="track-description">{{ track.description }}</p>

        <div class="track-stack">
          <h4>Рекомендуемый стек:</h4>
          <div class="stack-tags">
            <span v-for="tech in track.stack" :key="tech" class="tech-tag">
              {{ tech }}
            </span>
          </div>
        </div>

        <div class="track-stats">
          <div class="track-stat">
            <span>Участников:</span>
            <strong>{{ track.participants }}</strong>
          </div>
          <div class="track-stat">
            <span>Команд:</span>
            <strong>{{ track.teams }}</strong>
          </div>
        </div>

        <div class="track-actions">
          <button class="details-btn" @click="showTrackDetails(track)">
            Подробнее
          </button>
          <button 
            v-if="!track.isSelected" 
            class="select-btn"
            @click="selectTrack(track)"
          >
            Выбрать трек
          </button>
          <span v-else class="selected-badge">
            Выбран
          </span>
        </div>
      </div>
    </div>

    <!-- Модальное окно с деталями трека -->
    <div v-if="selectedTrack" class="modal-overlay" @click.self="selectedTrack = null">
      <div class="modal-content">
        <div class="track-modal-header">
          <div class="track-icon-large">{{ selectedTrack.icon }}</div>
          <h2>{{ selectedTrack.name }}</h2>
        </div>

        <div class="track-modal-section">
          <h3>Описание</h3>
          <p>{{ selectedTrack.description }}</p>
        </div>

        <div class="track-modal-section">
          <h3>Рекомендуемый стек</h3>
          <div class="stack-tags">
            <span v-for="tech in selectedTrack.stack" :key="tech" class="tech-tag">
              {{ tech }}
            </span>
          </div>
        </div>

        <div class="track-modal-section">
          <h3>Ресурсы и примеры</h3>
          <div class="resources-list">
            <div v-for="(resource, index) in selectedTrack.resources" :key="index" class="resource-item">
              <div class="resource-icon">📚</div>
              <div class="resource-info">
                <h4>{{ resource.title }}</h4>
                <p>{{ resource.description }}</p>
                <a :href="resource.link" target="_blank" rel="noopener noreferrer">
                  Открыть ресурс
                </a>
              </div>
            </div>
          </div>
        </div>

        <div class="track-modal-section">
          <h3>Статистика</h3>
          <div class="modal-stats">
            <div class="modal-stat-item">
              <span class="stat-label">Участников</span>
              <strong>{{ selectedTrack.participants }}</strong>
            </div>
            <div class="modal-stat-item">
              <span class="stat-label">Команд</span>
              <strong>{{ selectedTrack.teams }}</strong>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="cancel-btn" @click="selectedTrack = null">
            Закрыть
          </button>
          <button 
            v-if="!selectedTrack.isSelected"
            class="submit-btn"
            @click="selectTrack(selectedTrack)"
          >
            Выбрать трек
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Моковые данные
const tracks = ref([
  {
    id: 1,
    name: 'AI & Machine Learning',
    icon: '🧠',
    description: 'Создание решений на основе искусственного интеллекта и машинного обучения. Участники этого трека будут работать над проектами, использующими современные методы ИИ для решения реальных задач.',
    stack: ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn'],
    participants: 45,
    teams: 12,
    isSelected: false,
    resources: [
      {
        title: 'Введение в Machine Learning',
        description: 'Базовый курс по машинному обучению с примерами на Python',
        link: '#'
      },
      {
        title: 'TensorFlow Tutorial',
        description: 'Практическое руководство по работе с TensorFlow',
        link: '#'
      }
    ]
  },
  {
    id: 2,
    name: 'Web3 & Blockchain',
    icon: '⛓️',
    description: 'Разработка децентрализованных приложений и смарт-контрактов. Изучение и применение технологий блокчейн для создания инновационных решений.',
    stack: ['Solidity', 'Web3.js', 'Ethereum', 'React'],
    participants: 30,
    teams: 8,
    isSelected: false,
    resources: [
      {
        title: 'Основы Blockchain',
        description: 'Фундаментальные принципы работы блокчейна',
        link: '#'
      },
      {
        title: 'Smart Contracts с Solidity',
        description: 'Руководство по разработке смарт-контрактов',
        link: '#'
      }
    ]
  }
]);

// Вычисляемые свойства
const totalParticipants = computed(() => {
  return tracks.value.reduce((sum, track) => sum + track.participants, 0);
});

// Добавляем новую переменную состояния
const selectedTrack = ref(null);

// Методы
const showTrackDetails = (track) => {
  selectedTrack.value = track;
};

const selectTrack = (track) => {
  tracks.value = tracks.value.map(t => ({
    ...t,
    isSelected: t.id === track.id
  }));
};
</script>

<style scoped>
.tracks-tab {
  padding: 20px;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-item {
  background: var(--surface-variant);
  padding: 20px;
  border-radius: var(--radius-lg);
  text-align: center;
}

.stat-item h4 {
  color: var(--text-secondary);
  margin: 0 0 10px;
  font-size: 14px;
}

.stat-item p {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.tracks-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.track-card {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s;
}

.track-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.track-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

.track-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-variant);
  border-radius: var(--radius-md);
}

.track-header h3 {
  margin: 0;
  font-size: 18px;
}

.track-description {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.track-stack {
  margin-bottom: 20px;
}

.track-stack h4 {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 10px;
}

.stack-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  font-size: 12px;
  padding: 4px 8px;
  background: var(--surface-variant);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.track-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.track-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.track-stat span {
  font-size: 12px;
  color: var(--text-secondary);
}

.track-stat strong {
  font-size: 16px;
  color: var(--text-primary);
}

.track-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.details-btn, .select-btn {
  padding: 8px 16px;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.details-btn {
  background: var(--surface-variant);
  color: var(--text-primary);
}

.details-btn:hover {
  background: var(--surface-hover);
}

.select-btn {
  background: var(--primary-color);
  color: white;
}

.select-btn:hover {
  background: var(--primary-color-dark);
}

.selected-badge {
  padding: 8px 16px;
  background: var(--primary-color-light);
  color: var(--primary-color);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
}

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
}

.modal-content {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}

.track-modal-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.track-icon-large {
  font-size: 32px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-variant);
  border-radius: var(--radius-lg);
}

.track-modal-header h2 {
  margin: 0;
  font-size: 28px;
}

.track-modal-section {
  margin-bottom: 24px;
}

.track-modal-section h3 {
  font-size: 18px;
  margin: 0 0 16px;
  color: var(--text-secondary);
}

.track-modal-section p {
  margin: 0;
  line-height: 1.6;
  color: var(--text-primary);
}

.resources-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resource-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--surface-variant);
  border-radius: var(--radius-md);
}

.resource-icon {
  font-size: 24px;
}

.resource-info {
  flex: 1;
}

.resource-info h4 {
  margin: 0 0 8px;
  font-size: 16px;
}

.resource-info p {
  margin: 0 0 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.resource-info a {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.resource-info a:hover {
  text-decoration: underline;
}

.modal-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.modal-stat-item {
  text-align: center;
  padding: 16px;
  background: var(--surface-variant);
  border-radius: var(--radius-md);
}

.stat-label {
  display: block;
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.modal-stat-item strong {
  font-size: 24px;
  color: var(--text-primary);
}

.modal-actions {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.modal-actions button {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: var(--surface-variant);
  color: var(--text-primary);
}

.cancel-btn:hover {
  background: var(--surface-hover);
}

.submit-btn {
  background: var(--primary-color);
  color: white;
}

.submit-btn:hover {
  background: var(--primary-color-dark);
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: 1fr;
  }

  .tracks-list {
    grid-template-columns: 1fr;
  }
}
</style>
