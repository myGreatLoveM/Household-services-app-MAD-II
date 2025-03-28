import { useAuthStore } from '@/stores/authStore.js'


export async function createBookingForCustomer(custId, serviceId, bookingData) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/bookings`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ...bookingData, serviceId }),
    })

    const respData = await resp.json()

    if (resp.status == 401 && respData?.errors?.token_type) {
      authStore.refreshExpiredAuthToken()
      throw new Error('Auth Token Expired!!')
    }

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Failed to create bookings !!')
    }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong creating bookings!!')
  }
}

export async function getAllBookingForCustomerDashboard(custId, page, status) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const params = new URLSearchParams({ page: parseInt(page), status })

    const resp = await fetch(`/api/v1/customers/${custId}/bookings?${params.toString()}`, {
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
      throw new Error(respData.err_message || 'Failed to fetch bookings !!')
    }

    if (!respData.data && !respData.data.bookings) {
      throw new Error('Response has missing required fields: services')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching bookings!!')
  }
}

export async function getPaymentDetailOfBookingForCustomerDashboard(custId, paymentId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/payments/${paymentId}`, {
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
      throw new Error(respData.err_message || 'Failed to fetch payment detail!!')
    }

    if (!respData.data && !respData.data.payment) {
      throw new Error('Response has missing required fields: payment')
    }

    return respData.data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching payment detail!!')
  }
}

export async function confirmPaymentOfBookingForProviderDashboard(custId, paymentId, paymentData) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/payments/${paymentId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${authStore.authToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({...paymentData}),
    })

    if (resp.status == 401) {
      const respData = await resp.json()
      if (respData?.errors?.token_type) {
        authStore.refreshExpiredAuthToken()
        throw new Error('Auth Token Expired!!')
      }
    }

    if (!resp.ok) {
      throw new Error('Failed to confirm payment!!')
    }

    return { paymentId }
  } catch (error) {
    console.log(error);
    throw new Error(error.message || 'Something went wrong during payment confirm!!')
  }
}

export async function cancelPaymentOfBookingForProviderDashboard(custId, paymentId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/payments/${paymentId}`, {
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
      throw new Error('Failed to cancel payment!!')
    }

    return { paymentId }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during payment cancel!!')
  }
}


export async function completeBookingForProviderDashboard(custId, bookingId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/bookings/${bookingId}`, {
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
      throw new Error('Failed to complete booking!!')
    }

    return { bookingId }
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during booking complete!!')
  }
}

export async function updateProfileForCustomerDashboard(custId, profileData) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/profile`, {
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

export async function getProfileForCustomerDashboard(custId) {
  try {
    const authStore = useAuthStore()

    if (!authStore.authToken) {
      throw new Error('Auth token required to fetch data!!')
    }

    const resp = await fetch(`/api/v1/customers/${custId}/profile`, {
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

    if (!respData.data && !respData.data.customer) {
      throw new Error('Response has missing required fields: Customer')
    }

    return respData.data.customer
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching profile!!')
  }
}
