<template>
  <div class="hero-section">
    <h1>Welcome to LingoLift!</h1>
    <p>Your journey to language mastery starts here.</p>
    <button @click="goToListening">Listening</button>
    <button @click="goToVocabulary">Vocabulary</button>
  </div>
</template>

<script>
export default {
  name: "HeroSection",
  methods: {
    goToListening() {
      this.$router.push('/listening');
    },
    goToVocabulary() {
      this.$router.push('/vocabulary');
    }
  }
};
</script>

<style scoped>
.hero-section {
  text-align: center;
  padding: 50px 20px;
  background-color: #e9e9e9; /* Light background for the section */
}

.hero-section h1 {
  font-size: 2.5rem;
  color: var(--primary-color); /* Using primary color for the heading */
}

.hero-section p {
  font-size: 1.5rem;
  color: #666; /* Subtle color for paragraph */
}

</style>
