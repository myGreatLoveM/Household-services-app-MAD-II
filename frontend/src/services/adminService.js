import { useAuthStore } from "@/stores/authStore.js"
import { UserStatus, ServiceStatus } from '@/constants.js'



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
      throw new Error(respData.err_message || 'Failed to fetch categories!!')
    }

    if (!respData.data && !respData.data.categories) {
      throw new Error('Response has missing required fields: categories')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching categories!!')
  }
}

export async function getCategoryForAdminDashboard(catId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }


    const resp = await fetch(`/api/v1/admin/categories/${catId}`, {
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
      throw new Error(respData.err_message || 'Failed to fetch categories!!')
    }

    if (!respData.data && !respData.data.category) {
      throw new Error('Response has missing required fields: category')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching category!!')
  }
}

export async function createNewCategoryForAdminDashboard(categoryData) {
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
      body: JSON.stringify(categoryData),
    })

    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Failed to create new category!!')
    }

    return respData
  } catch (error) {
    throw new Error(error.message || 'Something went wrong creating new category!!')
  }
}

export async function updateExistingCategoryForAdminDashboard(catId, categoryData) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }
    console.log(categoryData);
    const resp = await fetch(`/api/v1/admin/categories/${catId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(categoryData),
    })

    
    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to update category!!')
    }

    return 
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during category update!!')
  }
}


export async function getAllServicesForAdminDashboard(page, status=ServiceStatus.APPROVED) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page), status })

    const resp = await fetch(`/api/v1/admin/services?${params.toString()}`, {
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
      throw new Error(respData.err_message || 'Failed to fetch services!!')
    }

    if (!respData.data && !respData.data.services) {
      throw new Error('Response has missing required fields: services')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching services!!')
  }
}


export async function approveOrUnblockServiceForAdminDashboard({ serviceId, serviceName }) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/admin/services/${serviceId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error(`Failed to update status of service ${serviceName}!!`)
    }

    return { serviceId, serviceName }
  } catch (error) {
    console.log('error', error)
    throw new Error(error.message || `Something went wrong updating status ${serviceName}!!`)
  }
}


export async function blockServiceForAdminDashboard({ serviceId, serviceName}) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/admin/services/${serviceId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error(`Failed to block service ${serviceName}!!`)
    }

    return { serviceId, serviceName }
  } catch (error) {
    console.log('error', error)
    throw new Error(error.message || `Something went wrong blocking service ${serviceName}!!`)
  }
}


export async function getAllProvidersForAdminDashboard(page, status=UserStatus.APPROVED) {
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
      throw new Error(respData.err_message || 'Failed to fetch providers!!')
    }

    if (!respData.data && !respData.data.providers) {
      throw new Error('Data has missing required fields: providers')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching providers')
  }
}


export async function approveOrUnblockProviderForAdminDashboard({provId, provUsername}) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/admin/providers/${provId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error(`Failed to update status of provider ${provUsername}!!`)
    }

    return {provId, provUsername}
  } catch (error) {
    console.log('error', error);
    throw new Error(error.message || `Something went wrong updating status ${provUsername}!!`)
  }
}


export async function blockProviderForAdminDashboard({provId, provUsername}) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/admin/providers/${provId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error(`Failed to block provider ${provUsername}!!`)
    }

    return {provId, provUsername}
  } catch (error) {
    console.log('error', error);
    throw new Error(error.message || `Something went wrong, blocking provider ${provUsername}!!`)
  }
}


export async function getAllCustomersForAdminDashboard(page, status) {
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
