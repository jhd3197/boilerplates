import JSZip from 'jszip'
import { saveAs } from 'file-saver'

/**
 * Fetches template files from GitHub, applies variable replacements, and downloads as ZIP
 */
export async function generateZip({ repoUrl, branch, templatePath, templateConfig, values, projectName }) {
  const repoPath = getRepoPath(repoUrl)
  const zip = new JSZip()

  // Fetch the file tree from GitHub API
  const treeUrl = `https://api.github.com/repos/${repoPath}/git/trees/${branch}?recursive=1`
  const treeResponse = await fetch(treeUrl)

  if (!treeResponse.ok) {
    throw new Error('Failed to fetch repository structure')
  }

  const treeData = await treeResponse.json()

  // Filter files that belong to this template
  const templateFiles = treeData.tree.filter(item => {
    return item.type === 'blob' &&
           item.path.startsWith(templatePath + '/') &&
           !item.path.endsWith('template.json') &&
           !item.path.endsWith('CLAUDE.md')
  })

  // Fetch and process each file
  const fetchPromises = templateFiles.map(async (file) => {
    const rawUrl = `https://raw.githubusercontent.com/${repoPath}/${branch}/${file.path}`
    const response = await fetch(rawUrl)

    if (!response.ok) {
      console.warn(`Failed to fetch: ${file.path}`)
      return null
    }

    // Get relative path within template
    let relativePath = file.path.replace(templatePath + '/', '')

    // Apply rename rules
    relativePath = applyRenames(relativePath, templateConfig.rename, values)

    // Check if this is a text file that should have replacements
    const content = await response.text()
    const processedContent = applyReplacements(content, file.path, templateConfig.replace, values)

    return { path: relativePath, content: processedContent }
  })

  const files = await Promise.all(fetchPromises)

  // Add files to ZIP
  files.filter(Boolean).forEach(file => {
    zip.file(file.path, file.content)
  })

  // Generate and download ZIP
  const blob = await zip.generateAsync({ type: 'blob' })
  const filename = formatProjectName(projectName) + '.zip'
  saveAs(blob, filename)
}

/**
 * Extract owner/repo from GitHub URL
 */
function getRepoPath(url) {
  const match = url.match(/github\.com\/([^\/]+\/[^\/]+)/)
  return match ? match[1] : url
}

/**
 * Apply rename rules to file/folder paths
 */
function applyRenames(path, renameRules, values) {
  if (!renameRules) return path

  let result = path
  Object.entries(renameRules).forEach(([oldName, newPattern]) => {
    const newName = replaceVariables(newPattern, values)
    result = result.replace(oldName, newName)
  })
  return result
}

/**
 * Apply replacement rules to file content
 */
function applyReplacements(content, filePath, replaceRules, values) {
  if (!replaceRules || replaceRules.length === 0) return content

  let result = content

  replaceRules.forEach(rule => {
    // Check if file matches the glob pattern
    if (matchesGlob(filePath, rule.glob)) {
      Object.entries(rule.values).forEach(([oldValue, newPattern]) => {
        const newValue = replaceVariables(newPattern, values)
        // Use regex to replace all occurrences
        const regex = new RegExp(escapeRegex(oldValue), 'g')
        result = result.replace(regex, newValue)
      })
    }
  })

  return result
}

/**
 * Replace {{variable}} patterns with actual values
 */
function replaceVariables(template, values) {
  return template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
    return values[key] !== undefined ? values[key] : match
  })
}

/**
 * Simple glob matching for common patterns
 */
function matchesGlob(filePath, glob) {
  // Handle common glob patterns
  // **/*.{ext1,ext2} - match any file with these extensions
  // **/* - match everything
  // *.ext - match files with extension in current dir

  if (glob === '**/*') return true

  // Handle {ext1,ext2} syntax
  const braceMatch = glob.match(/\*\*\/\*\.\{([^}]+)\}/)
  if (braceMatch) {
    const extensions = braceMatch[1].split(',')
    const fileExt = filePath.split('.').pop()
    return extensions.includes(fileExt)
  }

  // Handle simple *.ext
  const simpleMatch = glob.match(/\*\.(\w+)$/)
  if (simpleMatch) {
    return filePath.endsWith('.' + simpleMatch[1])
  }

  // Handle **/*.ext
  const recursiveMatch = glob.match(/\*\*\/\*\.(\w+)$/)
  if (recursiveMatch) {
    return filePath.endsWith('.' + recursiveMatch[1])
  }

  return false
}

/**
 * Escape special regex characters
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * Format project name for filename
 */
function formatProjectName(name) {
  return name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
}
