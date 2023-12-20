<template>
  <div class="landing-page">
    <HeroSection />
    <FeaturesSection />
    <PlaceholderForExercises />
  </div>
</template>

<script>
import HeroSection from '@/components/HeroSection.vue';
import FeaturesSection from '@/components/FeaturesSection.vue';
import PlaceholderForExercises from '@/components/PlaceholderForExercises.vue';

export default {
  name: 'LandingPage',
  components: {
    HeroSection,
    FeaturesSection,
    PlaceholderForExercises
  }
};
</script>

<style>
/* Specific styles for LandingPage */
</style>
