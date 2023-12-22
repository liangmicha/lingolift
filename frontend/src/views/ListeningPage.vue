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
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progressBarWidth + '%' }"></div>
    </div>
    <div v-if="flashcards.length > 0">
      <div class="flashcard" @keyup.enter="isCorrectAnswer !== null ? moveToNextFlashcard() : checkTranslation()">
        <button class="play-audio-button" @click="playCurrentCardAudio">Play</button>

        <div v-if="showFeedback">
          <p class="feedback-message" :class="{ 'correct': isCorrectAnswer, 'incorrect': !isCorrectAnswer }">
            {{ isCorrectAnswer ? 'Correct!' : 'Incorrect!' }}
          </p>
          <p><strong>Learning Language:</strong> {{ flashcards[currentFlashcardIndex].learning_language_text }}</p>
          <p><strong>Fluent Language:</strong> {{ flashcards[currentFlashcardIndex].primary_language_text }}</p>
          <button @click="moveToNextFlashcard">Next</button>
        </div>

        <div v-else>
          <input type="text" 
            v-model="userTranslation" 
            @keyup.enter="checkTranslation" 
            placeholder="Type your translation">
          <button @click="checkTranslation">Check</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
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
const flashcards = ref([]);
const currentFlashcardIndex = ref(0);
const flashcardStatus = ref({ needsReview: [], reviewed: [] });
const userTranslation = ref('');
const isCorrectAnswer = ref(null);
const showFeedback = ref(false);

const progressBarWidth = computed(() => {
  const total = flashcards.length;
  const reviewed = flashcardStatus.value.reviewed.length;
  return (reviewed / total) * 100;
});

const playAudio = async (phrase) => {
  try {
    const response = await axios.get(`/get-audio/${phrase}`, { responseType: 'blob' });
    const url = URL.createObjectURL(new Blob([response.data]));
    const audio = new Audio(url);
    audio.play();
  } catch (error) {
    console.error("Error fetching audio:", error);
  }
};

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
    const responseFlashcards = response.data.flashcards.flashcards;
    flashcards.value = responseFlashcards;
    flashcardStatus.value.needsReview = responseFlashcards.map((_, index) => index);
    currentFlashcardIndex.value = 0;

    // Play audio for the first flashcard
    if (flashcards.value.length > 0 && flashcards.value[0].learning_language_text) {
      playAudio(flashcards.value[0].learning_language_text);
    }
  } catch (error) {
    console.error('Error generating flashcards:', error);
  }
};

const checkTranslation = () => {
  const currentCard = flashcards.value[currentFlashcardIndex.value];
  const isCorrect = similarity(currentCard.primary_language_text, userTranslation.value) >= 0.95;
  isCorrectAnswer.value = isCorrect;
  showFeedback.value = true; // Show feedback after checking

  if (!isCorrect && !flashcardStatus.value.needsReview.includes(currentFlashcardIndex.value)) {
    flashcardStatus.value.needsReview.push(currentFlashcardIndex.value);
  }
};

function getEditDistance(a, b) {
  if (a.length === 0) return b.length; 
  if (b.length === 0) return a.length;

  const matrix = [];

  // Increment along the first column of each row
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }

  // Increment each column in the first row
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }

  // Fill in the rest of the matrix
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, Math.min(matrix[i][j - 1] + 1, matrix[i - 1][j] + 1));
      }
    }
  }

  return matrix[b.length][a.length];
}

function similarity(str1, str2) {
  const distance = getEditDistance(str1.toLowerCase(), str2.toLowerCase());
  const longestString = Math.max(str1.length, str2.length);
  return (longestString - distance) / longestString;
}

const moveToNextFlashcard = () => {
  // Find the next flashcard index in the 'Needs review' bucket
  const nextIndex = flashcardStatus.value.needsReview.find(index => index > currentFlashcardIndex.value);

  if (nextIndex !== undefined) {
    // If there's a next flashcard, move to it
    currentFlashcardIndex.value = nextIndex;
  } else if (flashcardStatus.value.needsReview.length > 0) {
    // If all flashcards after the current one are reviewed, start from the beginning
    currentFlashcardIndex.value = flashcardStatus.value.needsReview[0];
  } else {
    // Optional: Handle the case when all flashcards are reviewed
    console.log("All flashcards reviewed!");
    // You can reset the review process or provide a message to the user
  }

  // After updating the currentFlashcardIndex, play the audio
  const currentCard = flashcards.value[currentFlashcardIndex.value];
  if (currentCard && currentCard.learning_language_text) {
    showFeedback.value = false; // Hide feedback for the next card
    userTranslation.value = ''; // Clear input
    playCurrentCardAudio(); // Play audio for the new card
  }
};

const playCurrentCardAudio = () => {
  const currentCard = flashcards.value[currentFlashcardIndex.value];
  if (currentCard && currentCard.learning_language_text) {
    playAudio(currentCard.learning_language_text);
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

.flashcard {
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  margin-top: 20px;
}

.flashcard p {
  font-size: 1.5em;
  color: #333;
  margin-bottom: 15px;
}

.flashcard input {
  width: 80%;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 1em;
  border: 2px solid #ccc;
  border-radius: 4px;
}

.flashcard button {
  width: 100px;
  height: 40px;
  margin-left: 10px;
}

.play-audio-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  margin: 10px;
  cursor: pointer;
}

.correct-answer {
  border-color: green;
}

.incorrect-answer {
  border-color: red;
}

.feedback-message {
  font-size: 1.2em;
  margin: 10px 0;
}

.feedback-message.correct {
  color: green;
}

.feedback-message.incorrect {
  color: red;
}
</style>
