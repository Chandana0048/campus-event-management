import React, { useState } from 'react'
import axios from 'axios'
import RegisterForm from '../components/RegisterForm'

const API_BASE_URL = 'http://localhost:8000'

function Register() {
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)

  const handleRegister = async (formData) => {
    setLoading(true)
    setError(null)
    
    try {
      // First, create the student
      const studentResponse = await axios.post(`${API_BASE_URL}/students/`, {
        name: formData.name,
        email: formData.email,
        student_id: formData.studentId,
        college_id: formData.collegeId || null
      })
      
      // Then register for the event
      await axios.post(`${API_BASE_URL}/events/${formData.eventId}/register`, {
        student_id: studentResponse.data.id
      })
      
      setSuccess(true)
    } catch (err) {
      if (err.response?.status === 409) {
        setError('You are already registered for this event.')
      } else if (err.response?.status === 404) {
        setError('Event not found.')
      } else {
        setError('Registration failed. Please try again.')
      }
      console.error('Registration error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="px-4 py-6 sm:px-0">
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded mb-4">
          <h3 className="font-medium">Registration Successful!</h3>
          <p>You have been successfully registered for the event.</p>
        </div>
        <button
          onClick={() => {
            setSuccess(false)
            setError(null)
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
        >
          Register for Another Event
        </button>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Register for Event</h1>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}
        
        <RegisterForm onSubmit={handleRegister} loading={loading} />
      </div>
    </div>
  )
}

export default Register
