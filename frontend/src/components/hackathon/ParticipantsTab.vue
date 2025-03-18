<template>
  <div class="participants-tab">
    <!-- Статистика -->
    <div class="stats-section">
      <div class="stat-item">
        <h4>Всего участников</h4>
        <p>{{ participants.length }}</p>
      </div>
      <div class="stat-item">
        <h4>Средний размер стека</h4>
        <p>{{ averageStackSize }}</p>
      </div>
    </div>

    <!-- Фильтры и сортировка -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по имени или стеку..."
        >
      </div>
      
      <div class="filter-group">
        <select v-model="teamFilter">
          <option value="">Все команды</option>
          <option value="with-team">В команде</option>
          <option value="no-team">Без команды</option>
        </select>

        <select v-model="sortBy">
          <option value="name">По имени</option>
          <option value="team">По команде</option>
          <option value="stack">По размеру стека</option>
        </select>

        <button 
          class="sort-direction-btn"
          @click="sortDirection = sortDirection === 'asc' ? 'desc' : 'asc'"
        >
          {{ sortDirection === 'asc' ? '↑' : '↓' }}
        </button>
      </div>
    </div>

    <!-- Список участников -->
    <div class="participants-list">
      <div 
        v-for="participant in filteredParticipants" 
        :key="participant.id"
        :class="['participant-card', { 'current-user': participant.isCurrentUser }]"
      >
        <div class="participant-header">
          <div class="participant-info">
            <h3>{{ participant.name }}</h3>
            <span class="team-badge" :class="participant.status">
              {{ participant.team || 'Без команды' }}
            </span>
          </div>
          <div class="participant-actions">
            <button 
              v-if="!participant.isCurrentUser && participant.status === 'no-team'"
              class="invite-btn"
              @click="inviteToTeam(participant)"
            >
              Пригласить в команду
            </button>
            <button 
              v-if="!participant.isCurrentUser"
              class="contact-btn"
              @click="contactParticipant(participant)"
            >
              Связаться
            </button>
          </div>
        </div>

        <div class="stack-section">
          <h4>Стек технологий:</h4>
          <div class="stack-tags">
            <span 
              v-for="tech in participant.stack" 
              :key="tech" 
              class="tech-tag"
            >
              {{ tech }}
            </span>
          </div>
        </div>

        <div class="participant-footer">
          <div class="role-badge">
            {{ participant.role }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Состояние фильтров и сортировки
const searchQuery = ref('');
const teamFilter = ref('');
const sortBy = ref('name');
const sortDirection = ref('asc');

// Моковые данные
const participants = ref([
  {
    id: 1,
    name: 'Алексей Иванов',
    team: 'CodeMasters',
    status: 'in-team',
    stack: ['Python', 'TensorFlow'],
    role: 'Разработчик',
    isCurrentUser: true
  },
  {
    id: 2,
    name: 'Мария Петрова',
    team: null,
    status: 'no-team',
    stack: ['JavaScript', 'Vue.js', 'Node.js'],
    role: 'Full-stack разработчик'
  },
  {
    id: 3,
    name: 'Дмитрий Сидоров',
    team: 'BlockchainPros',
    status: 'in-team',
    stack: ['Solidity', 'Web3.js', 'React'],
    role: 'Blockchain разработчик'
  }
]);

// Вычисляемые свойства
const averageStackSize = computed(() => {
  const total = participants.value.reduce((sum, p) => sum + p.stack.length, 0);
  return (total / participants.value.length).toFixed(1);
});

const filteredParticipants = computed(() => {
  let result = [...participants.value];

  // Применяем поиск
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(p => 
      p.name.toLowerCase().includes(query) ||
      p.stack.some(tech => tech.toLowerCase().includes(query))
    );
  }

  // Применяем фильтр по команде
  if (teamFilter.value) {
    result = result.filter(p => 
      teamFilter.value === 'with-team' ? p.team : !p.team
    );
  }

  // Применяем сортировку
  result.sort((a, b) => {
    let compareResult = 0;
    
    switch (sortBy.value) {
      case 'name':
        compareResult = a.name.localeCompare(b.name);
        break;
      case 'team':
        compareResult = (a.team || '').localeCompare(b.team || '');
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
const inviteToTeam = (participant) => {
  console.log('Приглашение в команду:', participant.name);
};

const contactParticipant = (participant) => {
  console.log('Связаться с участником:', participant.name);
};
</script>

<style scoped>
.participants-tab {
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

.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 30px;
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-box input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--surface-color);
  color: var(--text-primary);
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-group select {
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--surface-color);
  color: var(--text-primary);
}

.sort-direction-btn {
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--surface-color);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.sort-direction-btn:hover {
  background: var(--surface-hover);
}

.participants-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.participant-card {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s;
}

.participant-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.participant-card.current-user {
  border: 2px solid var(--primary-color);
}

.participant-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.participant-info h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.team-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
}

.team-badge.in-team {
  background: #4CAF50;
  color: white;
}

.team-badge.no-team {
  background: var(--surface-variant);
  color: var(--text-secondary);
}

.participant-actions {
  display: flex;
  gap: 8px;
}

.invite-btn,
.contact-btn {
  padding: 8px 12px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.invite-btn {
  background: var(--primary-color);
  color: white;
}

.invite-btn:hover {
  background: var(--primary-color-dark);
}

.contact-btn {
  background: var(--surface-variant);
  color: var(--text-primary);
}

.contact-btn:hover {
  background: var(--surface-hover);
}

.stack-section {
  margin-bottom: 15px;
}

.stack-section h4 {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 8px;
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

.participant-footer {
  display: flex;
  justify-content: flex-end;
}

.role-badge {
  font-size: 12px;
  padding: 4px 8px;
  background: var(--surface-variant);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: 1fr;
  }

  .filters-section {
    flex-direction: column;
  }

  .filter-group {
    flex-wrap: wrap;
  }

  .participants-list {
    grid-template-columns: 1fr;
  }
}
</style>
