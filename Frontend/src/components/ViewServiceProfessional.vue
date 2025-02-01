<template>
    <div>
      <nav class="navbar navbar-expand-lg fade-in-up">
        <div class="container">
          <router-link class="navbar-brand" to="/admin_dashboard">Admin Dashboard</router-link>
          <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin_dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin_dashboard/search">Search</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/">Logout</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin_dashboard/summary">Summary</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <section class="container page-section fade-in-up">
        <div class="row justify-content-center text-center mb-4">
          <div class="col-lg-10">
            <h1>Service Professional Details</h1>
            <p class="text-muted">Review credentials and portfolio before approving or assigning new work.</p>
          </div>
        </div>
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">{{ customer.customer_name }}</h5>
                <span class="badge bg-primary">{{ customer.service }}</span>
              </div>
              <div class="card-body">
                <h6 class="card-subtitle mb-3 text-muted">Contact Information</h6>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between"><span>Phone Number</span><span>{{ customer.contact_phone }}</span></li>
                  <li class="list-group-item d-flex justify-content-between"><span>Address</span><span>{{ customer.address }}</span></li>
                  <li class="list-group-item d-flex justify-content-between"><span>Pincode</span><span>{{ customer.pincode }}</span></li>
                </ul>
              </div>
            </div>
            <div class="d-flex justify-content-center mt-4">
              <button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#viewFileModal">
                View Portfolio
              </button>
            </div>
          </div>
        </div>
      </section>
  
      <div class="modal fade" id="viewFileModal" tabindex="-1" aria-labelledby="viewFileModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="viewFileModalLabel">Portfolio</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <embed :src="customer.service_professional_file" type="application/pdf" width="100%" height="600px" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customer: {
          customer_name: '',
          contact_phone: '',
          address: '',
          pincode: '',
          service: {
            service_name: ''
          },
          service_professional_file: ''
        }
      }
    },
    methods: {
      async fetchServiceProfessionals() {
  try {
    const customerId = this.$route.params.customer_id;
    if (!customerId) {
      console.error("Customer ID is not defined");
      return;
    }
    const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/view_service_professional/${customerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
      },
    });
    if (!response.ok) {
      throw new Error(`Server returned an error: ${response.status} ${response.statusText}`);
    }
    const result = await response.json();
    console.log(result);
    this.customer = result.customer[0]; // Update the customer object with the response data
  } catch (error) {
    console.error(error);
    this.errorMessage = "Unable to connect to the server";
  }
},
    },
    mounted() {
      this.fetchServiceProfessionals();
    }
  };
</script>
