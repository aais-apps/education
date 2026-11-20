export function __(message, args = []) {
  const translated = window.educationTranslations?.[message] || message
  return translated.replace(/\{(\d+)\}/g, (token, index) => args[index] ?? token)
}
