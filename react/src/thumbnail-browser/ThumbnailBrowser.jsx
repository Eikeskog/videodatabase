import React, { useState } from 'react';
import PropTypes from 'prop-types';
import ThumbnailGrid from './components/ThumbnailGrid/ThumbnailGrid';
import Pagination from './components/Pagination/Pagination';

const getPageCount = (itemsCount, viewPerPage) => (
  Math.floor((itemsCount + viewPerPage - 1) / viewPerPage)
);

const ThumbnailBrowser = ({ openModal }) => {
  const [state, setState] = useState({
    currentPage: 1,
    viewPerPage: 20,
    itemsCount: 0,
  });

  const handlePageChange = (pageNumber) => setState(
    (prevState) => ({
      ...prevState,
      currentPage: pageNumber,
    }),
  );

  const setItemsCount = (count) => setState(
    (prevState) => ({
      ...prevState,
      itemsCount: count,
    }),
  );

  const handleChangeViewPerPage = (newPerPage) => {
    const newMaxPage = getPageCount(state.itemsCount, newPerPage);
    setState(
      (prevState) => ({
        ...prevState,
        currentPage:
          prevState.currentPage > newMaxPage
            ? newMaxPage
            : prevState.currentPage,
        viewPerPage: newPerPage,
      }),
    );
  };

  return (
    <>
      <ThumbnailGrid
        currentPage={state.currentPage}
        viewPerPage={state.viewPerPage}
        itemsCount={state.itemsCount}
        setItemsCount={setItemsCount}
        setCurrentPage={handlePageChange}
        toggleModal={openModal}
      />

      <Pagination
        currentPage={state.currentPage}
        viewPerPage={state.viewPerPage}
        itemsCount={state.itemsCount}
        handlePageChange={handlePageChange}
        setViewPerPage={handleChangeViewPerPage}
      />
    </>
  );
};

ThumbnailBrowser.propTypes = {
  openModal: PropTypes.func,
};

ThumbnailBrowser.defaultProps = {
  openModal: null,
};

const MemoizedThumbnailBrowser = React.memo(ThumbnailBrowser);

export default MemoizedThumbnailBrowser;
