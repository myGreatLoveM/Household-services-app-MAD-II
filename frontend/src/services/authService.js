
import { getRefreshToken } from "@/utils.js"

export async function getAllCategoriesForRegisterForm() {
  try {
    const params = new URLSearchParams({ only_names: true })

    const resp = await fetch(`/api/v1/categories?${params.toString()}`)
    const respData = await resp.json()

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong fetching category names')
    }

    if (!respData?.data && !respData?.data?.categories) {
      throw new Error('Data has missing required fields: categories')
    }

    return respData.data.categories
  } catch (error) {
    throw new Error(error.message || 'Something went wrong fetching category names')
  }
}


export async function registerUserService(formData, role) {
  try {
    const res = await fetch(`/api/v1/auth/register/${role}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...formData }),
    })
    const respData = await res.json()

    if (!res.ok || !respData.success) {
      throw new Error(respData.err_message || 'Registration failed')
    }

  } catch (error) {
    throw new Error(error.message || 'Something went wrong during registration')
  }
}


export async function loginUserService(formData) {
  try {
     const res = await fetch('/api/v1/auth/login', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ ...formData }),
     })
     const resp_data = await res.json()

     if (!res.ok || !resp_data.success) {
      throw new Error(resp_data.err_message || 'Login failed')
     }

     const data = resp_data?.data

     if (!data || !data?.access_token || !data?.refresh_token || !data?.user || !data?.user?.role) {
      throw new Error('Login failed. Missing necessary user data !!')
     }

     return data
  } catch (error) {
    throw new Error(error.message || 'Something went wrong during login!!')
  }
}


export async function refreshTokens() {
  try {
    const refreshToken = getRefreshToken()

    if (!refreshToken) {
      throw new Error('')
    }

    const res = await fetch('/api/v1/auth/token/refresh', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${refreshToken}`,
        'Content-Type': 'application/json',
      },
    })
    const resp_data = await res.json()

    if (!res.ok || !resp_data.success) {
      throw new Error(resp_data.err_message || 'Failed to refresh token!!')
    }

    const data = resp_data?.data

    if (!data || !data?.access_token || !data?.refresh_token) {
      throw new Error('Refreshing tokens failed due to missing fields!!')
    }

    return data
  } catch (error) {
    console.log(error);
    throw new Error(error.message || 'Something went wrong during refreshing tokens!!')
  }
}
