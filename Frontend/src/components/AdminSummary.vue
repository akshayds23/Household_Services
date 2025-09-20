<template>
  <div>
    <nav class="navbar navbar-expand-lg fade-in-up">
      <div class="container">
        <router-link class="navbar-brand" to="/admin_dashboard">Admin Dashboard</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-mdb-toggle="collapse"
          data-mdb-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
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
              <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_dashboard/summary">Summary</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div v-if="isAuthenticated" class="container page-section fade-in-up">
      <h1 class="text-center">Admin Summary</h1>
      <div class="row">
        <!-- Users by Category -->
        <div class="col-md-6 mb-4 chart-section">
          <h3>Users by Category</h3>
          <div class="chart-visual">
            <template v-if="userHasData">
              <div class="bar-chart3d">
                <div
                  v-for="bar in userBarData"
                  :key="bar.label"
                  class="bar3d"
                  :style="{ '--bar-height': bar.height, '--bar-color': bar.color }"
                >
                  <div class="bar3d-column">
                    <span class="bar3d-count">{{ bar.count }}</span>
                  </div>
                  <span class="bar3d-label">{{ bar.label }}</span>
                </div>
              </div>
            </template>
            <p v-else class="text-muted">No user data available</p>
          </div>

          <div class="category-panel">
            <table class="category-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Home Owners</td>
                  <td>{{ homeOwnerCount }}</td>
                </tr>
                <tr>
                  <td>Service Professionals</td>
                  <td>{{ serviceProfessionalCount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Status of Requests -->
        <div class="col-md-6 mb-4 chart-section">
          <h3>Status of Requests</h3>
          <div class="chart-visual">
            <div class="donut3d-wrapper">
              <div class="donut3d" :class="{ 'donut3d--empty': !statusHasData }" :style="statusChartStyle">
                <div class="donut3d-inner"></div>
              </div>
              <div class="donut3d-shadow"></div>
            </div>
          </div>
          <p v-if="!statusHasData" class="text-muted text-center mt-2 mb-3">No request data available</p>
          <p v-if="hasError" class="text-danger text-center">{{ errorMessage }}</p>

          <ul class="status-legend">
            <li v-for="segment in statusSegments" :key="segment.label">
              <span class="legend-swatch" :style="{ background: segment.color }"></span>
              <span class="legend-label">{{ segment.label }}</span>
              <span class="legend-value">{{ segment.count }}</span>
              <span class="legend-percent" v-if="statusTotal">{{ Math.round(segment.percent) }}%</span>
            </li>
          </ul>


        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: !!localStorage.getItem('adminToken'),
      homeOwnerCount: 0,
      serviceProfessionalCount: 0,
      acceptedCount: 0,
      pendingCount: 0,
      rejectedCount: 0,
      closedCount: 0,
      errorMessage: null
    };
  },
  computed: {
    userHasData() {
      return (this.homeOwnerCount || 0) + (this.serviceProfessionalCount || 0) > 0;
    },
    userBarData() {
      const bars = [
        { label: 'Home Owners', count: Number(this.homeOwnerCount) || 0, color: '#38bdf8' },
        { label: 'Service Professionals', count: Number(this.serviceProfessionalCount) || 0, color: '#f97316' }
      ];
      const max = Math.max(...bars.map(bar => bar.count), 0);
      const fallbackHeight = '18%';
      return bars.map(bar => ({
        ...bar,
        height: this.userHasData && max > 0 ? `${Math.max((bar.count / max) * 100, 12)}%` : fallbackHeight
      }));
    },
    statusCounts() {
      return [
        { label: 'Accepted', count: Number(this.acceptedCount) || 0, color: '#22c55e' },
        { label: 'Pending', count: Number(this.pendingCount) || 0, color: '#facc15' },
        { label: 'Rejected', count: Number(this.rejectedCount) || 0, color: '#f87171' },
        { label: 'Closed', count: Number(this.closedCount) || 0, color: '#60a5fa' }
      ];
    },
    statusTotal() {
      return this.statusCounts.reduce((total, segment) => total + segment.count, 0);
    },
    statusSegments() {
      const total = this.statusTotal;
      let cumulative = 0;
      return this.statusCounts.map(segment => {
        const percent = total > 0 ? (segment.count / total) * 100 : 0;
        const start = cumulative;
        cumulative += percent;
        return {
          ...segment,
          percent,
          start,
          end: cumulative
        };
      });
    },
    statusChartStyle() {
      if (!this.statusHasData) {
        return {
          background: 'radial-gradient(circle at 50% 45%, rgba(148, 163, 184, 0.35), rgba(30, 41, 59, 0.9))'
        };
      }

      const stops = this.statusSegments
        .filter(segment => segment.percent > 0)
        .map(segment => `${segment.color} ${segment.start}% ${segment.end}%`)
        .join(', ');

      return {
        background: `conic-gradient(${stops})`
      };
    },
    statusHasData() {
      return this.statusTotal > 0;
    },
    hasError() {
      return !!this.errorMessage;
    }
  },
  methods: {
    async fetchSummaryData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/admin_dashboard/summary', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('adminToken')}`,
            'Content-Type': 'application/json'
          }
        });

        const result = await response.json();
        if (!response.ok) {
          this.errorMessage = result.message || 'Unable to load admin summary.';
          this.resetMetrics();
          return;
        }

        this.homeOwnerCount = Number(result.home_owner_count) || 0;
        this.serviceProfessionalCount = Number(result.service_professional_count) || 0;
        this.acceptedCount = Number(result.accepted_count) || 0;
        this.pendingCount = Number(result.pending_count) || 0;
        this.rejectedCount = Number(result.rejected_count) || 0;
        this.closedCount = Number(result.closed_count) || 0;
        this.errorMessage = null;
      } catch (error) {
        console.error('Unable to connect to the server', error);
        this.errorMessage = 'Failed to load summary data.';
        this.resetMetrics();
      }
    },
    resetMetrics() {
      this.homeOwnerCount = 0;
      this.serviceProfessionalCount = 0;
      this.acceptedCount = 0;
      this.pendingCount = 0;
      this.rejectedCount = 0;
      this.closedCount = 0;
    },
    async logout() {
      try {
        const response = await fetch('http://127.0.0.1:5000/logout', {
          method: 'POST',
          headers: { Authorization: `Bearer ${localStorage.getItem('adminToken')}` }
        });

        if (response.ok) {
          localStorage.removeItem('adminToken');
          localStorage.removeItem('adminName');
          this.$router.push('/');
        }
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
  },
  mounted() {
    if (this.isAuthenticated) {
      this.fetchSummaryData();
    }
  }
};
</script>

