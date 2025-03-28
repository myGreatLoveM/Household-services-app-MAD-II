import { useAuthStore } from "@/stores/authStore.js"


export async function getAllServicesForProviderDashboard(provId, page) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page) })

    const resp = await fetch(`/api/v1/providers/${provId}/services?${params.toString()}`, {
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
      throw new Error(respData.err_message || 'Failed to fetch services !!')
    }

    if (!respData.data && !respData.data.services) {
      throw new Error('Response has missing required fields: services')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching services!!')
  }
}

export async function createServiceForProvider(provId, serviceData) {

  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/services`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ...serviceData }),
    })

    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Failed to create service !!')
    }

  } catch (error) {
    throw new Error(error.message || 'Something went wrong creating service!!')
  }
}

export async function continueServiceForProviderDashboard(provId, { serviceId, serviceName }) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/services/${serviceId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to update service status!!')
    }

    return { serviceId, serviceName }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong updating service status!!')
  }
}

export async function discontinueServiceForProviderDashboard(provId, {serviceId, serviceName}) {

  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/services/${serviceId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })


    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to discontinue service!!')
    }

    return { serviceId, serviceName }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong discontinue service!!')
  }
}

export async function getAllBookingsForProviderDashboard(provId, page, status) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page), status })

    const resp = await fetch(`/api/v1/providers/${provId}/bookings?${params.toString()}`, {
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
      throw new Error(respData.err_message || 'Failed to fetch services !!')
    }

    if (!respData.data && !respData.data.bookings) {
      throw new Error('Response has missing required fields: bookings')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching bookings!!')
  }
}

export async function confirmBookingForProviderDashboard(provId, bookingId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/bookings/${bookingId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to confirm booking!!')
    }

    return { bookingId }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during booking confirm!!')
  }
}

export async function closeBookingForProviderDashboard(provId, bookingId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/bookings/${bookingId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to close booking!!')
    }

    return { bookingId }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during booking close!!')
  }
}

export async function rejectBookingForProviderDashboard(provId, bookingId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/bookings/${bookingId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to reject booking!!')
    }

    return { }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during booking reject!!')
  }
}

export async function updateProfileForProviderDashboard(provId, profileData) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/profile`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ...profileData }),
    })

    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Failed to update profile!!')
    }

  } catch (error) {
    throw new Error(error.message || 'Something went wrong updating profile!!')
  }
}

export async function getProfileForProviderDashboard(provId) {

  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/profile`, {
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
      throw new Error(respData.err_message || 'Failed to get profile !!')
    }

     if (!respData.data && !respData.data.provider) {
       throw new Error('Response has missing required fields: provider')
     }

    return respData.data.provider
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching profile!!')
  }
}



export async function exportClosedBookingData(provId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/providers/${provId}/bookings/`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to confirm booking!!')
    }

    return { bookingId }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during booking confirm!!')
  }
}
