

export const validateServiceForm = (serviceForm, serviceFormErrors) => {
  if (!serviceForm || !serviceFormErrors) {
    return false
  }
  console.log('validate');
  if (!serviceForm.name) {
    serviceFormErrors.name = 'Name is required'
  } else if (serviceForm.name.length < 3) {
    serviceFormErrors.name = 'Name must be at least 3 characters long'
  } else {
    serviceFormErrors.name = ''
  }

  if (!serviceForm.description) {
    serviceFormErrors.description = 'Description is required'
  } else {
    serviceFormErrors.description = ''
  }

  if (!serviceForm.price) {
    serviceFormErrors.price = 'Price is required'
  } else if (!isNaN(serviceForm.price) && parseInt(serviceForm.price) < 100) {
    serviceFormErrors.price = 'Price should be above 100 INR'
  } else {
    serviceFormErrors.price = ''
  }

  if (!serviceForm.time) {
    serviceFormErrors.time = 'Min time is required'
  } else if (!isNaN(serviceForm.time) && parseInt(serviceForm.time) < 1) {
    serviceFormErrors.time = 'Minimum time required is 1 hr'
  } else {
    serviceFormErrors.time = ''
  }

  const isFormInvalid = Object.values(serviceFormErrors).some((error) => error !== '')
  return isFormInvalid
}
