import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import EventsList from './pages/EventsList'
import Register from './pages/Register'
import AdminReports from './pages/AdminReports'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation Header */}
        <nav className="bg-blue-600 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="flex-shrink-0 flex items-center">
                  <h1 className="text-white text-xl font-bold">
                    Webknot Campus Events
                  </h1>
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  to="/"
                  className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Events
                </Link>
                <Link
                  to="/register"
                  className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Register
                </Link>
                <Link
                  to="/reports"
                  className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Reports
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<EventsList />} />
            <Route path="/register" element={<Register />} />
            <Route path="/reports" element={<AdminReports />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
