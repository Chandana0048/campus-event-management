import React, { useState, useEffect } from 'react'
import axios from 'axios'
import ReportsTable from '../components/ReportsTable'

const API_BASE_URL = 'http://localhost:8000'

function AdminReports() {
  const [popularityReport, setPopularityReport] = useState([])
  const [participationReport, setParticipationReport] = useState([])
  const [topStudentsReport, setTopStudentsReport] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('popularity')

  useEffect(() => {
    fetchAllReports()
  }, [])

  const fetchAllReports = async () => {
    try {
      setLoading(true)
      
      const [popularityRes, participationRes, topStudentsRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/reports/event-popularity`),
        axios.get(`${API_BASE_URL}/reports/student-participation`),
        axios.get(`${API_BASE_URL}/reports/top-active-students?limit=10`)
      ])
      
      setPopularityReport(popularityRes.data)
      setParticipationReport(participationRes.data)
      setTopStudentsReport(topStudentsRes.data)
    } catch (err) {
      setError('Failed to fetch reports')
      console.error('Error fetching reports:', err)
    } finally {
      setLoading(false)
    }
  }

  const tabs = [
    { id: 'popularity', name: 'Event Popularity', data: popularityReport },
    { id: 'participation', name: 'Student Participation', data: participationReport },
    { id: 'topStudents', name: 'Top Active Students', data: topStudentsReport }
  ]

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
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Reports</h1>
        <p className="text-gray-600">Analytics and insights for campus events</p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.name} ({tab.data.length})
            </button>
          ))}
        </nav>
      </div>

      {/* Report Content */}
      {activeTab === 'popularity' && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Event Popularity Report</h2>
          <p className="text-gray-600 mb-4">
            Events ranked by number of registrations. Shows registration count, attendance count, and average rating.
          </p>
          <ReportsTable
            data={popularityReport}
            columns={[
              { key: 'title', label: 'Event Title' },
              { key: 'event_type', label: 'Type' },
              { key: 'registration_count', label: 'Registrations' },
              { key: 'attendance_count', label: 'Attendance' },
              { key: 'avg_rating', label: 'Avg Rating', format: (value) => value ? value.toFixed(1) : 'N/A' }
            ]}
          />
        </div>
      )}

      {activeTab === 'participation' && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Student Participation Report</h2>
          <p className="text-gray-600 mb-4">
            Students ranked by number of events attended. Shows total registrations and actual attendance.
          </p>
          <ReportsTable
            data={participationReport}
            columns={[
              { key: 'name', label: 'Student Name' },
              { key: 'email', label: 'Email' },
              { key: 'events_attended', label: 'Events Attended' },
              { key: 'total_registrations', label: 'Total Registrations' }
            ]}
          />
        </div>
      )}

      {activeTab === 'topStudents' && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Active Students</h2>
          <p className="text-gray-600 mb-4">
            Most active students by attendance count, including their average feedback ratings.
          </p>
          <ReportsTable
            data={topStudentsReport}
            columns={[
              { key: 'name', label: 'Student Name' },
              { key: 'email', label: 'Email' },
              { key: 'events_attended', label: 'Events Attended' },
              { key: 'avg_rating_given', label: 'Avg Rating Given', format: (value) => value ? value.toFixed(1) : 'N/A' }
            ]}
          />
        </div>
      )}
    </div>
  )
}

export default AdminReports
