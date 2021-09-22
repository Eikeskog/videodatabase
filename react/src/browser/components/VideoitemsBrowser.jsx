import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import ThumbnailCard from './ThumbnailCard/ThumbnailCard';
import Pagination from './Pagination';
import { useSearchfilters } from '../contexts/SearchfiltersContext';
import { localeDateStringNorwegianBugFix/* , getThumbnailUrl */ } from '../../common/utils/utils';

import styles from './VideoitemsBrowser.module.css';

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

export default function VideoitemsBrowser({ toggleModal }) {
  const { restApiParams } = useSearchfilters();

  const [items, setItems] = useState([]);
  const [itemsCount, setItemsCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [viewPerPage, setViewPerPage] = useState(20);

  const calculateMaxPage = (itemsPerPage) => Math.floor(
    (itemsCount + itemsPerPage - 1) / itemsPerPage,
  );

  const handleChangeViewPerPage = (newPerPage) => {
    const newMaxPage = calculateMaxPage(newPerPage);
    if (currentPage > newMaxPage) setCurrentPage(newMaxPage);
    setViewPerPage(newPerPage);
  };

  const handlePageChange = (pageNumber) => setCurrentPage(pageNumber);

  const fetchItems = async () => {
    const params = {
      ...restApiParams,
      ...{
        page: currentPage,
        perpage: viewPerPage,
        // orderby: orderBy,
      },
    };
    const { data } = await axios.get('http://localhost:8000/api/videoitems/', { params });

    setItemsCount(() => parseInt(data?.count, 10));

    setItems(() => data?.results?.map((item) => (
      <ThumbnailCard
        key={item.videoitem_id}
        toggleModal={toggleModal}
        videoitemId={item.videoitem_id}
        duration={item.exif_duration_sec}
        locationDisplayname={
          item.location_displayname_short
            ? item.location_displayname_short
            : 'Ukjent sted'
        }
        camera={
          item.exif_camera
            ? item.exif_camera
            : 'Ukjent'
        }
        exif_duration_hhmmss={item.exif_duration_hhmmss}
        fps={Math.floor(item.exif_fps)}
        date={
          localeDateStringNorwegianBugFix(
            item.exif_last_modified, 'long',
          )
        }
        thumbnailsCount={
          item.static_thumbnail_count
            ? item.static_thumbnail_count
            : 0
        }
        resolution={
          item.exif_resolution
            ? item.exif_resolution
            : item.exif_dimensions
        }
        geotag_old_id={item.geotag_old}
      />
    )));

    // console.log(data);
    // preloadAllImages(data);
  };

  useEffect(() => {
    fetchItems();
  }, [currentPage, viewPerPage]);

  useEffect(() => {
    if (currentPage === 1) {
      fetchItems();
    } else {
      setCurrentPage(1);
    }
  }, [restApiParams]);

  return (
    <>
      <div className={`${styles.gridWrapper}`}>
        <Grid className={`${styles.thumbnailGrid}`} container spacing={2}>
          {
            items.length ? items : <em>Loading...</em>
            }
        </Grid>
      </div>

      <Pagination
        itemsCount={itemsCount}
        currentPage={currentPage}
        viewPerPage={viewPerPage}
        handlePageChange={handlePageChange}
        setViewPerPage={handleChangeViewPerPage}
      />

    </>
  );
}

VideoitemsBrowser.propTypes = {
  toggleModal: PropTypes.func,
};

VideoitemsBrowser.defaultProps = {
  toggleModal: null,
};
