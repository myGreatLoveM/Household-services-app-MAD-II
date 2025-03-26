

export async function getAllCategoriesDetails(page) {
  try {
    const params = new URLSearchParams({ page })

    const resp = await fetch(`/api/v1/categories?${params.toString()}`)
    const respData = await resp.json()

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong while fetching category data')
    }

    if (!respData?.data || !respData?.data?.categories) {
      throw new Error('Data has missing required fields: categories')
    }

    return respData?.data
  } catch(error) {
    throw new Error(error.message || 'Something went wrong while fetching category data')
  }
}


export async function getAllActiveServices(page) {
  try {
    const params = new URLSearchParams({ page })

    const resp = await fetch(`/api/v1/active-services?${params.toString()}`)
    const respData = await resp.json()

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong while fetching services data')
    }

    if (!respData?.data || !respData?.data?.services) {
      throw new Error('Data has missing required fields: services')
    }

    return respData?.data
  } catch(error) {
    throw new Error(error.message || 'Something went wrong while fetching services data')
  }
}

export async function getActiveService(serviceId) {
  try {

    const resp = await fetch(`/api/v1/active-services/${serviceId}`)
    const respData = await resp.json()

    if (!resp.ok || !respData.success) {
      throw new Error(respData.err_message || 'Something went wrong while fetching service')
    }

    if (!respData?.data || !respData?.data?.service) {
      throw new Error('Data has missing required fields: service')
    }

    return respData?.data
  } catch(error) {
    throw new Error(error.message || 'Something went wrong while fetching service')
  }
}
