/**
 * Extract project ID from slug (assuming slug format includes ID at the end)
 * @param {string} slug - The slug containing the ID (e.g., "ems-project-3")
 * @returns {number|null} - Extracted project ID or null if not found
 */
export function extractIdFromSlug(slug) {
  if (!slug) return null
  
  // Try to extract ID from slug (assuming it ends with -ID)
  const parts = slug.split('-')
  const lastPart = parts[parts.length - 1]
  const id = parseInt(lastPart, 10)
  
  return isNaN(id) ? null : id
}