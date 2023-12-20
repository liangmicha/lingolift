<template>
  <div class="features-section">
    <h2>Features</h2>
    <ul>
      <li>Interactive Listening Exercises</li>
      <li>Two-Way Definition Learning</li>
      <li>Easy Note and Image Upload</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "FeaturesSection"
};
</script>

<style scoped>
.features-section {
  padding: 40px 20px; /* Add more padding */
  text-align: center; /* Center align the content */
  background-color: #ffffff; /* Optional: Change background color for contrast */
}

.features-section h2 {
  font-size: 2rem;
  color: var(--primary-color); /* Use primary color for header */
  margin-bottom: 30px; /* More space below the header */
}

.features-section ul {
  list-style-type: none; /* Remove bullet points */
  padding: 0;
  max-width: 800px; /* Set a max-width for better readability */
  margin: auto; /* Center align the list */
}

.features-section li {
  font-size: 1.4rem;
  color: #666; /* Subtle color for list items */
  margin-bottom: 20px; /* Space between list items */
}
</style>
