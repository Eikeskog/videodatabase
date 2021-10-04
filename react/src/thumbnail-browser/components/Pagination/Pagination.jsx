import React from 'react';
import TablePagination from '@material-ui/core/TablePagination';
import PropTypes from 'prop-types';

const defaultLabelDisplayedRows = ({
  from, to, count,
}) => `${from}-${to} av ${count !== -1 ? count : `mer enn ${to}`}`;

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

  const defaultRowsPerPageOptions = [8, 20, 50, 100, 250];

  return (
    <TablePagination
      style={{
        position: 'fixed',
        bottom: '0',
        marginLeft: 'auto',
        width: '100%',
        backgroundColor: 'black',
        color: 'yellow',
        zIndex: 100,
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
