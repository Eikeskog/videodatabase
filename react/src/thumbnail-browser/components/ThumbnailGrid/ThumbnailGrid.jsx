import React, {
  useEffect, useState, useCallback,
} from 'react';
import { Grid } from '@material-ui/core';
import PropTypes from 'prop-types';
import renderCards from './utils';
import { useUserContext } from '../../../common/contexts/UserContext/UserContext';
import { useSearchfilters } from '../../contexts/SearchfiltersContext';
import urls from '../../../dev_urls';

import styles from './ThumbnailGrid.module.css';

const baseUrl = urls.VIDEOITEMS;

const fetchData = ({
  authorizedFetch,
  handleResponse,
  handleError,
  restApiParams,
  currentPage,
  viewPerPage,
}) => {
  authorizedFetch({
    method: 'get',
    url: baseUrl,
    params: {
      ...restApiParams,
      ...{
        page: currentPage,
        perpage: viewPerPage,
      },
    },
    handleResponse,
    handleError,
  });
};

const ThumbnailGrid = ({
  toggleModal,
  viewPerPage,
  currentPage,
  setItemsCount,
  setCurrentPage,
}) => {
  const [data, setData] = useState([]);
  const { restApiParams } = useSearchfilters();

  const {
    useAuthorizedFetch: { authorizedFetch, isFetching },
  } = useUserContext();

  const handleResponse = useCallback((response) => {
    setItemsCount(parseInt(response?.count, 10));
    setData(() => renderCards(response?.results, toggleModal));
  }, []);

  const handleError = useCallback((error) => { console.log(error); }, []);

  useEffect(() => {
    fetchData({
      authorizedFetch,
      handleResponse,
      handleError,
      restApiParams,
      currentPage,
      viewPerPage,
    });
  }, [viewPerPage, currentPage]);

  useEffect(() => {
    if (currentPage !== 1) setCurrentPage(1);
    fetchData({
      authorizedFetch,
      handleResponse,
      handleError,
      restApiParams,
      currentPage,
      viewPerPage,
    });
  }, [restApiParams]);

  return (
    <div className={`${styles.wrapper}`}>
      <Grid
        container
        spacing={2}
        className={`${styles.grid}`}
      >

        {isFetching === baseUrl
          ? <p>loading...</p>
          : data}

      </Grid>
    </div>
  );
};

const MemoizedThumbnailGrid = React.memo(ThumbnailGrid);

export default MemoizedThumbnailGrid;

ThumbnailGrid.propTypes = {
  viewPerPage: PropTypes.number,
  currentPage: PropTypes.number,
  setItemsCount: PropTypes.func,
  setCurrentPage: PropTypes.func,
  toggleModal: PropTypes.func,
};

ThumbnailGrid.defaultProps = {
  toggleModal: null,
  setCurrentPage: null,
  viewPerPage: 0,
  currentPage: 0,
  setItemsCount: null,
};
