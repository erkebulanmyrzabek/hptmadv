<template>
  <div class="teams-tab">
    <!-- Статистика -->
    <div class="stats-section">
      <div class="stat-card" v-for="(stat, index) in stats" :key="index">
        <div class="stat-icon">{{ stat.icon }}</div>
        <div class="stat-content">
          <h3>{{ stat.label }}</h3>
          <p class="stat-value">{{ stat.value }}</p>
        </div>
      </div>
    </div>

    <!-- Фильтры и сортировка -->
    <div class="filters-section">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по названию или стеку..."
          @input="debounceSearch"
        />
      </div>
      <div class="filter-group">
        <div class="select-wrapper">
          <select v-model="statusFilter">
            <option value="">Все команды</option>
            <option value="open">Открытые для набора</option>
            <option value="closed">Набор закрыт</option>
          </select>
        </div>
        <div class="select-wrapper">
          <select v-model="sizeFilter">
            <option value="">Любой размер</option>
            <option value="small">Маленькие (2-3)</option>
            <option value="medium">Средние (4-5)</option>
            <option value="large">Большие (6+)</option>
          </select>
        </div>
        <div class="select-wrapper">
          <select v-model="sortBy">
            <option value="name">По названию</option>
            <option value="members">По количеству участников</option>
            <option value="stack">По размеру стека</option>
          </select>
        </div>
        <button
          class="sort-direction-btn"
          @click="sortDirection = sortDirection === 'asc' ? 'desc' : 'asc'"
        >
          {{ sortDirection === 'asc' ? '↑' : '↓' }}
        </button>
      </div>
    </div>

    <!-- Список команд -->
    <div class="teams-grid">
      <div v-for="team in filteredTeams" :key="team.id" class="team-card">
        <div class="team-header">
          <h3>{{ team.name }}</h3>
          <span class="team-size">{{ team.members.length }}/{{ team.maxMembers }}</span>
        </div>
        <div class="team-content">
          <div class="team-stack">
            <span v-for="tech in team.stack" :key="tech" class="tech-tag">{{ tech }}</span>
          </div>
          <div class="team-members">
            <div v-for="member in team.members" :key="member.id" class="member">
              {{ member.name }}
            </div>
          </div>
          <div class="team-status">
            {{ team.status === 'open' ? 'Открыта для набора' : 'Набор закрыт' }}
          </div>
        </div>
        <div class="team-actions">
          <button v-if="team.status === 'open'" @click="joinTeam(team.id)" class="join-btn">
            Присоединиться
          </button>
        </div>
      </div>
    </div>

    <!-- Кнопка создания команды -->
    <button @click="showCreateTeamModal = true" class="create-team-btn">
      Создать команду
    </button>

    <!-- Модальное окно создания команды -->
    <div v-if="showCreateTeamModal" class="modal">
      <div class="modal-content">
        <h2>Создание команды</h2>
        <form @submit.prevent="createTeam">
          <div class="form-group">
            <label>Название команды</label>
            <input v-model="newTeam.name" required />
          </div>
          <div class="form-group">
            <label>Максимальное количество участников</label>
            <input v-model.number="newTeam.maxMembers" type="number" min="2" max="10" required />
          </div>
          <div class="form-group">
            <label>Технологии</label>
            <div class="tech-selector">
              <button
                v-for="tech in availableTechnologies"
                :key="tech"
                type="button"
                @click="toggleTechnology(tech)"
                :class="{ active: newTeam.stack.includes(tech) }"
              >
                {{ tech }}
              </button>
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateTeamModal = false">Отмена</button>
            <button type="submit">Создать</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  teams: {
    type: Array,
    required: true,
    default: () => []
  }
});

// Состояние
const searchQuery = ref('');
const statusFilter = ref('');
const sizeFilter = ref('');
const sortBy = ref('name');
const sortDirection = ref('asc');
const showCreateTeamModal = ref(false);

// Новая команда
const newTeam = ref({
  name: '',
  maxMembers: 5,
  stack: []
});

// Доступные технологии
const availableTechnologies = [
  'Vue.js', 'React', 'Angular',
  'Node.js', 'Python', 'Java',
  'AI/ML', 'Web3', 'Mobile'
];

// Вычисляемые свойства
const stats = computed(() => [
  {
    icon: '👥',
    label: 'Всего команд',
    value: props.teams.length
  },
  {
    icon: '👤',
    label: 'Средний размер',
    value: Math.round(props.teams.reduce((acc, team) => acc + team.members.length, 0) / props.teams.length || 0)
  },
  {
    icon: '🎯',
    label: 'Открытых команд',
    value: props.teams.filter(team => team.status === 'open').length
  }
]);