<style scoped>
.chart-visual {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
  min-height: 260px;
}

.bar-chart3d {
  display: flex;
  align-items: flex-end;
  gap: 2.5rem;
  padding: 1.8rem 2.2rem 2.2rem;
  border-radius: 26px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(15, 23, 42, 0.85));
  box-shadow: 0 30px 65px -28px rgba(15, 23, 42, 0.85);
  position: relative;
  isolation: isolate;
}

.bar-chart3d::after {
  content: '';
  position: absolute;
  inset: auto 12% -14% 12%;
  height: 24%;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.2), transparent 65%);
  filter: blur(18px);
  z-index: -1;
}

.bar3d {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.bar3d-column {
  position: relative;
  width: 96px;
  height: var(--bar-height);
  min-height: 16%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.55), var(--bar-color));
  border-radius: 18px 18px 10px 10px;
  box-shadow: 0 32px 45px -28px rgba(56, 189, 248, 0.75);
  transition: transform 280ms ease, box-shadow 280ms ease;
}

.bar-chart3d--empty .bar3d-column {
  opacity: 0.6;
}

.bar3d-column::before {
  content: '';
  position: absolute;
  top: -22px;
  left: -14px;
  width: 96px;
  height: 26px;
  border-radius: 18px 18px 0 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.7), rgba(148, 163, 184, 0.15));
  transform: skewX(-18deg);
  transform-origin: bottom left;
  box-shadow: inset 0 6px 12px rgba(15, 23, 42, 0.35);
}

