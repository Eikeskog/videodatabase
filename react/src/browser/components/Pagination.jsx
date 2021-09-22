import React from 'react';
import TablePagination from '@material-ui/core/TablePagination';
import PropTypes from 'prop-types';

// skrive om denne, ikke bruke material ui
const Pagination = ({
  setViewPerPage,
  handlePageChange,
  itemsCount,
  currentPage,
  viewPerPage,
}) => {
  const onPageChange = (_, newPage) => {
    handlePageChange(parseInt(newPage, 10) + 1);
  };

  const handleChangeRowsPerPage = (event) => {
    setViewPerPage(parseInt(event.target.value, 10));
  };

  const defaultLabelDisplayedRows = ({
    from, to, count,
  }) => `${from}-${to} av ${count !== -1 ? count : `mer enn ${to}`}`;

  const defaultRowsPerPageOptions = [8, 20, 50, 100, 250];

  return (
    <div style={{
      position: 'fixed', bottom: '0', marginLeft: 'auto', width: '100%', opacity: 0.8, zIndex: 4000,
    }}
    >
      <TablePagination
        style={{
          position: 'fixed', bottom: '0', marginLeft: 'auto', width: '100%', backgroundColor: 'black', color: 'yellow', zIndex: 5000,
        }}
        component="div"
        count={itemsCount}
        page={(currentPage - 1)}
        onPageChange={onPageChange}
        rowsPerPage={viewPerPage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        labelRowsPerPage="Antall per side"
        labelDisplayedRows={defaultLabelDisplayedRows}
        rowsPerPageOptions={defaultRowsPerPageOptions}
      />
    </div>

  );
};

Pagination.propTypes = {
  setViewPerPage: PropTypes.func,
  handlePageChange: PropTypes.func,
  itemsCount: PropTypes.number,
  currentPage: PropTypes.number,
  viewPerPage: PropTypes.number,
};

Pagination.defaultProps = {
  setViewPerPage: () => null,
  handlePageChange: () => null,
  itemsCount: 0,
  currentPage: 1,
  viewPerPage: 20,
};

export default Pagination;
