import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import AdminLogin from '@/components/AdminLogin.vue'
import CustomerLogin from '@/components/CustomerLogin.vue'
import ServiceProfessionalRegister from '@/components/ServiceProfessionalRegister.vue'
import HomeownerRegister from '@/components/HomeownerRegister.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import CreateService from '@/components/CreateService.vue'
import AdminSearch from '@/components/AdminSearch.vue'
import AdminSummary from '@/components/AdminSummary.vue'
import EditService from '@/components/EditService.vue'
import ViewServiceProfessional from '@/components/ViewServiceProfessional.vue'
import HomeownerDashboard from '@/components/HomeownerDashboard.vue'
import CreateRequest from '@/components/CreateRequest.vue'
import EditRequest from '@/components/EditRequest.vue'
import HomeownerSearch from '@/components/HomeownerSearch.vue'
import ServiceProfessionalDashboard from '@/components/ServiceProfessionalDashboard.vue'
import CloseRequest from '@/components/CloseRequest.vue'
import BiddingRequest from '@/components/BiddingRequest.vue'
import OpenRequest from '@/components/OpenRequest.vue'
import BidRequest from '@/components/BidRequest.vue'
import ExportData from '@/components/ExportData.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/hhs_admin_login',
            name: 'hhs_admin_login',
            component: AdminLogin,
        },
        {
            path: '/login',
            name: 'login',
            component: CustomerLogin,
        },
        {
            path: '/service_professional_register',
            name: 'service_professional_register',
            component: ServiceProfessionalRegister,
        },
        {
            path :"/home_owner_register",
            name:"home_owner_register",
            component: HomeownerRegister,
        },
        {
            path :"/admin_dashboard",
            name:"admin_dashboard",
            component: AdminDashboard,
        },
        {
            path :"/admin_dashboard/create_service",
            name:"create_service",
            component: CreateService,
        },
        {
            path :"/admin_dashboard/search",
            name:"admin_search",
            component: AdminSearch,
        },
        {
            path :"/admin_dashboard/summary",
            name:"admin_summary",
            component: AdminSummary,
        },
        {
            path: '/admin_dashboard/edit_service/:id',
            name: 'edit_service',
            component: EditService,
            meta: {
              requiresAuth: true,
              role: 'admin'
            }
        },
        {
            path: '/logout',
            name : "logout"
        },
        {
            path: '/admin_dashboard/view_service_professional/:customer_id',
            name: 'view_service_professional',
            component: ViewServiceProfessional
        },
        {
            path: '/home_owner_dashboard',
            name: 'home_owner_dashboard',
            component: HomeownerDashboard
        },
        {
            path: '/home_owner_dashboard/create_request/:service_id',
            name: 'create_request',
            component: CreateRequest
        },
        {
            path: '/home_owner_dashboard/edit_request/:service_request_id',
            name: 'edit_request',
            component: EditRequest  
        },
        {
            path: '/home_owner_dashboard/search',
            name: 'home_owner_search',
            component: HomeownerSearch
        },
        {
            path: '/service_professional_dashboard',
            name: 'service_professional_dashboard',
            component: ServiceProfessionalDashboard
        },
        {
            path: '/home_owner_dashboard/close_request/:service_request_id',
            name: 'CloseRequest',
            component: CloseRequest
        },
        {
            path: '/home_owner_dashboard/bidding_requests',
            name: 'bidding_request',
            component: BiddingRequest
        },
        {
            path: '/service_professional_dashboard/open_requests_service_professional',
            name: 'open_request',
            component: OpenRequest
        },
        {
            path: '/service_professional_dashboard/bid_request/:requestId',
            name: 'BidRequest',
            component: BidRequest
        },
        {
            path : '/data_export',
            name : 'data_export',
            component : ExportData
        },
        {
            path : '/closed_requests',
            name : 'closed_requests',
        }
    ]
})

export default router