
export const validateCategoryForm = (categoryForm, categoryFormErrors) => {
  if (!categoryForm || !categoryFormErrors) {
    return false
  }

  if (!categoryForm.name) {
    categoryFormErrors.name = 'Name is required'
  } else if (categoryForm.name.length < 3) {
    categoryFormErrors.name = 'Name must be at least 3 characters long'
  } else {
    categoryFormErrors.name = ''
  }

  if (!categoryForm.description) {
    categoryFormErrors.description = 'Description is required'
  } else {
    categoryFormErrors.description = ''
  }

  if (!categoryForm.basePrice) {
    categoryFormErrors.basePrice = 'Base price is required'
  } else if (!isNaN(categoryForm.basePrice) && parseInt(categoryForm.basePrice) < 100) {
    categoryFormErrors.basePrice = 'Base Price should be above 100 INR'
  } else {
    categoryFormErrors.basePrice = ''
  }


  if (!categoryForm.minTime) {
    categoryFormErrors.minTime = 'Min time is required'
  } else if (!isNaN(categoryForm.minTime) && parseInt(categoryForm.minTime) < 1) {
    categoryFormErrors.minTime = 'Minimu time required is 1 hr'
  } else {
    categoryFormErrors.minTime = ''
  }

  if (!categoryForm.serviceRate) {
    categoryFormErrors.serviceRate = 'Service rate is required'
  } else if (!isNaN(categoryForm.serviceRate) && parseInt(categoryForm.serviceRate) < 1) {
    categoryFormErrors.serviceRate = 'Service rate should be above 1 %'
  } else {
    categoryFormErrors.serviceRate = ''
  }

  if (!categoryForm.bookingRate) {
    categoryFormErrors.bookingRate = 'Booking rate is required'
  } else if (!isNaN(categoryForm.bookingRate) && parseInt(categoryForm.bookingRate) < 1) {
    categoryFormErrors.bookingRate = 'Booking rate should be above 1 %'
  } else {
    categoryFormErrors.bookingRate = ''
  }

  if (!categoryForm.transactionRate) {
    categoryFormErrors.transactionRate = 'Transaction rate is required'
  } else if (!isNaN(categoryForm.transactionRate) && parseInt(categoryForm.transactionRate) < 1) {
    categoryFormErrors.transactionRate = 'Transaction rate should be above 1 %'
  } else {
    categoryFormErrors.transactionRate = ''
  }

  const isFormInvalid = Object.values(categoryFormErrors).some((error) => error !== '')
  return isFormInvalid
}
