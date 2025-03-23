

export const validateRegisterForm = (registerForm, registerFormErrors, role) => {

  if (!registerForm || !registerFormErrors) {
    return false
  }

  // Validate email
  if (!registerForm.email) {
    registerFormErrors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(registerForm.email)) {
    registerFormErrors.email = 'Invalid email'
  } else {
    registerFormErrors.email = ''
  }

  // Validate username
  if (!registerForm.username) {
    registerFormErrors.username = 'Username is required'
  } else if (registerForm.username.length < 3) {
    registerFormErrors.username = 'Username must be at least 3 characters long'
  } else {
    registerFormErrors.username = ''
  }

  // Validate password
  if (!registerForm.password) {
    registerFormErrors.password = 'Password is required'
  } else if (registerForm.password.length < 6) {
    registerFormErrors.password = 'Password must be at least 6 characters long'
  } else {
    registerFormErrors.password = ''
  }

  // Validate confirmPassword
  if (!registerForm.confirmPassword) {
    registerFormErrors.confirmPassword = 'Confirm Password is required'
  } else if (registerForm.password !== registerForm.confirmPassword) {
    registerFormErrors.confirmPassword = 'Confirm password should match with password'
  } else {
    registerFormErrors.confirmPassword = ''
  }

  // Validate gender
  if (!registerForm.gender) {
    registerFormErrors.gender = 'Select gender'
  } else {
    registerFormErrors.gender = ''
  }

  // Validate location
  if (!registerForm.location) {
    registerFormErrors.location = 'Location is required'
  } else if (registerForm.location.length < 5) {
    registerFormErrors.location = 'Please provide valid location, at least 5 characters long'
  } else {
    registerFormErrors.location = ''
  }

  // Validate contact
  if (!registerForm.contact) {
    registerFormErrors.contact = 'Contact is required'
  } else if (registerForm.contact.length < 10 || registerForm.contact.length > 10 || isNaN(registerForm.contact)) {
    registerFormErrors.contact = 'Please provide valid contact number, 10 characters long'
  } else {
    registerFormErrors.contact = ''
  }

  // Validate category for provider
  if (role === 'provider') {
    if (!registerForm.category) {
      registerFormErrors.category = 'Select category'
    } else {
      registerFormErrors.category = ''
    }

  // Validate experience for provider
    if (!registerForm.experience) {
      registerFormErrors.experience = 'Experience is required'
    } else if (parseInt(registerForm.experience) < 0) {
      registerFormErrors.experience = 'Please provide valid experience'
    } else {
      registerFormErrors.experience = ''
    }
  }

  const isFormInvalid = Object.values(registerFormErrors).some((error) => error !== '')
  return !isFormInvalid
}

export const validateLoginForm = (loginForm, loginFormErrors) => {

  if (!loginForm || !loginFormErrors) {
    return false
  }

  // Validate username
  if (!loginForm.username) {
    loginFormErrors.username = 'Username is required'
  } else if (loginForm.username.length < 3) {
    loginFormErrors.username = 'Username must be at least 3 characters long'
  } else {
    loginFormErrors.username = ''
  }

  // Validate password
  if (!loginForm.password) {
    loginFormErrors.password = 'Password is required'
  } else if (loginForm.password.length < 6) {
    loginFormErrors.password = 'Password must be at least 6 characters long'
  } else {
    loginFormErrors.password = ''
  }

  const isFormInvalid = Object.values(loginFormErrors).some((error) => error !== '')
  return !isFormInvalid
}
