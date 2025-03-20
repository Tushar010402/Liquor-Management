import { useState, useCallback, useEffect } from 'react';
import useDataFetching from './useDataFetching';
import { PaginatedResponse } from '../services';

export interface TableFilter {
  [key: string]: any;
}

export interface SortConfig {
  field: string;
  direction: 'asc' | 'desc';
}

interface UseTableDataOptions<T, F extends TableFilter> {
  fetchFunction: (params: F & {
    page: number;
    limit: number;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
  }) => Promise<PaginatedResponse<T>>;
  initialFilters?: F;
  initialSort?: SortConfig;
  initialPageSize?: number;
  dependencies?: any[];
}

/**
 * Custom hook for handling paginated table data with filtering and sorting
 * @param options Table data options
 * @returns Table data, pagination state, and handlers
 */
function useTableData<T, F extends TableFilter>({
  fetchFunction,
  initialFilters = {} as F,
  initialSort,
  initialPageSize = 10,
  dependencies = [],
}: UseTableDataOptions<T, F>) {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(initialPageSize);
  const [filters, setFilters] = useState<F>(initialFilters);
  const [sort, setSort] = useState<SortConfig | undefined>(initialSort);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(1);

  // Create the fetch params by combining pagination, filters, and sort
  const createFetchParams = useCallback(() => {
    const params: any = {
      ...filters,
      page,
      limit: pageSize,
    };

    if (sort) {
      params.sort_by = sort.field;
      params.sort_order = sort.direction;
    }

    return params;
  }, [filters, page, pageSize, sort]);

  // Fetch function that will be passed to useDataFetching
  const fetchData = useCallback(async () => {
    const params = createFetchParams();
    const response = await fetchFunction(params);
    
    // Update pagination state based on response
    setTotalItems(response.meta.total);
    setTotalPages(response.meta.last_page);
    
    return response.data;
  }, [createFetchParams, fetchFunction]);

  // Use the data fetching hook
  const { data, isLoading, error, refetch } = useDataFetching<T[]>({
    fetchFunction: fetchData,
    dependencies: [...dependencies, page, pageSize, JSON.stringify(filters), JSON.stringify(sort)],
  });

  // Reset to page 1 when filters or page size changes
  useEffect(() => {
    setPage(1);
  }, [filters, pageSize]);

  // Handle page change
  const handlePageChange = useCallback((newPage: number) => {
    setPage(newPage);
  }, []);

  // Handle page size change
  const handlePageSizeChange = useCallback((newPageSize: number) => {
    setPageSize(newPageSize);
  }, []);

  // Handle filter change
  const handleFilterChange = useCallback((newFilters: F) => {
    setFilters(newFilters);
  }, []);

  // Handle sort change
  const handleSortChange = useCallback((field: string, direction: 'asc' | 'desc') => {
    setSort({ field, direction });
  }, []);

  // Clear all filters
  const clearFilters = useCallback(() => {
    setFilters(initialFilters);
  }, [initialFilters]);

  return {
    data,
    isLoading,
    error,
    page,
    pageSize,
    totalItems,
    totalPages,
    filters,
    sort,
    handlePageChange,
    handlePageSizeChange,
    handleFilterChange,
    handleSortChange,
    clearFilters,
    refetch,
  };
}

export default useTableData;