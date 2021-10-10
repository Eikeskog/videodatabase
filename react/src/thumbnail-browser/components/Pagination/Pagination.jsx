import React from 'react';
import TablePagination from '@material-ui/core/TablePagination';
import PropTypes from 'prop-types';
import styles from './Pagination.module.css';
import { defaultLabelDisplayedRows, defaultLabelRowsPerPage, defaultRowsPerPageOptions } from './utils';

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

  return (
    <TablePagination
      className={styles.pagination}
      style={{ zIndex: 100 }}
      component="div"
      count={itemsCount}
      page={currentPage - 1}
      onPageChange={onPageChange}
      rowsPerPage={viewPerPage}
      onRowsPerPageChange={handleChangeRowsPerPage}
      labelRowsPerPage={defaultLabelRowsPerPage}
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
