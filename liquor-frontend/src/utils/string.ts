/**
 * Truncate a string to a specified length and add ellipsis if needed
 * @param str String to truncate
 * @param maxLength Maximum length
 * @returns Truncated string
 */
export const truncate = (str: string, maxLength: number): string => {
  if (!str) return '';
  if (str.length <= maxLength) return str;
  return `${str.substring(0, maxLength)}...`;
};

/**
 * Capitalize the first letter of a string
 * @param str String to capitalize
 * @returns Capitalized string
 */
export const capitalize = (str: string): string => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * Capitalize the first letter of each word in a string
 * @param str String to capitalize
 * @returns Capitalized string
 */
export const capitalizeEachWord = (str: string): string => {
  if (!str) return '';
  return str
    .split(' ')
    .map((word) => capitalize(word))
    .join(' ');
};

/**
 * Convert a string to title case
 * @param str String to convert
 * @returns Title case string
 */
export const toTitleCase = (str: string): string => {
  if (!str) return '';
  
  // List of minor words that should not be capitalized unless they are the first or last word
  const minorWords = ['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'from', 'by', 'with'];
  
  const words = str.toLowerCase().split(' ');
  
  // Always capitalize the first and last word
  for (let i = 0; i < words.length; i++) {
    if (i === 0 || i === words.length - 1 || !minorWords.includes(words[i])) {
      words[i] = capitalize(words[i]);
    }
  }
  
  return words.join(' ');
};

/**
 * Convert a camelCase string to a human-readable string
 * @param str String to convert
 * @returns Human-readable string
 */
export const camelCaseToHuman = (str: string): string => {
  if (!str) return '';
  
  // Add a space before each uppercase letter and capitalize the first letter
  const result = str.replace(/([A-Z])/g, ' $1');
  return capitalize(result);
};

/**
 * Convert a snake_case string to a human-readable string
 * @param str String to convert
 * @returns Human-readable string
 */
export const snakeCaseToHuman = (str: string): string => {
  if (!str) return '';
  
  // Replace underscores with spaces and capitalize each word
  return capitalizeEachWord(str.replace(/_/g, ' '));
};

/**
 * Convert a kebab-case string to a human-readable string
 * @param str String to convert
 * @returns Human-readable string
 */
export const kebabCaseToHuman = (str: string): string => {
  if (!str) return '';
  
  // Replace hyphens with spaces and capitalize each word
  return capitalizeEachWord(str.replace(/-/g, ' '));
};

/**
 * Generate initials from a name
 * @param name Name to generate initials from
 * @param maxInitials Maximum number of initials to generate
 * @returns Initials
 */
export const getInitials = (name: string, maxInitials: number = 2): string => {
  if (!name) return '';
  
  const words = name.split(' ').filter((word) => word.length > 0);
  
  if (words.length === 0) return '';
  if (words.length === 1) return words[0].charAt(0).toUpperCase();
  
  // Get the first letter of each word, up to maxInitials
  return words
    .slice(0, maxInitials)
    .map((word) => word.charAt(0).toUpperCase())
    .join('');
};

/**
 * Format a phone number
 * @param phone Phone number to format
 * @param format Format to use (e.g., 'XXX-XXX-XXXX')
 * @returns Formatted phone number
 */
export const formatPhone = (phone: string, format: string = 'XXX-XXX-XXXX'): string => {
  if (!phone) return '';
  
  // Remove all non-digit characters
  const digits = phone.replace(/\D/g, '');
  
  // Replace X with digits
  let result = format;
  for (let i = 0; i < digits.length && result.includes('X'); i++) {
    result = result.replace('X', digits[i]);
  }
  
  // Remove any remaining X
  result = result.replace(/X/g, '');
  
  return result;
};

export default {
  truncate,
  capitalize,
  capitalizeEachWord,
  toTitleCase,
  camelCaseToHuman,
  snakeCaseToHuman,
  kebabCaseToHuman,
  getInitials,
  formatPhone,
};