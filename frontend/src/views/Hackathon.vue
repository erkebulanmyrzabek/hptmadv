<template>
    <div class="hackathon-page">
      <h1>Хакатоны</h1>
      <div class="hackathon-list">
        <hackathon-card
          v-for="hackathon in hackathons"
          :key="hackathon.id"
          :hackathon="hackathon"
        />
        <p v-if="!hackathons.length" class="no-hackathons">Хакатоны пока недоступны.</p>
      </div>
    </div>
  </template>
  
  <script>
  import HackathonCard from '../components/HackathonCard.vue';
  import { useHackathonStore } from '../stores/hackathon';
  
  export default {
    components: { HackathonCard },
    computed: {
      hackathons() {
        const hackathonStore = useHackathonStore();
        return hackathonStore.hackathons;
      },
    },
    async created() {
      const hackathonStore = useHackathonStore();
      await hackathonStore.fetchHackathons();
    },
  };
  </script>
  
  <style scoped>
  .hackathon-page {
    padding: 20px;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #00BFFF;
  }
  
  .hackathon-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .no-hackathons {
    text-align: center;
    color: #ccc;
    font-size: 16px;
  }
  </style>