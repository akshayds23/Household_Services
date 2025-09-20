<template>
  <div class="container page-section compact fade-in-up">
    <h1 class="text-center">Close Request</h1>
    <form @submit.prevent="closeRequest">
      <div class="rating">
        <input type="radio" id="star5" name="rating" value="5" v-model="rating" />
        <label for="star5" title="5 stars" class="fa fa-star checked">⭐⭐⭐⭐⭐</label><br>
        <input type="radio" id="star4" name="rating" value="4" v-model="rating" />
        <label for="star4" title="4 stars" class="fa fa-star checked">⭐⭐⭐⭐</label><br>
        <input type="radio" id="star3" name="rating" value="3" v-model="rating" />
        <label for="star3" title="3 stars" class="fa fa-star checked">⭐⭐⭐</label><br>
        <input type="radio" id="star2" name="rating" value="2" v-model="rating" />
        <label for="star2" title="2 stars" class="fa fa-star checked">⭐⭐</label><br>
        <input type="radio" id="star1" name="rating" value="1" v-model="rating" />
        <label for="star1" title="1 star" class="fa fa-star checked">⭐</label>
      </div>
      <div class="mb-3">
        <label for="review" class="form-label">Review:</label>
        <textarea class="form-control" id="review" v-model="review" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Close Request</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: '',
      review: '',
      errorMessage: null,
      requestId: null
    };
  },
  mounted() {
    this.requestId = this.$route.params.service_request_id;
    console.log('Request ID in CloseRequest component:', this.service_request_id);
  },
  methods: {
    async closeRequest() {
      this.errorMessage = null;
      const payload = {
        rating: this.rating,
        review: this.review
      };

      console.log("Sending payload:", payload);
      console.log("Token:", localStorage.getItem('homeownerToken'));

      try {
        const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/close_request/${this.requestId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        console.log("Server response:", result);

        if (!response.ok) {
          this.errorMessage = result.message || 'An error occurred';
        } else {
          alert("Request closed successfully");
          this.resetForm();
          this.$router.push('/home_owner_dashboard');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    resetForm() {
      this.rating = null;
      this.review = '';
    }
  }
};
</script>