const filteredTeams = computed(() => {
  let result = [...props.teams];

  // Поиск
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(team => 
      team.name.toLowerCase().includes(query) ||
      team.stack.some(tech => tech.toLowerCase().includes(query))
    );
  }

  // Фильтры
  if (statusFilter.value) {
    result = result.filter(team => team.status === statusFilter.value);
  }

  if (sizeFilter.value) {
    switch (sizeFilter.value) {
      case 'small':
        result = result.filter(team => team.members.length <= 3);
        break;
      case 'medium':
        result = result.filter(team => team.members.length > 3 && team.members.length <= 5);
        break;
      case 'large':
        result = result.filter(team => team.members.length > 5);
        break;
    }
  }

  // Сортировка
  result.sort((a, b) => {
    let compareResult = 0;
    
    switch (sortBy.value) {
      case 'name':
        compareResult = a.name.localeCompare(b.name);
        break;
      case 'members':
        compareResult = a.members.length - b.members.length;
        break;
      case 'stack':
        compareResult = a.stack.length - b.stack.length;
        break;
    }

    return sortDirection.value === 'asc' ? compareResult : -compareResult;
  });

  return result;
});

// Методы
const debounceSearch = (() => {
  let timeout = null;
  return () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      // Дебаунс поиска
    }, 300);
  };
})();

const toggleTechnology = (tech) => {
  const index = newTeam.value.stack.indexOf(tech);
  if (index === -1) {
    newTeam.value.stack.push(tech);
  } else {
    newTeam.value.stack.splice(index, 1);
  }
};

const createTeam = () => {
  const team = {
    id: Date.now(),
    name: newTeam.value.name,
    members: [{ id: 1, name: 'Текущий пользователь' }],
    stack: newTeam.value.stack,
    status: 'open',
    maxMembers: newTeam.value.maxMembers
  };
  
  emit('team-created', team);
  
  // Сброс формы
  newTeam.value = { name: '', maxMembers: 5, stack: [] };
  showCreateTeamModal.value = false;
};

const joinTeam = (teamId) => {
  emit('join-team', teamId);
};

// События
const emit = defineEmits(['team-created', 'join-team']);
</script>

<style scoped>
.teams-tab {
  padding: 20px;
  max-width: 100%;
  overflow-x: hidden;
}

/* Статистика */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: var(--surface-variant);
  border-radius: 10px;
  padding: 15px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 24px;
  margin-right: 15px;
}

.stat-content h3 {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  margin: 5px 0 0;
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

/* Фильтры */
.filters-section {
  margin-bottom: 30px;
}

.search-box {
  position: relative;
  margin-bottom: 15px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-box input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.select-wrapper {
  flex: 1;
  min-width: 150px;
}

.select-wrapper select {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: white;
  font-size: 14px;
}

.sort-direction-btn {
  padding: 10px 15px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: white;
  cursor: pointer;
}

/* Список команд */
.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.team-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.team-header {
  padding: 15px;
  background: var(--primary-color);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.team-header h3 {
  margin: 0;
  font-size: 18px;
}

.team-size {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 12px;
}

.team-content {
  padding: 15px;
}

.team-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
}

.tech-tag {
  background: var(--surface-variant);
  color: var(--text-secondary);
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 12px;
}

.team-members {
  margin-bottom: 15px;
}

.member {
  padding: 5px 0;
  border-bottom: 1px solid var(--border-color);
  font-size: 14px;
}

.team-status {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 15px;
}

.team-actions {
  padding: 0 15px 15px;
}

.join-btn {
  width: 100%;
  padding: 10px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.join-btn:hover {
  background: var(--primary-color-dark);
}

/* Кнопка создания команды */
.create-team-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 15px 25px;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s, background 0.2s;
  z-index: 10;
}

.create-team-btn:hover {
  background: var(--primary-color-dark);
  transform: translateY(-2px);
}

/* Модальное окно */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background: white;
  border-radius: 10px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.tech-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-selector button {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.tech-selector button.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.modal-actions button {
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}

.modal-actions button:first-child {
  background: white;
  border: 1px solid var(--border-color);
}

.modal-actions button:last-child {
  background: var(--primary-color);
  color: white;
  border: none;
}

/* Адаптивность */
@media (max-width: 768px) {
  .teams-tab {
    padding: 15px;
  }
  
  .stats-section {
    grid-template-columns: 1fr;
  }
  
  .filter-group {
    flex-direction: column;
  }
  
  .select-wrapper {
    width: 100%;
  }
  
  .teams-grid {
    grid-template-columns: 1fr;
  }
  
  .create-team-btn {
    bottom: 20px;
    right: 20px;
    padding: 12px 20px;
  }
}
</style>