<template>
  <div class="listening-page">
    <h1>Listening Exercises</h1>
    <textarea v-model="userInput" placeholder="Paste your notes here..."></textarea>
    
    <div class="dropdown-container">
      <div class="dropdown-group">
        <label for="learningLanguage">I'm Learning:</label>
        <select v-model="learningLanguage" id="learningLanguage">
          <option value="pt">Portuguese</option>
          <!-- Add other learning language options here -->
        </select>
      </div>
      
      <div class="dropdown-group">
        <label for="primaryLanguage">I'm Fluent In:</label>
        <select v-model="primaryLanguage" id="primaryLanguage">
          <option value="en">English</option>
          <!-- Add other primary language options here -->
        </select>
      </div>
    </div>

    <button @click="generateExercises">Generate learning exercises</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const userInput = ref('');
const learningLanguage = ref('pt'); // Default learning language
const primaryLanguage = ref('en'); // Default primary language

const fetchAudio = async (phrase) => {
  try {
    const response = await axios.get(`http://localhost:5000/get-audio/${phrase}`);
    console.log(response.data); // Handle the response here
  } catch (error) {
    console.error("Error fetching audio:", error);
  }
};

const generateExercises = async () => {
  console.log('Exercises generation initiated');
  // Call fetchAudio here, replace 'yourPhrase' with the actual phrase
  await fetchAudio('yourPhrase');
};

</script>

<style scoped>
.listening-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

textarea {
  width: 100%;
  min-height: 150px;
  margin: 10px 0;
}

.dropdown-container {
  display: flex;
  gap: 10px;
  margin: 10px 0;
}

.dropdown-group {
  flex: 1;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

select {
  width: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  background-color: white;
  font-size: 16px;
}

button {
  background-color: var(--primary-color);
  border: none;
  border-radius: 4px;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: var(--secondary-color);
}
</style>
