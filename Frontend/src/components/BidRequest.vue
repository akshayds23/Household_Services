<template>
  <section class="container page-section compact fade-in-up">
    <h1 class="text-center">Bid Request</h1>
    <form @submit.prevent="submitBid" class="mt-4">
      <div class="mb-3">
        <label for="description" class="form-label">Share your proposal</label>
        <textarea
          class="form-control"
          id="description"
          rows="4"
          v-model="description"
          placeholder="Highlight your expertise, availability, and estimated cost."
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit Bid</button>
    </form>
    <div v-if="errorMessage" class="error-message mt-3">{{ errorMessage }}</div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      description: '',
      requestId: this.$route.params.requestId,
      errorMessage: null
    }
  },
  methods: {
    async submitBid() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/service_professional_dashboard/bid_request/${this.requestId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            description: this.description
          })
        });
        const result = await response.json();

        if (!response.ok) {
          this.errorMessage = result.message || 'An error occurred';
        } else {
          alert('Bid submitted successfully');
          this.$router.push('/service_professional_dashboard');
        }
      } catch (error) {
        console.error('Fetch error:', error);
        this.errorMessage = 'Unable to connect to the server';
      }
    }
  }
}
</script>
