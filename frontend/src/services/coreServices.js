

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
