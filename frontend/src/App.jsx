import { useState } from 'react'
import './App.css'
import {
requestOtp,
verifyOtp,
getCrops,
getSchedules,
getCosts,
getProfitLoss,
getReminderDashboard,
createFarmer,
createFarm,
createCrop,
generateCropProgramSchedules,
getCropPrograms,
} from './api/api'

const API_BASE_URL = 'http://127.0.0.1:8000'

async function createCost(costData) {
const token = localStorage.getItem('access_token')

const response = await fetch(`${API_BASE_URL}/costs/`, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
...(token
? { Authorization: `Bearer ${token}` }
: {}),
},
body: JSON.stringify(costData),
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

return response.json()
}

async function getHarvests() {
const token = localStorage.getItem('access_token')

const response = await fetch(`${API_BASE_URL}/harvests/`, {
method: 'GET',
headers: {
...(token
? { Authorization: `Bearer ${token}` }
: {}),
},
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

return response.json()
}

async function createHarvest(harvestData) {
const token = localStorage.getItem('access_token')

const response = await fetch(`${API_BASE_URL}/harvests/`, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
...(token
? { Authorization: `Bearer ${token}` }
: {}),
},
body: JSON.stringify(harvestData),
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

return response.json()
}

async function completeReminder(reminderId) {
const token = localStorage.getItem('access_token')

const response = await fetch(
`${API_BASE_URL}/reminders/${reminderId}/complete`,
{
method: 'PATCH',
headers: {
...(token
? { Authorization: `Bearer ${token}` }
: {}),
},
}
)

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

return response.json()
}

function App() {
const [step, setStep] = useState('phone')
const [simu, setSimu] = useState('')
const [code, setCode] = useState('')
const [farmerRegistration, setFarmerRegistration] = useState({
jina: '',
simu: '',
eneo: '',
})
const [loading, setLoading] = useState(false)
const [dashboardLoading, setDashboardLoading] = useState(false)
const [scheduleLoading, setScheduleLoading] = useState(false)
const [costLoading, setCostLoading] = useState(false)
const [harvestLoading, setHarvestLoading] = useState(false)
const [profitLossLoading, setProfitLossLoading] = useState(false)
const [savingCost, setSavingCost] = useState(false)
const [savingHarvest, setSavingHarvest] = useState(false)
const [completingReminderId, setCompletingReminderId] = useState(null)

const [error, setError] = useState('')
const [message, setMessage] = useState('')

const [crops, setCrops] = useState([])
const [schedules, setSchedules] = useState([])
const [costs, setCosts] = useState([])
const [harvests, setHarvests] = useState([])
const [profitLoss, setProfitLoss] = useState(null)
const [reminderDashboard, setReminderDashboard] = useState(null)
const [reminderLoading, setReminderLoading] = useState(false)
const [farmForm, setFarmForm] = useState({
jina: '',
eneo: '',
ukubwa: '',
})
const [cropForm, setCropForm] = useState({
jina: '',
aina: '',
msimu: '',
tarehe_ya_kupanda: '',
program_id: '',
})
const [createdFarmId, setCreatedFarmId] = useState(null)
const [cropPrograms, setCropPrograms] = useState([])
const [farmCreationStep, setFarmCreationStep] = useState('farm')
const [farmCreating, setFarmCreating] = useState(false)
const [cropCreating, setCropCreating] = useState(false)
const [cropProgramsLoading, setCropProgramsLoading] = useState(false)

const [activePage, setActivePage] = useState('dashboard')

const [costForm, setCostForm] = useState({
jina: '',
aina: '',
kiasi: '',
unit: '',
gharama: '',
tarehe: new Date().toISOString().split('T')[0],
maelezo: '',
})

const [harvestForm, setHarvestForm] = useState({
kiasi: '',
unit: '',
tarehe: new Date().toISOString().split('T')[0],
maelezo: '',
})

async function loadDashboardData() {
setDashboardLoading(true)
setError('')

try {
  const [
    cropsData,
    schedulesData,
    costsData,
    harvestsData,
    reminderDashboardData,
  ] = await Promise.all([
    getCrops(),
    getSchedules(),
    getCosts(),
    getHarvests(),
    getReminderDashboard(),
  ])

  setCrops(cropsData)
  setSchedules(schedulesData)
  setCosts(costsData)
  setHarvests(harvestsData)
  setReminderDashboard(reminderDashboardData)

  if (cropsData.length > 0) {
    const profitLossData = await getProfitLoss(
      cropsData[0].id
    )

    setProfitLoss(profitLossData)
  } else {
    setProfitLoss(null)
  }
} catch (err) {
  setError(err.message)
} finally {
  setDashboardLoading(false)
}

}

async function loadReminderDashboard() {
setReminderLoading(true)
setError('')

try {
  const data = await getReminderDashboard()
  setReminderDashboard(data)
} catch (err) {
  setError(err.message)
} finally {
  setReminderLoading(false)
}

}

async function handleCompleteReminder(reminderId) {
setError('')
setMessage('')
setCompletingReminderId(reminderId)

try {
  await completeReminder(reminderId)

  await loadReminderDashboard()

  setMessage('Kumbusho limekamilishwa kikamilifu.')

  setTimeout(() => {
    setMessage('')
  }, 3000)
} catch (err) {
  setError(err.message)
} finally {
  setCompletingReminderId(null)
}

}

async function loadSchedules() {
setScheduleLoading(true)
setError('')

try {
  const data = await getSchedules()
  setSchedules(data)
} catch (err) {
  setError(err.message)
} finally {
  setScheduleLoading(false)
}

}

async function loadCosts() {
setCostLoading(true)
setError('')

try {
  const data = await getCosts()
  setCosts(data)
} catch (err) {
  setError(err.message)
} finally {
  setCostLoading(false)
}

}

async function loadHarvests() {
setHarvestLoading(true)
setError('')

try {
  const data = await getHarvests()
  setHarvests(data)
} catch (err) {
  setError(err.message)
} finally {
  setHarvestLoading(false)
}

}

async function loadProfitLoss() {
setProfitLossLoading(true)
setError('')

try {
  const currentCrop = getCurrentCrop()

  if (!currentCrop) {
    setProfitLoss(null)
    return
  }

  const data = await getProfitLoss(currentCrop.id)

  console.log('PROFIT LOSS FROM BACKEND:', data)
  console.log('FAIDA/HASARA VALUE:', data.faida_au_hasara)
  console.log('FAIDA/HASARA TYPE:', typeof data.faida_au_hasara)

  setProfitLoss(data)
} catch (err) {
  setError(err.message)
} finally {
  setProfitLossLoading(false)
}

}

async function handleRequestOtp(event) {
event.preventDefault()

setError('')
setMessage('')
setLoading(true)

try {
  const data = await requestOtp(simu)

  setMessage(
    `${data.ujumbe} OTP yako ya majaribio ni ${data.code}`
  )

  setStep('otp')
} catch (err) {
  setError(err.message)
} finally {
  setLoading(false)
}

}

function handleFarmerRegistrationChange(event) {
const { name, value } = event.target

setFarmerRegistration((previous) => ({
  ...previous,
  [name]: value,
}))
}

async function handleRegisterFarmer(event) {
event.preventDefault()

setError('')
setMessage('')
setLoading(true)

try {
  await createFarmer({
    jina: farmerRegistration.jina.trim(),
    simu: farmerRegistration.simu.trim(),
    eneo: farmerRegistration.eneo.trim(),
  })

  setSimu(farmerRegistration.simu.trim())
  setStep('phone')
  setMessage('Usajili umefanikiwa. Ingia kwa kutumia namba yako ya simu.')
} catch (err) {
  setError(err.message)
} finally {
  setLoading(false)
}
}

async function handleVerifyOtp(event) {
event.preventDefault()

setError('')
setMessage('')
setLoading(true)

try {
  await verifyOtp(simu, code)

  setMessage('')
  setStep('dashboard')

  await loadDashboardData()
} catch (err) {
  setError(err.message)
} finally {
  setLoading(false)
}

}

function getScheduleDate(crop, schedule) {
if (
!crop?.tarehe_ya_kupanda ||
schedule?.siku === null ||
schedule?.siku === undefined
) {
return null
}

const plantingDate = new Date(
  `${crop.tarehe_ya_kupanda}T00:00:00`
)

const scheduleDate = new Date(plantingDate)

scheduleDate.setDate(
  scheduleDate.getDate() + Number(schedule.siku)
)

return scheduleDate

}

function formatDate(date) {
if (!date) {
return 'Haijawekwa'
}

return date.toLocaleDateString('sw-TZ', {
  day: 'numeric',
  month: 'long',
  year: 'numeric',
})

}

function getCurrentCrop() {
return (
crops.find(
(crop) =>
crop.program_id !== null &&
crop.tarehe_ya_kupanda !== null
) ||
crops.find(
(crop) => crop.tarehe_ya_kupanda !== null
)
)
}

function getTodaySchedule(crop) {
if (!crop) {
return null
}

const today = new Date()

return (
  schedules.find((schedule) => {
    if (schedule.crop_id !== crop.id) {
      return false
    }

    const scheduleDate = getScheduleDate(
      crop,
      schedule
    )

    if (!scheduleDate) {
      return false
    }

    return (
      scheduleDate.getFullYear() === today.getFullYear() &&
      scheduleDate.getMonth() === today.getMonth() &&
      scheduleDate.getDate() === today.getDate()
    )
  }) || null
)

}

function getCropSchedules(crop) {
if (!crop) {
return []
}

return schedules
  .filter(
    (schedule) => schedule.crop_id === crop.id
  )
  .map((schedule) => ({
    ...schedule,
    calculatedDate: getScheduleDate(
      crop,
      schedule
    ),
  }))
  .sort((a, b) => {
    if (!a.calculatedDate) return 1
    if (!b.calculatedDate) return -1

    return (
      a.calculatedDate.getTime() -
      b.calculatedDate.getTime()
    )
  })

}

function getCropCosts(crop) {
if (!crop) {
return []
}

return costs.filter(
  (cost) => cost.crop_id === crop.id
)

}

function getCropHarvests(crop) {
if (!crop) {
return []
}

return harvests.filter(
  (harvest) => harvest.crop_id === crop.id
)

}

function formatMoney(amount) {
const value = Number(amount || 0)

return `Tsh ${value.toLocaleString('sw-TZ')}`

}

function getTotalCropCosts(crop) {
const cropCosts = getCropCosts(crop)

return cropCosts.reduce(
  (total, cost) =>
    total + Number(cost.gharama || 0),
  0
)

}

async function downloadCropPdf(cropId) {
const token = localStorage.getItem('access_token')

const response = await fetch(
  `${API_BASE_URL}/pdf/crop/${cropId}`,
  {
    method: 'GET',
    headers: {
      ...(token
        ? { Authorization: `Bearer ${token}` }
        : {}),
    },
  }
)

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

const blob = await response.blob()

const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')

link.href = url
link.download = `ripoti_zao_${cropId}.pdf`

document.body.appendChild(link)
link.click()
link.remove()

window.URL.revokeObjectURL(url)

}

function getTotalCropHarvestQuantity(crop) {
const cropHarvests = getCropHarvests(crop)

return cropHarvests.reduce(
  (total, harvest) =>
    total + Number(harvest.kiasi || 0),
  0
)

}

function handleCostChange(event) {
const { name, value } = event.target

setCostForm((previous) => ({
  ...previous,
  [name]: value,
}))

}

function handleHarvestChange(event) {
const { name, value } = event.target

setHarvestForm((previous) => ({
  ...previous,
  [name]: value,
}))

}

async function handleSaveCost(event) {
event.preventDefault()

setError('')
setMessage('')

const currentCrop = getCurrentCrop()

if (!currentCrop) {
  setError(
    'Hakuna zao lililopo. Weka zao kwanza.'
  )
  return
}

setSavingCost(true)

try {
  const costData = {
    jina: costForm.jina,
    aina: costForm.aina,
    kiasi: costForm.kiasi,
    unit: costForm.unit,
    gharama: Number(costForm.gharama),
    tarehe: costForm.tarehe,
    maelezo: costForm.maelezo,
    crop_id: currentCrop.id,
  }

  await createCost(costData)

  await loadCosts()

  setCostForm({
    jina: '',
    aina: '',
    kiasi: '',
    unit: '',
    gharama: '',
    tarehe: new Date()
      .toISOString()
      .split('T')[0],
    maelezo: '',
  })

  setMessage(
    'Gharama imehifadhiwa kikamilifu.'
  )

  setActivePage('costs')
} catch (err) {
  setError(err.message)
} finally {
  setSavingCost(false)
}

}

async function handleSaveHarvest(event) {
event.preventDefault()

setError('')
setMessage('')

const currentCrop = getCurrentCrop()

if (!currentCrop) {
  setError(
    'Hakuna zao lililopo. Weka zao kwanza.'
  )
  return
}

if (!harvestForm.kiasi) {
  setError(
    'Weka kiasi cha mavuno.'
  )
  return
}

if (!harvestForm.unit.trim()) {
  setError(
    'Weka kipimo cha mavuno.'
  )
  return
}

setSavingHarvest(true)

try {
  const harvestData = {
    kiasi: Number(harvestForm.kiasi),
    unit: harvestForm.unit,
    tarehe: harvestForm.tarehe,
    maelezo: harvestForm.maelezo,
    crop_id: currentCrop.id,
  }

  await createHarvest(harvestData)

  await loadHarvests()

  setHarvestForm({
    kiasi: '',
    unit: '',
    tarehe: new Date()
      .toISOString()
      .split('T')[0],
    maelezo: '',
  })

  setMessage(
    'Mavuno yamehifadhiwa kikamilifu.'
  )

  setTimeout(() => {
    setMessage('')
  }, 3000)

  setActivePage('harvests')
} catch (err) {
  setError(err.message)
} finally {
  setSavingHarvest(false)
}

}

function handleFarmFormChange(event) {
const { name, value } = event.target

setFarmForm((previous) => ({
  ...previous,
  [name]: value,
}))

}

function handleCropFormChange(event) {
const { name, value } = event.target

setCropForm((previous) => ({
  ...previous,
  [name]: value,
}))

}

async function openFarmCreation() {
setError('')
setMessage('')
setFarmForm({ jina: '', eneo: '', ukubwa: '' })
setCropForm({
  jina: '',
  aina: '',
  msimu: '',
  tarehe_ya_kupanda: '',
  program_id: '',
})
setCreatedFarmId(null)
setFarmCreationStep('farm')
setActivePage('new-farm')
setCropProgramsLoading(true)

try {
  const programs = await getCropPrograms()
  setCropPrograms(programs)
} catch (err) {
  setError(`Imeshindikana kupakia programu za mazao: ${err.message}`)
} finally {
  setCropProgramsLoading(false)
}

}

async function handleCreateFarm(event) {
event.preventDefault()
setError('')
setMessage('')

if (!farmForm.jina.trim() || !farmForm.eneo.trim() || farmForm.ukubwa === '') {
  setError('Jaza jina la shamba, eneo na ukubwa wa shamba.')
  return
}

const farmSize = Number(farmForm.ukubwa)

if (!Number.isFinite(farmSize)) {
  setError('Weka ukubwa sahihi wa shamba kwa namba.')
  return
}

setFarmCreating(true)

try {
  const createdFarm = await createFarm({
    jina: farmForm.jina.trim(),
    eneo: farmForm.eneo.trim(),
    ukubwa: farmSize,
  })

  if (createdFarm?.id === null || createdFarm?.id === undefined) {
    throw new Error('Majibu ya seva hayana kitambulisho cha shamba.')
  }

  setCreatedFarmId(createdFarm.id)
  setFarmCreationStep('crop')
} catch (err) {
  setError(`Imeshindikana kuhifadhi shamba: ${err.message}`)
} finally {
  setFarmCreating(false)
}

}

async function handleCreateCrop(event) {
event.preventDefault()
setError('')
setMessage('')

if (!cropForm.jina.trim() || !cropForm.aina.trim() || !cropForm.msimu.trim()) {
  setError('Jaza jina la zao, aina na msimu.')
  return
}

if (createdFarmId === null || createdFarmId === undefined) {
  setError('Taarifa za shamba hazijapatikana. Anza tena kwa kuhifadhi shamba.')
  return
}

setCropCreating(true)

try {
  const programId = cropForm.program_id
    ? Number(cropForm.program_id)
    : null
  const createdCrop = await createCrop({
    jina: cropForm.jina.trim(),
    aina: cropForm.aina.trim(),
    msimu: cropForm.msimu.trim(),
    farm_id: createdFarmId,
    tarehe_ya_kupanda: cropForm.tarehe_ya_kupanda || null,
    program_id: programId,
  })

  let successMessage = 'Shamba na zao vimehifadhiwa kikamilifu.'

  if (programId !== null && cropForm.tarehe_ya_kupanda) {
    try {
      await generateCropProgramSchedules(createdCrop.id)
    } catch (scheduleError) {
      successMessage = `Shamba na zao vimehifadhiwa, lakini ratiba hazikuweza kutengenezwa: ${scheduleError.message}`
    }
  }

  await loadDashboardData()
  setMessage(successMessage)
  setActivePage('dashboard')
} catch (err) {
  setError(`Imeshindikana kuhifadhi zao: ${err.message}`)
} finally {
  setCropCreating(false)
}

}

function renderBottomNavigation() {
return ( <nav className="bottom-navigation">
<button
type="button"
className={`nav-item ${
            activePage === 'dashboard'
              ? 'active'
              : ''
          }`}
onClick={() => {
setError('')
setMessage('')
setActivePage('dashboard')
}}
> <span>🏠</span> <small>Dashibodi</small> </button>

    <button
      type="button"
      className={`nav-item ${
        activePage === 'schedule'
          ? 'active'
          : ''
      }`}
      onClick={() => {
        setError('')
        setMessage('')
        setActivePage('schedule')
        loadSchedules()
      }}
    >
      <span>📅</span>
      <small>Ratiba</small>
    </button>

    <button
      type="button"
      className={`nav-item ${
        activePage === 'costs' ||
        activePage === 'add-cost'
          ? 'active'
          : ''
      }`}
      onClick={() => {
        setError('')
        setMessage('')
        setActivePage('costs')
        loadCosts()
      }}
    >
      <span>💰</span>
      <small>Gharama</small>
    </button>

    <button
      type="button"
      className={`nav-item ${
        activePage === 'harvests' ||
        activePage === 'add-harvest'
          ? 'active'
          : ''
      }`}
      onClick={() => {
        setError('')
        setMessage('')
        setActivePage('harvests')
        loadHarvests()
      }}
    >
      <span>🌾</span>
      <small>Mavuno</small>
    </button>

    <button
      type="button"
      className={`nav-item ${
        activePage === 'more' ||
        activePage === 'profit-loss' ||
        activePage === 'reports' ||
        activePage === 'reminders' ||
        activePage === 'new-farm'
          ? 'active'
          : ''
      }`}
      onClick={() => {
        setError('')
        setMessage('')
        setActivePage('more')
      }}
    >
      <span>☰</span>
      <small>Zaidi</small>
    </button>
  </nav>
)

}

if (step === 'dashboard') {
const farmer = JSON.parse(
localStorage.getItem('farmer') || '{}'
)

const currentCrop = getCurrentCrop()

let sikuTanguKupanda = null

if (currentCrop?.tarehe_ya_kupanda) {
  const plantingDate = new Date(
    `${currentCrop.tarehe_ya_kupanda}T00:00:00`
  )

  const today = new Date()

  const difference =
    today.getTime() - plantingDate.getTime()

  sikuTanguKupanda = Math.max(
    1,
    Math.floor(
      difference / (1000 * 60 * 60 * 24)
    ) + 1
  )
}

const todaySchedule =
  getTodaySchedule(currentCrop)

const cropSchedules =
  getCropSchedules(currentCrop)

const cropCosts =
  getCropCosts(currentCrop)

const cropHarvests =
  getCropHarvests(currentCrop)

const totalCropCosts =
  getTotalCropCosts(currentCrop)

const totalCropHarvestQuantity =
  getTotalCropHarvestQuantity(currentCrop)

/*
 * =========================
 * ZAIDI
 * =========================
 */

if (activePage === 'more') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Zaidi</h1>

          <p>
            Huduma na taarifa nyingine za shamba lako.
          </p>
        </section>

        <section className="today-task">
          <div className="section-label">
            🔔 KUMBUSHO
          </div>

          <h2>
            Kumbusho za shamba
          </h2>

          <p>
            Angalia kumbusho za leo,
            zilizopita, zinazokuja na
            zilizokamilishwa.
          </p>

          <button
            type="button"
            className="btn-primary auth-button"
            onClick={async () => {
              setError('')
              setMessage('')
              setActivePage('reminders')
              await loadReminderDashboard()
            }}
          >
            🔔 ANGALIA KUMBUSHO
          </button>
        </section>

        <section className="today-task">
          <div className="section-label">
            📊 TAARIFA ZA FEDHA
          </div>

          <button
            type="button"
            className="btn-primary auth-button"
            onClick={async () => {
              setError('')
              setMessage('')
              setActivePage('profit-loss')
              await loadProfitLoss()
            }}
          >
            📊 FAIDA / HASARA
          </button>
        </section>

        <section className="today-task">
          <div className="section-label">
            📄 RIPOTI
          </div>

          <h2>
            Ripoti ya shamba
          </h2>

          <p>
            Angalia taarifa za shamba lako
            na chapisha ripoti.
          </p>

          <button
            type="button"
            className="btn-secondary auth-button"
            onClick={() => {
              setError('')
              setMessage('')
              setActivePage('reports')
            }}
          >
            📄 RIPOTI
          </button>
        </section>

        <section className="today-task">
          <div className="section-label">
            🌱 SHAMBA JIPYA
          </div>

          <button
            type="button"
            className="btn-primary auth-button"
            onClick={openFarmCreation}
          >
            ANZISHA SHAMBA JIPYA
          </button>
        </section>
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

if (activePage === 'new-farm') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Anzisha Shamba Jipya</h1>

          <p>
            {farmCreationStep === 'farm'
              ? 'Weka taarifa za shamba lako.'
              : 'Weka taarifa za zao litakalolimwa.'}
          </p>
        </section>

        <section className="today-task">
          <div className="section-label">
            {farmCreationStep === 'farm'
              ? 'TAARIFA ZA SHAMBA'
              : 'TAARIFA ZA ZAO'}
          </div>

          {farmCreationStep === 'farm' ? (
            <form onSubmit={handleCreateFarm}>
              <label htmlFor="new-farm-jina">
                Jina la shamba
              </label>

              <input
                id="new-farm-jina"
                name="jina"
                type="text"
                value={farmForm.jina}
                onChange={handleFarmFormChange}
                required
              />

              <label htmlFor="new-farm-eneo">
                Eneo
              </label>

              <input
                id="new-farm-eneo"
                name="eneo"
                type="text"
                value={farmForm.eneo}
                onChange={handleFarmFormChange}
                required
              />

              <label htmlFor="new-farm-ukubwa">
                Ukubwa wa shamba (Ekari)
              </label>

              <input
                id="new-farm-ukubwa"
                name="ukubwa"
                type="number"
                step="any"
                value={farmForm.ukubwa}
                onChange={handleFarmFormChange}
                required
              />

              <button
                type="submit"
                className="btn-primary auth-button"
                disabled={farmCreating}
              >
                {farmCreating
                  ? 'INAHIFADHI...'
                  : 'HIFADHI NA ENDELEA'}
              </button>

              <button
                type="button"
                className="btn-secondary auth-button"
                onClick={() => {
                  setError('')
                  setMessage('')
                  setActivePage('more')
                }}
              >
                RUDI KWENYE ZAIDI
              </button>
            </form>
          ) : (
            <form onSubmit={handleCreateCrop}>
              <label htmlFor="new-crop-jina">
                Jina la zao
              </label>

              <input
                id="new-crop-jina"
                name="jina"
                type="text"
                value={cropForm.jina}
                onChange={handleCropFormChange}
                required
              />

              <label htmlFor="new-crop-aina">
                Aina
              </label>

              <input
                id="new-crop-aina"
                name="aina"
                type="text"
                value={cropForm.aina}
                onChange={handleCropFormChange}
                required
              />

              <label htmlFor="new-crop-msimu">
                Msimu
              </label>

              <input
                id="new-crop-msimu"
                name="msimu"
                type="text"
                value={cropForm.msimu}
                onChange={handleCropFormChange}
                required
              />

              <label htmlFor="new-crop-tarehe">
                Tarehe ya kupanda
              </label>

              <input
                id="new-crop-tarehe"
                name="tarehe_ya_kupanda"
                type="date"
                value={cropForm.tarehe_ya_kupanda}
                onChange={handleCropFormChange}
              />

              <label htmlFor="new-crop-program">
                Programu ya zao (si lazima)
              </label>

              <select
                id="new-crop-program"
                name="program_id"
                value={cropForm.program_id}
                onChange={handleCropFormChange}
                disabled={cropProgramsLoading}
              >
                <option value="">
                  {cropProgramsLoading
                    ? 'Inapakia programu...'
                    : 'Chagua programu (si lazima)'}
                </option>
                {cropPrograms.map((program) => (
                  <option
                    key={program.id}
                    value={program.id}
                  >
                    {program.jina}
                  </option>
                ))}
              </select>

              <button
                type="submit"
                className="btn-primary auth-button"
                disabled={cropCreating}
              >
                {cropCreating
                  ? 'INAHIFADHI...'
                  : 'HIFADHI SHAMBA NA ZAO'}
              </button>

              <button
                type="button"
                className="btn-secondary auth-button"
                onClick={() => {
                  setError('')
                  setMessage('')
                  setActivePage('more')
                }}
              >
                RUDI KWENYE ZAIDI
              </button>
            </form>
          )}

          {message && (
            <div className="auth-message">
              {message}
            </div>
          )}

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}
        </section>
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * REMINDERS
 * =========================
 */

if (activePage === 'reminders') {
  const leo =
    reminderDashboard?.reminders?.leo || []

  const zinazokuja =
    reminderDashboard?.reminders?.zinazokuja || []

  const zilizopita =
    reminderDashboard?.reminders?.zilizopita || []

  const zilizokamilika =
    reminderDashboard?.reminders?.zilizokamilika || []

  const counts =
    reminderDashboard?.idadi || {
      leo: 0,
      zinazokuja: 0,
      zilizopita: 0,
      zilizokamilika: 0,
    }

  function renderReminderItem(reminder, showComplete = false) {
    return (
      <div
        className="schedule-item"
        key={reminder.id}
      >
        <div>
          <h2>
            {reminder.ujumbe ||
              'Kumbusho la shamba'}
          </h2>

          {reminder.zao && (
            <p>
              🌽 Zao: {reminder.zao}
            </p>
          )}

          {reminder.shamba && (
            <p>
              🚜 Shamba: {reminder.shamba}
            </p>
          )}

          <p>
            📅 Tarehe: {reminder.tarehe}
          </p>

          <p>
            Hali:{' '}
            {reminder.hali === 'imekamilika'
              ? '✅ Imekamilika'
              : '⏳ Haijakamilika'}
          </p>

          {showComplete &&
            reminder.hali !== 'imekamilika' && (
              <button
                type="button"
                className="btn-primary auth-button"
                disabled={
                  completingReminderId === reminder.id
                }
                onClick={() =>
                  handleCompleteReminder(
                    reminder.id
                  )
                }
              >
                {completingReminderId === reminder.id
                  ? 'INAKAMILISHA...'
                  : '✅ KAMILISHA'}
              </button>
            )}
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Kumbusho</h1>

          <p>
            Fuatilia kazi na taarifa muhimu za
            shamba lako.
          </p>
        </section>

        {message && (
          <div className="auth-message">
            {message}
          </div>
        )}

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        {reminderLoading ? (
          <section className="today-task">
            <p>
              Inapakia kumbusho...
            </p>
          </section>
        ) : (
          <>
            <section className="crop-summary">
              <div className="crop-header">
                <div>
                  <span className="crop-icon">
                    🔔
                  </span>

                  <div>
                    <h2>
                      Muhtasari wa Kumbusho
                    </h2>

                    <p>
                      Taarifa ya kumbusho zako.
                    </p>
                  </div>
                </div>
              </div>

              <div className="crop-progress">
                <div className="progress-info">
                  <strong>
                    Leo
                  </strong>

                  <span>
                    {counts.leo}
                  </span>
                </div>

                <div className="progress-info">
                  <strong>
                    Zinazokuja
                  </strong>

                  <span>
                    {counts.zinazokuja}
                  </span>
                </div>

                <div className="progress-info">
                  <strong>
                    Zilizopita
                  </strong>

                  <span>
                    {counts.zilizopita}
                  </span>
                </div>

                <div className="progress-info">
                  <strong>
                    Zilizokamilika
                  </strong>

                  <span>
                    {counts.zilizokamilika}
                  </span>
                </div>
              </div>
            </section>

            <section className="today-task">
              <div className="section-label">
                🔔 LEO
              </div>

              {leo.length === 0 ? (
                <p>
                  Hakuna kumbusho la leo.
                </p>
              ) : (
                leo.map((reminder) =>
                  renderReminderItem(
                    reminder,
                    true
                  )
                )
              )}
            </section>

            <section className="today-task">
              <div className="section-label">
                ⏰ ZILIZOPITA
              </div>

              {zilizopita.length === 0 ? (
                <p>
                  Hakuna kumbusho lililopita.
                </p>
              ) : (
                zilizopita.map((reminder) =>
                  renderReminderItem(
                    reminder,
                    true
                  )
                )
              )}
            </section>

            <section className="today-task">
              <div className="section-label">
                📅 ZINAZOKUJA
              </div>

              {zinazokuja.length === 0 ? (
                <p>
                  Hakuna kumbusho linalokuja.
                </p>
              ) : (
                zinazokuja.map((reminder) =>
                  renderReminderItem(
                    reminder,
                    true
                  )
                )
              )}
            </section>

            <section className="today-task">
              <div className="section-label">
                ✅ ZILIZOKAMILIKA
              </div>

              {zilizokamilika.length === 0 ? (
                <p>
                  Hakuna kumbusho lililokamilishwa.
                </p>
              ) : (
                zilizokamilika.map((reminder) =>
                  renderReminderItem(
                    reminder,
                    false
                  )
                )
              )}
            </section>
          </>
        )}
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * PROFIT / LOSS
 * =========================
 */

if (activePage === 'profit-loss') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Faida / Hasara</h1>

          <p>
            Angalia hali ya kifedha ya zao lako.
          </p>
        </section>

        {profitLossLoading && (
          <section className="today-task">
            <p>
              Inapakia taarifa za faida / hasara...
            </p>
          </section>
        )}

        {!profitLossLoading && !currentCrop && (
          <section className="today-task">
            <div className="section-label">
              💰 FAIDA / HASARA
            </div>

            <h2>
              Hakuna zao
            </h2>

            <p>
              Weka zao lako kwanza ili
              kuona faida au hasara.
            </p>
          </section>
        )}

        {!profitLossLoading &&
          currentCrop &&
          profitLoss && (
            <section className="today-task">
              <div className="section-label">
                💰 MUHTASARI WA FEDHA
              </div>

              <div className="schedule-item">
                <div>
                  <h2>
                    {profitLoss.zao}
                  </h2>

                  <p>
                    Jumla ya gharama:{' '}
                    {formatMoney(
                      profitLoss.jumla_ya_gharama
                    )}
                  </p>

                  <p>
                    Jumla ya mapato:{' '}
                    {formatMoney(
                      profitLoss.jumla_ya_mapato
                    )}
                  </p>

                  <p>
                    Faida / Hasara:{' '}
                    {formatMoney(
                      profitLoss.faida_au_hasara
                    )}
                  </p>

                  <p>
                    Hali:{' '}
                    {profitLoss.faida_au_hasara > 0
                      ? 'FAIDA'
                      : profitLoss.faida_au_hasara < 0
                        ? 'HASARA'
                        : profitLoss.jumla_ya_gharama === 0 &&
                            profitLoss.jumla_ya_mapato === 0
                          ? 'HAKUNA TAARIFA'
                          : profitLoss.hali === 'faida'
                            ? 'FAIDA'
                            : 'HASARA'}
                  </p>
                </div>
              </div>
            </section>
          )}

        {!profitLossLoading &&
          currentCrop &&
          !profitLoss && (
            <section className="today-task">
              <h2>
                Hakuna taarifa za fedha
              </h2>

              <p>
                Mfumo haujapata taarifa za
                faida au hasara kwa zao hili.
              </p>
            </section>
          )}
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * REPORTS
 * =========================
 */

if (activePage === 'reports') {
  const reportCrop = getCurrentCrop()
  const reportCosts = getCropCosts(reportCrop)
  const reportHarvests = getCropHarvests(reportCrop)
  const reportSchedules = getCropSchedules(reportCrop)
  const reportTotalCosts = getTotalCropCosts(reportCrop)
  const reportTotalHarvest =
    getTotalCropHarvestQuantity(reportCrop)

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Ripoti ya Shamba</h1>

          <p>
            Muhtasari wa taarifa za shamba lako.
          </p>
        </section>

        {reportCrop && (
          <section className="today-task">
            <button
              type="button"
              className="btn-primary auth-button"
              onClick={async () => {
                setError('')
                setMessage('')

                try {
                  await downloadCropPdf(reportCrop.id)

                  setMessage(
                    'Ripoti imepakuliwa kwa mafanikio.'
                  )
                } catch (err) {
                  setError(err.message)
                }
              }}
            >
              📥 DOWNLOAD REPORT
            </button>
          </section>
        )}

        {!reportCrop && (
          <section className="today-task">
            <div className="section-label">
              📄 RIPOTI
            </div>

            <h2>
              Hakuna taarifa za zao
            </h2>

            <p>
              Weka zao lenye tarehe ya kupanda
              ili kutengeneza ripoti.
            </p>
          </section>
        )}

        {reportCrop && (
          <>
            <section className="today-task">
              <div className="section-label">
                🌾 TAARIFA ZA ZAO
              </div>

              <h2>
                {reportCrop.jina}
              </h2>

              <p>
                Aina: {reportCrop.aina}
              </p>

              <p>
                Msimu: {reportCrop.msimu}
              </p>

              <p>
                Tarehe ya kupanda:{' '}
                {reportCrop.tarehe_ya_kupanda
                  ? formatDate(
                      new Date(
                        `${reportCrop.tarehe_ya_kupanda}T00:00:00`
                      )
                    )
                  : 'Haijawekwa'}
              </p>
            </section>

            <section className="today-task">
              <div className="section-label">
                📅 RATIBA
              </div>

              <h2>
                Ratiba ya zao
              </h2>

              {reportSchedules.length === 0 ? (
                <p>
                  Hakuna ratiba iliyopatikana.
                </p>
              ) : (
                reportSchedules.map((schedule) => (
                  <div
                    className="schedule-item"
                    key={schedule.id}
                  >
                    <div>
                      <h3>
                        {schedule.jina}
                      </h3>

                      <p>
                        {schedule.maelezo ||
                          'Hakuna maelezo'}
                      </p>

                      <p>
                        Tarehe:{' '}
                        {formatDate(
                          schedule.calculatedDate
                        )}
                      </p>
                    </div>
                  </div>
                ))
              )}
            </section>

            <section className="today-task">
              <div className="section-label">
                💰 GHARAMA
              </div>

              <h2>
                {formatMoney(reportTotalCosts)}
              </h2>

              {reportCosts.length === 0 ? (
                <p>
                  Hakuna gharama zilizorekodiwa.
                </p>
              ) : (
                reportCosts.map((cost) => (
                  <div
                    className="schedule-item"
                    key={cost.id}
                  >
                    <div>
                      <h3>
                        {cost.jina}
                      </h3>

                      <p>
                        {cost.aina || ''}
                      </p>

                      <p>
                        Kiasi: {cost.kiasi}{' '}
                        {cost.unit || ''}
                      </p>

                      <p>
                        Gharama:{' '}
                        {formatMoney(cost.gharama)}
                      </p>

                      <p>
                        Tarehe: {cost.tarehe}
                      </p>
                    </div>
                  </div>
                ))
              )}
            </section>

            <section className="today-task">
              <div className="section-label">
                🌽 MAVUNO
              </div>

              <h2>
                Jumla: {reportTotalHarvest}
              </h2>

              {reportHarvests.length === 0 ? (
                <p>
                  Hakuna mavuno yaliyorekodiwa.
                </p>
              ) : (
                reportHarvests.map((harvest) => (
                  <div
                    className="schedule-item"
                    key={harvest.id}
                  >
                    <div>
                      <h3>
                        {harvest.kiasi}{' '}
                        {harvest.unit || ''}
                      </h3>

                      <p>
                        {harvest.maelezo ||
                          'Hakuna maelezo'}
                      </p>

                      <p>
                        Tarehe: {harvest.tarehe}
                      </p>
                    </div>
                  </div>
                ))
              )}
            </section>

            <section className="today-task">
              <div className="section-label">
                📊 FAIDA / HASARA
              </div>

              {!profitLoss ? (
                <p>
                  Hakuna taarifa za faida
                  au hasara zilizopatikana.
                </p>
              ) : (
                <>
                  <h2>
                    {formatMoney(
                      profitLoss.faida_au_hasara
                    )}
                  </h2>

                  <p>
                    Jumla ya gharama:{' '}
                    {formatMoney(
                      profitLoss.jumla_ya_gharama
                    )}
                  </p>

                  <p>
                    Jumla ya mapato:{' '}
                    {formatMoney(
                      profitLoss.jumla_ya_mapato
                    )}
                  </p>

                  <p>
                    Hali:{' '}
                    {profitLoss.faida_au_hasara > 0
                      ? 'FAIDA'
                      : profitLoss.faida_au_hasara < 0
                        ? 'HASARA'
                        : profitLoss.jumla_ya_gharama === 0 &&
                            profitLoss.jumla_ya_mapato === 0
                          ? 'HAKUNA TAARIFA'
                          : profitLoss.hali === 'faida'
                            ? 'FAIDA'
                            : 'HASARA'}
                  </p>
                </>
              )}
            </section>
          </>
        )}
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * RATIBA
 * =========================
 */

if (activePage === 'schedule') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Ratiba ya Zao</h1>

          <p>
            Angalia kazi zilizopangwa kwa zao lako.
          </p>
        </section>

        {scheduleLoading && (
          <section className="today-task">
            <p>
              Inapakia ratiba...
            </p>
          </section>
        )}

        {!scheduleLoading && currentCrop && (
          <section className="crop-summary">
            <div className="crop-header">
              <div>
                <span className="crop-icon">
                  🌽
                </span>

                <div>
                  <h2>
                    {currentCrop.jina}
                  </h2>

                  <p>
                    Aina: {currentCrop.aina}
                  </p>
                </div>
              </div>
            </div>

            <div className="crop-progress">
              <div className="progress-info">
                <strong>
                  {currentCrop.msimu}
                </strong>

                <span>
                  {cropSchedules.length} kazi
                </span>
              </div>

              <p>
                Tarehe ya kupanda:{' '}
                {currentCrop.tarehe_ya_kupanda}
              </p>
            </div>
          </section>
        )}

        {!scheduleLoading &&
          currentCrop &&
          cropSchedules.length > 0 && (
            <section className="today-task">
              <div className="section-label">
                📅 RATIBA
              </div>

              {cropSchedules.map((schedule) => (
                <div
                  key={schedule.id}
                  className="schedule-item"
                >
                  <div>
                    <h2>
                      {schedule.jina ||
                        'Kazi ya shamba'}
                    </h2>

                    <p>
                      {schedule.maelezo ||
                        'Hakuna maelezo ya kazi.'}
                    </p>

                    <small>
                      📅{' '}
                      {formatDate(
                        schedule.calculatedDate
                      )}
                    </small>
                  </div>
                </div>
              ))}
            </section>
          )}

        {!scheduleLoading &&
          currentCrop &&
          cropSchedules.length === 0 && (
            <section className="today-task">
              <div className="section-label">
                📅 RATIBA
              </div>

              <h2>
                Hakuna ratiba
              </h2>

              <p>
                Kwa sasa hakuna kazi
                iliyopangwa kwa zao hili.
              </p>
            </section>
          )}

        {!scheduleLoading && !currentCrop && (
          <section className="today-task">
            <div className="section-label">
              📅 RATIBA
            </div>

            <h2>
              Hakuna zao
            </h2>

            <p>
              Weka zao lako kwanza ili
              kuona ratiba yake.
            </p>
          </section>
        )}
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * ADD COST
 * =========================
 */

if (activePage === 'add-cost') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Weka Gharama</h1>

          <p>
            Weka gharama iliyotumika kwenye zao lako.
          </p>
        </section>

        {currentCrop && (
          <section className="crop-summary">
            <div className="crop-header">
              <div>
                <span className="crop-icon">
                  🌽
                </span>

                <div>
                  <h2>
                    {currentCrop.jina}
                  </h2>

                  <p>
                    Aina: {currentCrop.aina}
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        <section className="today-task">
          <div className="section-label">
            💰 TAARIFA ZA GHARAMA
          </div>

          <form onSubmit={handleSaveCost}>
            <label htmlFor="jina">
              Jina la gharama
            </label>

            <input
              id="jina"
              name="jina"
              type="text"
              value={costForm.jina}
              onChange={handleCostChange}
              placeholder="Mfano: Mbolea"
              required
            />

            <label htmlFor="aina">
              Aina
            </label>

            <input
              id="aina"
              name="aina"
              type="text"
              value={costForm.aina}
              onChange={handleCostChange}
              placeholder="Mfano: Mbolea"
              required
            />

            <label htmlFor="kiasi">
              Kiasi
            </label>

            <input
              id="kiasi"
              name="kiasi"
              type="text"
              value={costForm.kiasi}
              onChange={handleCostChange}
              placeholder="Mfano: 1"
              required
            />

            <label htmlFor="unit">
              Unit
            </label>

            <input
              id="unit"
              name="unit"
              type="text"
              value={costForm.unit}
              onChange={handleCostChange}
              placeholder="Mfano: mfuko"
              required
            />

            <label htmlFor="gharama">
              Gharama (Tsh)
            </label>

            <input
              id="gharama"
              name="gharama"
              type="number"
              min="0"
              value={costForm.gharama}
              onChange={handleCostChange}
              onWheel={(event) => event.currentTarget.blur()}
              placeholder="Mfano: 100000"
              required
            />

            <label htmlFor="tarehe">
              Tarehe
            </label>

            <input
              id="tarehe"
              name="tarehe"
              type="date"
              value={costForm.tarehe}
              onChange={handleCostChange}
              required
            />

            <label htmlFor="maelezo">
              Maelezo
            </label>

            <textarea
              id="maelezo"
              name="maelezo"
              value={costForm.maelezo}
              onChange={handleCostChange}
              placeholder="Andika maelezo ya gharama..."
              rows="4"
            />

            <button
              type="submit"
              className="btn-primary auth-button"
              disabled={savingCost}
            >
              {savingCost
                ? 'INAHIFADHI...'
                : 'HIFADHI GHARAMA'}
            </button>

            <button
              type="button"
              className="btn-secondary auth-button"
              onClick={() => {
                setError('')
                setMessage('')
                setActivePage('costs')
              }}
            >
              RUDI KWENYE GHARAMA
            </button>
          </form>

          {message && (
            <div className="auth-message">
              {message}
            </div>
          )}

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}
        </section>
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * ADD HARVEST
 * =========================
 */

if (activePage === 'add-harvest') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Weka Mavuno</h1>

          <p>
            Rekodi mavuno yaliyopatikana kwenye zao lako.
          </p>
        </section>

        {currentCrop && (
          <section className="crop-summary">
            <div className="crop-header">
              <div>
                <span className="crop-icon">
                  🌽
                </span>

                <div>
                  <h2>
                    {currentCrop.jina}
                  </h2>

                  <p>
                    Aina: {currentCrop.aina}
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        <section className="today-task">
          <div className="section-label">
            🌾 TAARIFA ZA MAVUNO
          </div>

          <form onSubmit={handleSaveHarvest}>
            <label htmlFor="harvest-kiasi">
              Kiasi cha mavuno
            </label>

            <input
              id="harvest-kiasi"
              name="kiasi"
              type="number"
              min="0"
              step="any"
              value={harvestForm.kiasi}
              onChange={handleHarvestChange}
              placeholder="Mfano: 20"
              required
            />

            <label htmlFor="harvest-unit">
              Kipimo
            </label>

            <input
              id="harvest-unit"
              name="unit"
              type="text"
              value={harvestForm.unit}
              onChange={handleHarvestChange}
              placeholder="Mfano: gunia"
              required
            />

            <label htmlFor="harvest-tarehe">
              Tarehe
            </label>

            <input
              id="harvest-tarehe"
              name="tarehe"
              type="date"
              value={harvestForm.tarehe}
              onChange={handleHarvestChange}
              required
            />

            <label htmlFor="harvest-maelezo">
              Maelezo
            </label>

            <textarea
              id="harvest-maelezo"
              name="maelezo"
              value={harvestForm.maelezo}
              onChange={handleHarvestChange}
              placeholder="Andika maelezo ya mavuno..."
              rows="4"
            />

            <button
              type="submit"
              className="btn-primary auth-button"
              disabled={savingHarvest}
            >
              {savingHarvest
                ? 'INAHIFADHI...'
                : 'HIFADHI MAVUNO'}
            </button>

            <button
              type="button"
              className="btn-secondary auth-button"
              onClick={() => {
                setError('')
                setMessage('')
                setActivePage('harvests')
              }}
            >
              RUDI KWENYE MAVUNO
            </button>
          </form>

          {message && (
            <div className="auth-message">
              {message}
            </div>
          )}

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}
        </section>
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * GHARAMA
 * =========================
 */

if (activePage === 'costs') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Gharama</h1>

          <p>
            Fuatilia gharama za zao lako.
          </p>
        </section>

        {costLoading && (
          <section className="today-task">
            <p>
              Inapakia gharama...
            </p>
          </section>
        )}

        {!costLoading && currentCrop && (
          <>
            <section className="crop-summary">
              <div className="crop-header">
                <div>
                  <span className="crop-icon">
                    🌽
                  </span>

                  <div>
                    <h2>
                      {currentCrop.jina}
                    </h2>

                    <p>
                      Aina: {currentCrop.aina}
                    </p>
                  </div>
                </div>
              </div>

              <div className="crop-progress">
                <div className="progress-info">
                  <strong>
                    Jumla ya gharama
                  </strong>

                  <span>
                    {cropCosts.length} rekodi
                  </span>
                </div>

                <h2>
                  {formatMoney(
                    totalCropCosts
                  )}
                </h2>
              </div>
            </section>

            <section className="today-task">
              <div className="section-label">
                💰 GHARAMA
              </div>

              <button
                type="button"
                className="btn-primary auth-button"
                onClick={() => {
                  setError('')
                  setMessage('')
                  setActivePage('add-cost')
                }}
              >
                + WEKA GHARAMA
              </button>

              {cropCosts.length === 0 ? (
                <>
                  <h2>
                    Hakuna gharama
                  </h2>

                  <p>
                    Kwa sasa hakuna gharama
                    zilizowekwa kwa zao hili.
                  </p>
                </>
              ) : (
                cropCosts.map((cost) => (
                  <div
                    key={cost.id}
                    className="schedule-item"
                  >
                    <div>
                      <h2>
                        {cost.jina ||
                          'Gharama ya shamba'}
                      </h2>

                      {cost.aina && (
                        <p>
                          Aina: {cost.aina}
                        </p>
                      )}

                      {cost.maelezo && (
                        <p>
                          {cost.maelezo}
                        </p>
                      )}

                      <p>
                        Kiasi:{' '}
                        {cost.kiasi || 0}{' '}
                        {cost.unit || ''}
                      </p>

                      <strong>
                        💰{' '}
                        {formatMoney(
                          cost.gharama
                        )}
                      </strong>

                      <small>
                        📅 {cost.tarehe}
                      </small>
                    </div>
                  </div>
                ))
              )}
            </section>
          </>
        )}

        {!costLoading && !currentCrop && (
          <section className="today-task">
            <div className="section-label">
              💰 GHARAMA
            </div>

            <h2>
              Hakuna zao
            </h2>

            <p>
              Weka zao lako kwanza ili
              kuona gharama zake.
            </p>
          </section>
        )}
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * MAVUNO
 * =========================
 */

if (activePage === 'harvests') {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="brand">
            🌱 MKULIMA SMART ASSISTANT
          </div>

          <p className="welcome">
            Karibu, {farmer.jina || 'Mkulima'}
          </p>
        </div>
      </header>

      <main className="dashboard">
        <section className="dashboard-title">
          <h1>Mavuno</h1>

          <p>
            Fuatilia mavuno yaliyopatikana kwenye zao lako.
          </p>
        </section>

        {harvestLoading && (
          <section className="today-task">
            <p>
              Inapakia mavuno...
            </p>
          </section>
        )}

        {!harvestLoading && currentCrop && (
          <>
            <section className="crop-summary">
              <div className="crop-header">
                <div>
                  <span className="crop-icon">
                    🌽
                  </span>

                  <div>
                    <h2>
                      {currentCrop.jina}
                    </h2>

                    <p>
                      Aina: {currentCrop.aina}
                    </p>
                  </div>
                </div>
              </div>

              <div className="crop-progress">
                <div className="progress-info">
                  <strong>
                    Jumla ya mavuno
                  </strong>

                  <span>
                    {cropHarvests.length} rekodi
                  </span>
                </div>

                <h2>
                  {totalCropHarvestQuantity}
                </h2>

                {cropHarvests.length > 0 && (
                  <p>
                    Kiasi cha jumla kwa vipimo
                    vilivyorekodiwa.
                  </p>
                )}
              </div>
            </section>

            <section className="today-task">
              <div className="section-label">
                🌾 MAVUNO
              </div>

              <button
                type="button"
                className="btn-primary auth-button"
                onClick={() => {
                  setError('')
                  setMessage('')

                  setHarvestForm({
                    kiasi: '',
                    unit: '',
                    tarehe: new Date()
                      .toISOString()
                      .split('T')[0],
                    maelezo: '',
                  })

                  setActivePage('add-harvest')
                }}
              >
                + WEKA MAVUNO
              </button>

              {message && (
                <div className="auth-message">
                  {message}
                </div>
              )}

              {error && (
                <div className="auth-error">
                  {error}
                </div>
              )}

              {cropHarvests.length === 0 ? (
                <>
                  <h2>
                    Hakuna mavuno
                  </h2>

                  <p>
                    Kwa sasa hakuna mavuno
                    yaliyorekodiwa kwa zao hili.
                  </p>
                </>
              ) : (
                cropHarvests.map((harvest) => (
                  <div
                    key={harvest.id}
                    className="schedule-item"
                  >
                    <div>
                      <h2>
                        {harvest.kiasi}{' '}
                        {harvest.unit}
                      </h2>

                      {harvest.maelezo && (
                        <p>
                          {harvest.maelezo}
                        </p>
                      )}

                      <small>
                        📅 {harvest.tarehe}
                      </small>
                    </div>
                  </div>
                ))
              )}
            </section>
          </>
        )}

        {!harvestLoading && !currentCrop && (
          <section className="today-task">
            <div className="section-label">
              🌾 MAVUNO
            </div>

            <h2>
              Hakuna zao
            </h2>

            <p>
              Weka zao lako kwanza ili
              kurekodi mavuno.
            </p>
          </section>
        )}
      </main>

      {renderBottomNavigation()}
    </div>
  )
}

/*
 * =========================
 * DASHBOARD
 * =========================
 */

return (
  <div className="app">
    <header className="app-header">
      <div>
        <div className="brand">
          🌱 MKULIMA SMART ASSISTANT
        </div>

        <p className="welcome">
          Karibu, {farmer.jina || 'Mkulima'}
        </p>
      </div>
    </header>

    <main className="dashboard">
      <section className="dashboard-title">
        <h1>Dashibodi</h1>

        <p>
          Fuatilia maendeleo ya zao lako na kazi za shamba.
        </p>
      </section>

      {message && (
        <div className="auth-message">
          {message}
        </div>
      )}

      {dashboardLoading && (
        <section className="crop-summary">
          <p>
            Inapakia taarifa za mazao...
          </p>
        </section>
      )}

      {!dashboardLoading && currentCrop && (
        <section className="crop-summary">
          <div className="crop-header">
            <div>
              <span className="crop-icon">
                🌽
              </span>

              <div>
                <h2>
                  {currentCrop.jina}
                </h2>

                <p>
                  Aina: {currentCrop.aina}
                </p>
              </div>
            </div>
          </div>

          <div className="crop-progress">
            <div className="progress-info">
              <strong>
                {sikuTanguKupanda !== null
                  ? `Siku ya ${sikuTanguKupanda}`
                  : 'Tarehe ya kupanda haipo'}
              </strong>

              <span>
                {currentCrop.msimu}
              </span>
            </div>

            <p>
              Tarehe ya kupanda:{' '}
              {currentCrop.tarehe_ya_kupanda
                ? currentCrop.tarehe_ya_kupanda
                : 'Haijawekwa'}
            </p>

            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: '0%' }}
              />
            </div>
          </div>
        </section>
      )}

      {!dashboardLoading && !currentCrop && (
        <section className="crop-summary">
          <div className="crop-header">
            <div>
              <span className="crop-icon">
                🌱
              </span>

              <div>
                <h2>
                  Hakuna zao lililowekwa
                </h2>

                <p>
                  Ongeza zao lako ili kuanza
                  kufuatilia maendeleo yake.
                </p>

                <button
                  type="button"
                  className="btn-primary auth-button"
                  onClick={openFarmCreation}
                >
                  🌱 ANZISHA SHAMBA JIPYA
                </button>
              </div>
            </div>
          </div>
        </section>
      )}

      <section className="today-task">
        <div className="section-label">
          🧪 KAZI YA LEO
        </div>

        {todaySchedule ? (
          <>
            <h2>
              {todaySchedule.jina ||
                'Kazi ya shamba'}
            </h2>

            <p>
              {todaySchedule.maelezo ||
                'Kuna kazi iliyopangwa kwa leo.'}
            </p>

            <div className="task-date">
              📅{' '}
              {formatDate(
                getScheduleDate(
                  currentCrop,
                  todaySchedule
                )
              )}
            </div>
          </>
        ) : (
          <>
            <h2>
              Hakuna kazi ya leo
            </h2>

            <p>
              Kwa sasa hakuna kazi iliyopangwa
              kwa zao hili leo.
            </p>
          </>
        )}
      </section>

      <section className="today-task">
        <div className="section-label">
          🔔 KUMBUSHO
        </div>

        {reminderLoading ? (
          <p>
            Inapakia kumbusho...
          </p>
        ) : reminderDashboard?.idadi?.leo > 0 ? (
          <>
            <h2>
              Una {reminderDashboard.idadi.leo} kumbusho la leo
            </h2>

            <p>
              {reminderDashboard.reminders.leo[0]?.ujumbe ||
                'Kuna kazi ya kufuatilia leo.'}
            </p>

            <button
              type="button"
              className="btn-secondary auth-button"
              onClick={async () => {
                setError('')
                setMessage('')
                setActivePage('reminders')
                await loadReminderDashboard()
              }}
            >
              ANGALIA KUMBUSHO ZOTE
            </button>
          </>
        ) : (
          <>
            <h2>
              Hakuna kumbusho la leo
            </h2>

            <p>
              Kwa sasa hakuna kumbusho linalokusubiri leo.
            </p>

            <button
              type="button"
              className="btn-secondary auth-button"
              onClick={async () => {
                setError('')
                setMessage('')
                setActivePage('reminders')
                await loadReminderDashboard()
              }}
            >
              ANGALIA KUMBUSHO
            </button>
          </>
        )}
      </section>

      <section className="cost-summary">
        <div className="cost-icon">
          💰
        </div>

        <div>
          <p>
            Gharama hadi sasa
          </p>

          <h2>
            {cropCosts.length > 0
              ? formatMoney(totalCropCosts)
              : 'Zitaonyeshwa hapa'}
          </h2>
        </div>
      </section>

      {currentCrop && profitLoss && (
        <section className="cost-summary">
          <div className="cost-icon">
            📊
          </div>

          <div>
            <p>
              {profitLoss.hali === 'faida'
                ? 'Faida hadi sasa'
                : 'Hasara hadi sasa'}
            </p>

            <h2>
              {formatMoney(
                profitLoss.faida_au_hasara
              )}
            </h2>
          </div>
        </section>
      )}
    </main>

    {renderBottomNavigation()}
  </div>
)

}

/*

* =========================
* LOGIN / OTP
* =========================
  */

return ( <div className="app"> <main className="auth-container"> <section className="auth-card"> <div className="auth-logo">
🌱 </div>

      <h1>
        MKULIMA SMART ASSISTANT
      </h1>

      <p className="auth-subtitle">
        Msaidizi wako wa kilimo
      </p>

      {step === 'phone' && (
        <>
          <form onSubmit={handleRequestOtp}>
            <h2>
              Ingia kwenye mfumo
            </h2>

            <p>
              Weka namba yako ya simu ili
              kuendelea.
            </p>

            <label htmlFor="simu">
              Namba ya simu
            </label>

            <input
              id="simu"
              type="tel"
              value={simu}
              onChange={(event) =>
                setSimu(event.target.value)
              }
              placeholder="0712345678"
              required
            />

            <button
              type="submit"
              className="btn-primary auth-button"
              disabled={loading}
            >
              {loading
                ? 'INATUMA...'
                : 'TUMA OTP'}
            </button>
          </form>

          <button
            type="button"
            className="btn-secondary auth-button"
            onClick={() => {
              setError('')
              setMessage('')
              setStep('register')
            }}
          >
            JISAJILI KAMA MKULIMA
          </button>
        </>
      )}

      {step === 'register' && (
        <form onSubmit={handleRegisterFarmer}>
          <h2>
            Usajili wa Mkulima
          </h2>

          <label htmlFor="registration-jina">
            Jina la mkulima
          </label>

          <input
            id="registration-jina"
            name="jina"
            type="text"
            value={farmerRegistration.jina}
            onChange={handleFarmerRegistrationChange}
            required
          />

          <label htmlFor="registration-simu">
            Namba ya simu
          </label>

          <input
            id="registration-simu"
            name="simu"
            type="tel"
            value={farmerRegistration.simu}
            onChange={handleFarmerRegistrationChange}
            required
          />

          <label htmlFor="registration-eneo">
            Eneo
          </label>

          <input
            id="registration-eneo"
            name="eneo"
            type="text"
            value={farmerRegistration.eneo}
            onChange={handleFarmerRegistrationChange}
            required
          />

          <button
            type="submit"
            className="btn-primary auth-button"
            disabled={loading}
          >
            {loading ? 'INASAJILI...' : 'JISAJILI'}
          </button>

          <button
            type="button"
            className="btn-secondary auth-button"
            onClick={() => {
              setError('')
              setMessage('')
              setStep('phone')
            }}
          >
            RUDI KWENYE KUINGIA
          </button>
        </form>
      )}

      {step === 'otp' && (
        <form onSubmit={handleVerifyOtp}>
          <h2>
            Thibitisha OTP
          </h2>

          <p>
            Ingiza OTP uliyotumiwa kwenye simu
            yako.
          </p>

          <label htmlFor="code">
            OTP
          </label>

          <input
            id="code"
            type="text"
            value={code}
            onChange={(event) =>
              setCode(event.target.value)
            }
            placeholder="123456"
            maxLength="6"
            required
          />

          <button
            type="submit"
            className="btn-primary auth-button"
            disabled={loading}
          >
            {loading
              ? 'INATHIBITISHA...'
              : 'INGIA'}
          </button>

          <button
            type="button"
            className="btn-secondary auth-button"
            onClick={() => {
              setStep('phone')
              setCode('')
              setMessage('')
              setError('')
            }}
          >
            BADILI NAMBA
          </button>
        </form>
      )}

      {message && (
        <div className="auth-message">
          {message}
        </div>
      )}
      {error && (
        <div className="auth-error">
          {error}
        </div>
      )}
    </section>
    </main>
</div>
  )
}

export default App