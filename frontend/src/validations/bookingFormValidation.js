import { isToday } from "@/utils"


export const validateBookingForm = (bookingForm, bookingFormErrors) => {
  if (!bookingForm || !bookingFormErrors) {
    return false
  }

  const today = new Date()
  const bookDate = new Date(bookingForm.bookDate)
  const fullfillmentDate = new Date(bookingForm.fullfillmentDate)

  if (!bookingForm.bookDate) {
    bookingFormErrors.bookDate = 'Book date is required'
  } else if (bookDate < today && !isToday(bookDate)) {
    bookingFormErrors.bookDate = 'Select valid book date'
  } else {
    bookingFormErrors.bookDate = ''
  }

  if (!bookingForm.fullfillmentDate) {
    bookingFormErrors.fullfillmentDate = 'Fullfillment date is required'
  } else if (!!bookDate && (fullfillmentDate < bookDate)) {
    bookingFormErrors.fullfillmentDate = 'Select valid fullfillment date'
  } else {
    bookingFormErrors.fullfillmentDate = ''
  }

  const isFormInvalid = Object.values(bookingFormErrors).some((error) => error !== '')
  return isFormInvalid
}






export const validateServiceForm = (serviceForm, serviceFormErrors) => {
  if (!serviceForm || !serviceFormErrors) {
    return false
  }


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
