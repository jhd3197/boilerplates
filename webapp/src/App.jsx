import { useState, useEffect } from 'react'
import TemplateList from './components/TemplateList'
import TemplateForm from './components/TemplateForm'
import Header from './components/Header'

const REGISTRY_URL = 'https://raw.githubusercontent.com/jhd3197/boilerplates/main/templates-registry.json'

function App() {
  const [registry, setRegistry] = useState(null)
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchRegistry()
  }, [])

  async function fetchRegistry() {
    try {
      setLoading(true)
      const response = await fetch(REGISTRY_URL)
      if (!response.ok) throw new Error('Failed to fetch registry')
      const data = await response.json()
      setRegistry(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleSelectTemplate(template) {
    setSelectedTemplate(template)
  }

  function handleBack() {
    setSelectedTemplate(null)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-4">Error: {error}</p>
          <button
            onClick={fetchRegistry}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <Header />
      <main className="max-w-6xl mx-auto px-4 py-8">
        {selectedTemplate ? (
          <TemplateForm
            template={selectedTemplate}
            registry={registry}
            onBack={handleBack}
          />
        ) : (
          <TemplateList
            templates={registry?.templates || []}
            onSelect={handleSelectTemplate}
          />
        )}
      </main>
    </div>
  )
}

export default App
