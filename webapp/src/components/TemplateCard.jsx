import { ArrowRight, Tag } from 'lucide-react'

const categoryIcons = {
  react: '⚛️',
  python: '🐍',
  php: '🐘',
  other: '📦',
}

function TemplateCard({ template, onSelect }) {
  const icon = categoryIcons[template.category] || categoryIcons.other

  return (
    <div
      onClick={onSelect}
      className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer group"
    >
      <div className="flex items-start justify-between mb-3">
        <span className="text-2xl">{icon}</span>
        <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
      </div>

      <h3 className="font-semibold text-gray-900 mb-1">{template.name}</h3>
      <p className="text-sm text-gray-500 mb-4 line-clamp-2">{template.description}</p>

      {template.tags && template.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {template.tags.slice(0, 4).map(tag => (
            <span
              key={tag}
              className="inline-flex items-center gap-1 px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full"
            >
              <Tag className="w-3 h-3" />
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

export default TemplateCard
