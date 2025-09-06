import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

function RegisterForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    studentId: '',
    collegeId: '',
    eventId: ''
  })
  const [events, setEvents] = useState([])
  const [loadingEvents, setLoadingEvents] = useState(true)

  useEffect(() => {
    fetchEvents()
  }, [])

  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/events/`)
      setEvents(response.data)
    } catch (err) {
      console.error('Error fetching events:', err)
    } finally {
      setLoadingEvents(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  if (loadingEvents) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="eventId" className="block text-sm font-medium text-gray-700 mb-2">
          Select Event *
        </label>
        <select
          id="eventId"
          name="eventId"
          value={formData.eventId}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Choose an event...</option>
          {events.map((event) => (
            <option key={event.id} value={event.id}>
              {event.title} - {new Date(event.date).toLocaleDateString()}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
          Full Name *
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter your full name"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
          Email Address *
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter your email address"
        />
      </div>

      <div>
        <label htmlFor="studentId" className="block text-sm font-medium text-gray-700 mb-2">
          Student ID *
        </label>
        <input
          type="text"
          id="studentId"
          name="studentId"
          value={formData.studentId}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter your student ID"
        />
      </div>

      <div>
        <label htmlFor="collegeId" className="block text-sm font-medium text-gray-700 mb-2">
          College ID (Optional)
        </label>
        <input
          type="number"
          id="collegeId"
          name="collegeId"
          value={formData.collegeId}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter your college ID"
        />
      </div>

      <div className="pt-4">
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-200 font-medium"
        >
          {loading ? 'Registering...' : 'Register for Event'}
        </button>
      </div>
    </form>
  )
}

export default RegisterForm
