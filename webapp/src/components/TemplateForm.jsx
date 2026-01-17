import { useState, useEffect } from 'react'
import { ArrowLeft, Download, Loader2, FolderTree } from 'lucide-react'
import { generateZip } from '../utils/zipGenerator'

function TemplateForm({ template, registry, onBack }) {
  const [templateConfig, setTemplateConfig] = useState(null)
  const [values, setValues] = useState({})
  const [loading, setLoading] = useState(true)
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState(null)

  const repoUrl = template.repo || registry.default_repo
  const branch = template.branch || 'main'

  useEffect(() => {
    fetchTemplateConfig()
  }, [template])

  async function fetchTemplateConfig() {
    try {
      setLoading(true)
      const configUrl = `https://raw.githubusercontent.com/${getRepoPath(repoUrl)}/${branch}/${template.path}/template.json`
      const response = await fetch(configUrl)
      if (!response.ok) throw new Error('Failed to fetch template config')
      const config = await response.json()
      setTemplateConfig(config)

      // Initialize values with defaults
      const initialValues = {}
      if (config.prompts) {
        Object.entries(config.prompts).forEach(([key, prompt]) => {
          initialValues[key] = prompt.default || ''
        })
      }
      setValues(initialValues)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function getRepoPath(url) {
    // Extract owner/repo from GitHub URL
    const match = url.match(/github\.com\/([^\/]+\/[^\/]+)/)
    return match ? match[1] : url
  }

  function handleChange(key, value) {
    setValues(prev => ({ ...prev, [key]: value }))
  }

  function formatValue(value, format) {
    if (!format || format === 'text') return value
    if (format === 'snake_case') {
      return value.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '')
    }
    return value
  }

  async function handleDownload() {
    try {
      setDownloading(true)
      setError(null)

      // Format values according to their format rules
      const formattedValues = {}
      if (templateConfig.prompts) {
        Object.entries(templateConfig.prompts).forEach(([key, prompt]) => {
          formattedValues[key] = formatValue(values[key], prompt.format)
        })
      }

      await generateZip({
        repoUrl,
        branch,
        templatePath: template.path,
        templateConfig,
        values: formattedValues,
        projectName: values.project_name || values.package_name || template.id,
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setDownloading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to templates
      </button>

      {/* Template Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">{template.name}</h2>
        <p className="text-gray-600 mb-4">{template.description}</p>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <FolderTree className="w-4 h-4" />
          <span>{template.path}</span>
        </div>
      </div>

      {/* Form */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold mb-4">Configure Your Project</h3>

        {templateConfig?.prompts && Object.entries(templateConfig.prompts).map(([key, prompt]) => (
          <div key={key} className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {prompt.label}
            </label>
            <input
              type="text"
              value={values[key] || ''}
              onChange={(e) => handleChange(key, e.target.value)}
              placeholder={prompt.default}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            {prompt.format && prompt.format !== 'text' && (
              <p className="text-xs text-gray-500 mt-1">Format: {prompt.format}</p>
            )}
          </div>
        ))}

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleDownload}
          disabled={downloading}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {downloading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Download className="w-5 h-5" />
              Download Project
            </>
          )}
        </button>
      </div>
    </div>
  )
}

export default TemplateForm
