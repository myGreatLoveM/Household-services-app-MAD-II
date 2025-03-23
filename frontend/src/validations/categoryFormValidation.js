
export const validateCategoryForm = (addCategoryForm, addCategoryFormErrors) => {
  if (!addCategoryForm || !addCategoryFormErrors) {
    return false
  }

  if (!addCategoryForm.name) {
    addCategoryFormErrors.name = 'Name is required'
  } else if (addCategoryForm.name.length < 3) {
    addCategoryFormErrors.name = 'Name must be at least 3 characters long'
  } else {
    addCategoryFormErrors.name = ''
  }

  if (!addCategoryForm.description) {
    addCategoryFormErrors.description = 'Description is required'
  } else {
    addCategoryFormErrors.description = ''
  }

  if (!addCategoryForm.basePrice) {
    addCategoryFormErrors.basePrice = 'Base price is required'
  } else if (!isNaN(addCategoryForm.basePrice) && parseInt(addCategoryForm.basePrice) < 100) {
    addCategoryFormErrors.basePrice = 'Base Price should be above 100 INR'
  } else {
    addCategoryFormErrors.basePrice = ''
  }


  if (!addCategoryForm.minTime) {
    addCategoryFormErrors.minTime = 'Min time is required'
  } else if (!isNaN(addCategoryForm.minTime) && parseInt(addCategoryForm.minTime) < 1) {
    addCategoryFormErrors.minTime = 'Minimu time required is 1 hr'
  } else {
    addCategoryFormErrors.minTime = ''
  }

  if (!addCategoryForm.serviceRate) {
    addCategoryFormErrors.serviceRate = 'Service rate is required'
  } else if (!isNaN(addCategoryForm.serviceRate) && parseInt(addCategoryForm.serviceRate) < 1) {
    addCategoryFormErrors.serviceRate = 'Service rate should be above 1 %'
  } else {
    addCategoryFormErrors.serviceRate = ''
  }

  if (!addCategoryForm.bookingRate) {
    addCategoryFormErrors.bookingRate = 'Booking rate is required'
  } else if (!isNaN(addCategoryForm.bookingRate) && parseInt(addCategoryForm.bookingRate) < 1) {
    addCategoryFormErrors.bookingRate = 'Booking rate should be above 1 %'
  } else {
    addCategoryFormErrors.bookingRate = ''
  }

  if (!addCategoryForm.transactionRate) {
    addCategoryFormErrors.transactionRate = 'Transaction rate is required'
  } else if (!isNaN(addCategoryForm.transactionRate) && parseInt(addCategoryForm.transactionRate) < 1) {
    addCategoryFormErrors.transactionRate = 'Transaction rate should be above 1 %'
  } else {
    addCategoryFormErrors.transactionRate = ''
  }

  const isFormInvalid = Object.values(addCategoryFormErrors).some((error) => error !== '')
  return isFormInvalid
}
