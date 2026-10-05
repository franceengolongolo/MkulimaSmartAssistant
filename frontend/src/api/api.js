const API_BASE_URL = 'http://127.0.0.1:8000'

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('access_token')

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    let errorMessage = `API Error: ${response.status}`

    try {
      const errorData = await response.json()

      if (errorData.detail) {
        errorMessage =
          typeof errorData.detail === 'string'
            ? errorData.detail
            : JSON.stringify(errorData.detail)
      }
    } catch {
      // Response haikuwa JSON
    }

    throw new Error(errorMessage)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}


/* =========================
   AUTHENTICATION
========================= */

export async function requestOtp(simu) {
  return apiRequest('/auth/request-otp', {
    method: 'POST',
    body: JSON.stringify({
      simu,
    }),
  })
}


export async function verifyOtp(simu, code) {
  const data = await apiRequest('/auth/verify-otp', {
    method: 'POST',
    body: JSON.stringify({
      simu,
      code,
    }),
  })

  localStorage.setItem('access_token', data.access_token)

  localStorage.setItem(
    'farmer',
    JSON.stringify({
      farmer_id: data.farmer_id,
      jina: data.jina,
      simu: data.simu,
    }),
  )

  return data
}


/* =========================
   FARMERS / REGISTRATION
========================= */

export async function createFarmer(farmerData) {
  return apiRequest('/farmers/', {
    method: 'POST',
    body: JSON.stringify(farmerData),
  })
}


/* =========================
   CROPS
========================= */

export async function getCrops() {
  return apiRequest('/crops/')
}


export async function getCrop(cropId) {
  return apiRequest(`/crops/${cropId}`)
}


/* =========================
   CROP PROGRAMS
========================= */

export async function getCropPrograms() {
  return apiRequest('/crop-programs/')
}


export async function getCropProgram(programId) {
  return apiRequest(`/crop-programs/${programId}`)
}


/* =========================
   PROGRAM STAGES
========================= */

export async function getProgramStages() {
  return apiRequest('/program-stages/')
}


/* =========================
   PROGRAM TASKS
========================= */

export async function getProgramTasks() {
  return apiRequest('/program-tasks/')
}


/* =========================
   PROGRAM INPUTS
========================= */

export async function getProgramInputs() {
  return apiRequest('/program-inputs/')
}


/* =========================
   PROGRAM RULES
========================= */

export async function getProgramRules() {
  return apiRequest('/program-rules/')
}


/* =========================
   PROGRAM SOURCES
========================= */

export async function getProgramSources() {
  return apiRequest('/program-sources/')
}


/* =========================
   SCHEDULES
========================= */

export async function getSchedules() {
  return apiRequest('/schedules/')
}


/* =========================
   COSTS
========================= */

export async function getCosts() {
  return apiRequest('/costs/')
}


/* =========================
   PROFIT / LOSS
========================= */

export async function getProfitLoss(cropId) {
  return apiRequest(`/profit-loss/crop/${cropId}`)
}


/* =========================
   REMINDERS / NOTIFICATIONS
========================= */

export async function getReminderDashboard() {
  return apiRequest('/reminders/dashboard')
}


/* =========================
   FARMS
========================= */

export async function getFarms() {
  return apiRequest('/farms/')
}


export async function createFarm(farmData) {
  return apiRequest('/farms/', {
    method: 'POST',
    body: JSON.stringify(farmData),
  })
}


/* =========================
   CREATE CROP
========================= */

export async function createCrop(cropData) {
  return apiRequest('/crops/', {
    method: 'POST',
    body: JSON.stringify(cropData),
  })
}


/* =========================
   GENERATE CROP SCHEDULES
========================= */

export async function generateCropProgramSchedules(cropId) {
  return apiRequest(`/crops/${cropId}/generate-program-schedules`, {
    method: 'POST',
  })
}