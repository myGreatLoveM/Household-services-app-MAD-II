

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
