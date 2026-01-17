import { Package } from 'lucide-react'

function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <Package className="w-8 h-8 text-blue-600" />
          <div>
            <h1 className="text-xl font-bold text-gray-900">Boilerplate Manager</h1>
            <p className="text-sm text-gray-500">Browse and download project templates</p>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
