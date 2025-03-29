export function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('en-US', options)
}

export function getAuthToken() {
  const token = JSON.parse(localStorage.getItem('auth-token')) || null

  if (token) {
    return token
  } else {
    console.warn('No auth token found in localStorage')
    return null
  }
}

export function getRefreshToken() {
  const token = JSON.parse(localStorage.getItem('refresh-token')) || null

  if (token) {
    return token
  } else {
    console.warn('No refresh token found in localStorage')
    return null
  }
}

export function trimObjectStringValues(obj) {
  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => {
      if (typeof value === 'string') {
        value = value.trim()
      }
      return [key, value]
    }),
  )
}

export function parseNumericFields(obj) {
  Object.entries(obj).forEach(([k, v]) => {
    if (typeof v === 'string' && !isNaN(v) && v.trim() !== '') {
      obj[k] = parseInt(v)
    }
  })
  return obj
}

export function generateRandomNumberString(length) {
  let randomNumber = ''
  for (let i = 0; i < length; i++) {
    randomNumber += Math.floor(Math.random() * 10) // Generates a digit between 0-9
  }
  return randomNumber
}

export function isToday(bookingDate) {
  const today = new Date()

  // Extract year, month, and date for both today and bookingDate
  const bookingYear = bookingDate.getFullYear()
  const bookingMonth = bookingDate.getMonth()
  const bookingDay = bookingDate.getDate()

  const todayYear = today.getFullYear()
  const todayMonth = today.getMonth()
  const todayDay = today.getDate()

  // Check if year, month, and day match
  return bookingYear === todayYear && bookingMonth === todayMonth && bookingDay === todayDay
}