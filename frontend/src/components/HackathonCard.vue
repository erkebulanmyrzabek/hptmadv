<template>
    <div class="hackathon-card">
      <img
        :src="hackathon.preview_image || 'https://via.placeholder.com/300x150'"
        alt="Hackathon Preview"
        class="hackathon-image"
      />
      <div class="hackathon-content">
        <h3>{{ hackathon.title }}</h3>
        <p class="description">{{ hackathon.short_description || 'Описание отсутствует' }}</p>
        <div class="info">
          <span class="status" :class="hackathon.status">{{ hackathon.status }}</span>
          <span class="type">{{ hackathon.type }}</span>
        </div>
        <div class="stats">
          <span>Участники: {{ hackathon.participants_count }}/{{ hackathon.max_participants || '∞' }}</span>
          <span>Призовых мест: {{ hackathon.total_prize_places }}</span>
          <span>Призовой фонд: {{ hackathon.total_prize_amount }}₸</span>
        </div>
        <router-link :to="`/hackathons/${hackathon.id}`" class="details-btn">Подробнее</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      hackathon: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .hackathon-card {
    background-color: #2A3435;
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.3s;
  }
  
  .hackathon-card:hover {
    transform: translateY(-5px);
  }
  
  .hackathon-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
  }
  
  .hackathon-content {
    padding: 15px;
  }
  
  h3 {
    font-size: 18px;
    margin: 0 0 10px;
    color: #fff;
  }
  
  .description {
    font-size: 14px;
    color: #ccc;
    margin-bottom: 10px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .info {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .status {
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    text-transform: capitalize;
  }
  
  .status.anounce {
    background-color: #FFD700;
    color: #000;
  }
  
  .status.registration {
    background-color: #00FF00;
    color: #000;
  }
  
  .status.in_progress {
    background-color: #1E90FF;
    color: #fff;
  }
  
  .status.finished {
    background-color: #FF4500;
    color: #fff;
  }
  
  .status.archived {
    background-color: #808080;
    color: #fff;
  }
  
  .type {
    font-size: 12px;
    color: #ccc;
  }
  
  .stats {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 12px;
    color: #ccc;
    margin-bottom: 15px;
  }
  
  .details-btn {
    display: inline-block;
    padding: 8px 16px;
    background-color: #00BFFF;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
    text-align: center;
    transition: background-color 0.3s;
  }
  
  .details-btn:hover {
    background-color: #009ACD;
  }
  </style>