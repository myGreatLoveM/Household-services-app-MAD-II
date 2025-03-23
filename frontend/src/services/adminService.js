import { useAuthStore } from "@/stores/authStore.js"
import { UserStatus } from "@/constants.js"


export async function getAllCategoriesForAdminDashboard(page) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page) })

    const resp = await fetch(`/api/v1/admin/categories?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Failed to fetch categories')
    }

    if (!respData.data && !respData.data.categories) {
      throw new Error('Response has missing required fields: categories')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching categories')
  }
}


export async function createNewCategoryForAdminDashboard() {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch('/api/v1/admin/categories', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong fetching categories')
    }

    if (!respData.data && !respData.data.categories) {
      throw new Error('Data has missing required fields: categories')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching categories')
  }
}


export async function getAllProvidersForAdminDashboard(status=UserStatus.APPROVED, page) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page), status })

    const resp = await fetch(`/api/v1/admin/providers?${params.toString()}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })
    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong fetching providers')
    }

    if (!respData.data && !respData.data.providers) {
      throw new Error('Data has missing required fields: providers')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching providers')
  }
}


export async function getAllCustomersForAdminDashboard(status, page) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page), status })

    const resp = await fetch(`/api/v1/admin/customers?${params.toString()}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })
    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong fetching customers')
    }

    if (!respData.data && !respData.data.customers) {
      throw new Error('Data has missing required fields: customers')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching customers')
  }
}
