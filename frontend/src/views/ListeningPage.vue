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
    <button @click="generateFlashcards">Generate Flashcards</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
let baseURL = ''; // Default empty baseURL

// Check if the app is running locally or on Vercel
if (process.env.NODE_ENV === 'development') {
  // Running locally
  baseURL = 'http://localhost:5000'; // Set your local Flask server URL here
} else {
  // Running on Vercel (or other deployment)
  // Set the production server URL here
  // Example: baseURL = 'https://your-production-api-url.com'
}

// Set the baseURL for Axios
axios.defaults.baseURL = baseURL;

const userInput = ref('');
const learningLanguage = ref('pt'); // Default learning language
const primaryLanguage = ref('en'); // Default primary language

// const fetchAudio = async (phrase) => {
//   try {
//     const response = await axios.get(`http://localhost:5000/get-audio/${phrase}`, { responseType: 'blob' });
//     const url = URL.createObjectURL(new Blob([response.data]));
//     const audio = new Audio(url);
//     audio.play();
//   } catch (error) {
//     console.error("Error fetching audio:", error);
//   }
// };

const generateFlashcards = async () => {
  try {
    // Create a data object with the required fields
    const requestData = {
      text: userInput.value,
      learning_language: learningLanguage.value,
      primary_language: primaryLanguage.value,
    };

    const response = await axios.post('/api/process-notes', requestData);
    // Handle the response, such as updating flashcards data
    console.log(response.data);
  } catch (error) {
    console.error('Error generating flashcards:', error);
  }
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
