/**
 * Group an array of objects by a key
 * @param array Array to group
 * @param key Key to group by
 * @returns Grouped object
 */
export const groupBy = <T>(array: T[], key: keyof T): Record<string, T[]> => {
  return array.reduce((result, item) => {
    const groupKey = String(item[key]);
    if (!result[groupKey]) {
      result[groupKey] = [];
    }
    result[groupKey].push(item);
    return result;
  }, {} as Record<string, T[]>);
};

/**
 * Sort an array of objects by a key
 * @param array Array to sort
 * @param key Key to sort by
 * @param direction Sort direction
 * @returns Sorted array
 */
export const sortBy = <T>(
  array: T[],
  key: keyof T,
  direction: 'asc' | 'desc' = 'asc'
): T[] => {
  return [...array].sort((a, b) => {
    if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
    if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
    return 0;
  });
};

/**
 * Filter an array of objects by a key and value
 * @param array Array to filter
 * @param key Key to filter by
 * @param value Value to filter by
 * @returns Filtered array
 */
export const filterBy = <T>(array: T[], key: keyof T, value: any): T[] => {
  return array.filter((item) => item[key] === value);
};

/**
 * Search an array of objects by a key and search term
 * @param array Array to search
 * @param key Key to search by
 * @param searchTerm Search term
 * @returns Filtered array
 */
export const searchBy = <T>(array: T[], key: keyof T, searchTerm: string): T[] => {
  const term = searchTerm.toLowerCase();
  return array.filter((item) => {
    const value = String(item[key]).toLowerCase();
    return value.includes(term);
  });
};

/**
 * Search an array of objects by multiple keys and search term
 * @param array Array to search
 * @param keys Keys to search by
 * @param searchTerm Search term
 * @returns Filtered array
 */
export const searchByMultiple = <T>(array: T[], keys: (keyof T)[], searchTerm: string): T[] => {
  const term = searchTerm.toLowerCase();
  return array.filter((item) => {
    return keys.some((key) => {
      const value = String(item[key]).toLowerCase();
      return value.includes(term);
    });
  });
};

/**
 * Get unique items from array
 * @param array Array to get unique items from
 * @returns Array with unique items
 */
export const unique = <T>(array: T[]): T[] => {
  return Array.from(new Set(array));
};

/**
 * Remove duplicates from an array of objects by a key
 * @param array Array to deduplicate
 * @param key Key to deduplicate by
 * @returns Deduplicated array
 */
export const uniqueBy = <T>(array: T[], key: keyof T): T[] => {
  const seen = new Set();
  return array.filter((item) => {
    const value = item[key];
    if (seen.has(value)) {
      return false;
    }
    seen.add(value);
    return true;
  });
};

/**
 * Sum an array of numbers
 * @param array Array to sum
 * @returns Sum
 */
export const sum = (array: number[]): number => {
  return array.reduce((total, num) => total + num, 0);
};

/**
 * Sum a property of an array of objects
 * @param array Array to sum
 * @param key Key to sum by
 * @returns Sum
 */
export const sumBy = <T>(array: T[], key: keyof T): number => {
  return array.reduce((total, item) => {
    const value = Number(item[key]);
    return total + (isNaN(value) ? 0 : value);
  }, 0);
};

/**
 * Find the maximum value in an array of objects by a key
 * @param array Array to search
 * @param key Key to search by
 * @returns Maximum value
 */
export const maxBy = <T>(array: T[], key: keyof T): number => {
  if (array.length === 0) return 0;
  return Math.max(...array.map((item) => Number(item[key])));
};

/**
 * Find the minimum value in an array of objects by a key
 * @param array Array to search
 * @param key Key to search by
 * @returns Minimum value
 */
export const minBy = <T>(array: T[], key: keyof T): number => {
  if (array.length === 0) return 0;
  return Math.min(...array.map((item) => Number(item[key])));
};

/**
 * Calculate the average of an array of numbers
 * @param array Array to average
 * @returns Average
 */
export const average = (array: number[]): number => {
  if (array.length === 0) return 0;
  return sum(array) / array.length;
};

/**
 * Calculate the average of a property of an array of objects
 * @param array Array to average
 * @param key Key to average by
 * @returns Average
 */
export const averageBy = <T>(array: T[], key: keyof T): number => {
  if (array.length === 0) return 0;
  return sumBy(array, key) / array.length;
};

export default {
  groupBy,
  sortBy,
  filterBy,
  searchBy,
  searchByMultiple,
  unique,
  uniqueBy,
  sum,
  sumBy,
  maxBy,
  minBy,
  average,
  averageBy,
};