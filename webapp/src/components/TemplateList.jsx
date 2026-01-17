import { useState } from 'react'
import TemplateCard from './TemplateCard'
import { Search } from 'lucide-react'

function TemplateList({ templates, onSelect }) {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')

  const categories = ['all', ...new Set(templates.map(t => t.category))]

  const filtered = templates.filter(t => {
    const matchesSearch = t.name.toLowerCase().includes(search.toLowerCase()) ||
      t.description.toLowerCase().includes(search.toLowerCase()) ||
      t.tags?.some(tag => tag.toLowerCase().includes(search.toLowerCase()))
    const matchesCategory = category === 'all' || t.category === category
    return matchesSearch && matchesCategory
  })

  // Group by category
  const grouped = filtered.reduce((acc, t) => {
    const cat = t.category || 'other'
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(t)
    return acc
  }, {})

  return (
    <div>
      {/* Search and Filter */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search templates..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                category === cat
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Template Grid */}
      {Object.entries(grouped).map(([cat, catTemplates]) => (
        <div key={cat} className="mb-8">
          <h2 className="text-lg font-semibold text-gray-700 mb-4 capitalize">{cat}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {catTemplates.map(template => (
              <TemplateCard
                key={template.id}
                template={template}
                onSelect={() => onSelect(template)}
              />
            ))}
          </div>
        </div>
      ))}

      {filtered.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No templates found matching your criteria.</p>
        </div>
      )}
    </div>
  )
}

export default TemplateList