.bar3d-column::after {
  content: '';
  position: absolute;
  top: 0;
  right: -24px;
  width: 28px;
  height: 100%;
  border-radius: 0 10px 10px 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.7), rgba(56, 189, 248, 0.45));
  transform: skewY(-45deg);
  transform-origin: top right;
  box-shadow: inset -4px 0 12px rgba(8, 47, 73, 0.45);
}

.bar3d-column:hover {
  transform: translateY(-6px);
  box-shadow: 0 38px 65px -32px rgba(56, 189, 248, 0.85);
}

.bar3d-count {
  position: absolute;
  top: -38px;
  left: 50%;
  transform: translateX(-50%);
  font-weight: 600;
  letter-spacing: 0.04em;
}

.bar3d-label {
  font-weight: 500;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: var(--color-text-soft, #cbd5f5);
}

.donut3d-wrapper {
  position: relative;
  width: 240px;
  height: 240px;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1100px;
}

.donut3d {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  transform: rotateX(34deg);
  box-shadow: inset 0 12px 24px rgba(255, 255, 255, 0.18), 0 34px 55px -30px rgba(15, 23, 42, 0.7);
  transition: transform 320ms ease, box-shadow 320ms ease;
}

.donut3d--empty {
  filter: saturate(0.6) brightness(0.9);
  opacity: 0.85;
}

.donut3d::before {
  content: '';
  position: absolute;
  inset: 8%;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 35%, rgba(255, 255, 255, 0.65), transparent 75%);
  mix-blend-mode: screen;
}

.donut3d-inner {
  position: absolute;
  inset: 26%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.85));
  box-shadow: inset 0 8px 16px rgba(15, 23, 42, 0.6);
}

.donut3d-shadow {
  position: absolute;
  bottom: -34px;
  width: 70%;
  height: 28%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(8, 47, 73, 0.45), transparent 65%);
  filter: blur(18px);
  transform: translateZ(-60px);
}

.status-legend {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0;
  display: grid;
  gap: 0.75rem;
}

.status-legend li {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 14px;
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 0 18px 38px -24px rgba(15, 23, 42, 0.6);
}

.legend-swatch {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  box-shadow: 0 0 12px rgba(148, 163, 184, 0.35);
}

.legend-label {
  font-weight: 500;
  letter-spacing: 0.02em;
}

.legend-value {
  font-variant-numeric: tabular-nums;
  font-weight: 600;
}

.category-panel {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.92), rgba(2, 6, 23, 0.82));
  border-radius: 22px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 1.3rem 1.6rem;
  box-shadow: 0 24px 48px -28px rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(16px);
}

.category-table {
  width: 100%;
  border-collapse: collapse;
  color: var(--color-text);
}

.category-table thead th {
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.06em;
  font-size: 0.82rem;
  padding: 0.75rem 1rem;
  color: var(--color-muted, #94a3b8);
}

.category-table tbody tr {
  background: rgba(15, 23, 42, 0.65);
  border-top: 1px solid rgba(148, 163, 184, 0.15);
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.category-table tbody tr:first-child {
  border-top: none;
}

.category-table tbody tr:nth-child(even) {
  background: rgba(15, 23, 42, 0.55);
}

.category-table tbody tr:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px -28px rgba(56, 189, 248, 0.55);
}

.category-table tbody td {
  padding: 0.85rem 1rem;
  font-weight: 500;
}

@media (max-width: 576px) {
  .bar3d-column {
    width: 72px;
  }

  .bar3d-column::before {
    width: 72px;
    left: -10px;
  }

  .bar3d-column::after {
    right: -18px;
  }
}
</style>









