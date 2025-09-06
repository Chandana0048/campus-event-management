import React, { useState, useEffect } from 'react'
import axios from 'axios'
import EventCard from '../components/EventCard'

const API_BASE_URL = 'http://localhost:8000'

function EventsList() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({
    college_id: '',
    event_type: ''
  })

  useEffect(() => {
    fetchEvents()
  }, [filters])

  const fetchEvents = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (filters.college_id) params.append('college_id', filters.college_id)
      if (filters.event_type) params.append('event_type', filters.event_type)
      
      const response = await axios.get(`${API_BASE_URL}/events/?${params}`)
      setEvents(response.data)
    } catch (err) {
      setError('Failed to fetch events')
      console.error('Error fetching events:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
        {error}
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Campus Events</h1>
        
        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Filter Events</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="event_type" className="block text-sm font-medium text-gray-700 mb-2">
                Event Type
              </label>
              <select
                id="event_type"
                value={filters.event_type}
                onChange={(e) => handleFilterChange('event_type', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Types</option>
                <option value="workshop">Workshop</option>
                <option value="seminar">Seminar</option>
                <option value="competition">Competition</option>
                <option value="conference">Conference</option>
              </select>
            </div>
            <div>
              <label htmlFor="college_id" className="block text-sm font-medium text-gray-700 mb-2">
                College ID
              </label>
              <input
                type="number"
                id="college_id"
                value={filters.college_id}
                onChange={(e) => handleFilterChange('college_id', e.target.value)}
                placeholder="Enter college ID"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Events Grid */}
      {events.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No events found matching your criteria.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      )}
    </div>
  )
}

export default EventsList
