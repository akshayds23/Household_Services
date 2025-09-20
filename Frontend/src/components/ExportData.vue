<template>
  <nav class="navbar navbar-expand-lg fade-in-up">
        <div class="container">
          <a class="navbar-brand" href="/service_professional_dashboard">Service Professional Dashboard : {{ customerName }}</a>
          <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <router-link class="nav-link" to="/service_professional_dashboard">Home</router-link>
              </li>
    
              <li class="nav-item">
                <router-link class="nav-link" to="/service_professional_dashboard/open_requests_service_professional">Open Requests</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/data_export">Export Data</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    <section class="container page-section fade-in-up">
      <h1 class="text-center">Service History Export</h1>
      <p class="text-muted text-center mb-4">Download your completed requests in a polished table for easy reporting.</p>
      <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>Customer Name</th>
            <th>Service Name</th>
            <th>Service Professional Name</th>
            <th>Date of Request</th>
            <th>Date of Completion</th>
            <th>Rating</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.customer_name">
            <td>{{ request.customer_name }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.service_professional_name }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.date_of_completion }}</td>
            <td>{{ request.rating }}</td>
            <td>{{ request.remarks }}</td>
          </tr>
        </tbody>
      </table>
      </div>
      <div class="d-flex justify-content-center mt-4">
        <button @click="exportData" class="btn btn-primary">Export Data</button>
      </div>
    </section>
</template>

<script>
export default {
  data() {
    return {
      requests: [],
      customerName: ''
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    async logout() {
      const response = await fetch('http://127.0.0.1:5000/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}` },
        });
        this.$router.push('/');
    },
    async getData() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/closed_requests`,{
          method : 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
              'Content-Type': 'application/json'
          }
        })
        const data = await response.json()
        console.log(data)
        this.requests = data.closed_requests
        this.customerName = data.customer_name
      } catch (error) {
        console.error('Error:', error)
      }
    },
    async exportData() {
      const response = await fetch(`http://127.0.0.1:5000/data_export`,{
          method : 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
              'Content-Type': 'application/json'
          }
        })
        const data = await response.json()
        this.$router.push('/service_professional_dashboard')
        console.log(data)
    }
  }
}
</script>
