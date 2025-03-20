import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Tooltip,
} from '@mui/material';
import { DataGrid, GridColDef, GridRowsProp, GridToolbar } from '@mui/x-data-grid';
import { motion } from 'framer-motion';

interface DataTableProps {
  title: string;
  rows: GridRowsProp;
  columns: GridColDef[];
  loading?: boolean;
  actionText?: string;
  onActionClick?: () => void;
  pageSize?: number;
  height?: number | string;
  delay?: number;
}

const DataTable: React.FC<DataTableProps> = ({
  title,
  rows,
  columns,
  loading = false,
  actionText = 'Add New',
  onActionClick,
  pageSize = 10,
  height = 400,
  delay = 0,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" component="h2">
              {title}
            </Typography>
            {onActionClick && (
              <Button variant="contained" size="small" onClick={onActionClick}>
                {actionText}
              </Button>
            )}
          </Box>
          <Box sx={{ height, width: '100%' }}>
            <DataGrid
              rows={rows}
              columns={columns}
              loading={loading}
              initialState={{
                pagination: {
                  paginationModel: { pageSize, page: 0 },
                },
              }}
              pageSizeOptions={[5, 10, 25, 50, 100]}
              disableRowSelectionOnClick
              slots={{ toolbar: GridToolbar }}
              slotProps={{
                toolbar: {
                  showQuickFilter: true,
                  quickFilterProps: { debounceMs: 500 },
                },
              }}
              sx={{
                '& .MuiDataGrid-cell:hover': {
                  color: 'primary.main',
                },
                '& .MuiDataGrid-columnHeaders': {
                  backgroundColor: 'background.default',
                  borderRadius: 1,
                },
              }}
            />
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default DataTable;