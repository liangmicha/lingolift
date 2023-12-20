<template>
  <header>
    <img class="logo" src="@/assets/logo.png" alt="LingoLift Logo" />
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
        <li><router-link to="/contact">Contact</router-link></li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: "AppHeader"
};
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

nav ul {
  list-style: none;
  display: flex;
}

nav ul li {
  margin: 0 10px;
  font-size: 1.2rem; /* Larger text size for accessibility */
}

.logo {
  width: 50px; /* Adjust size as needed */
  height: auto;
}
</style>
