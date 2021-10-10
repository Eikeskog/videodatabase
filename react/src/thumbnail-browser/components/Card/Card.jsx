import React, { useState, useCallback } from 'react';
import PropTypes from 'prop-types';
import Grid from '@material-ui/core/Grid';
import Overlay from './components/Overlay/Overlay';
import Footer from './components/Footer/Footer';
import Header from './components/Header/Header';
import { Image, Placeholder } from './components/Image/Image';
import { getThumbnailUrl } from '../../../common/utils/utils';

import styles from './Card.module.css';

const defaultCardSizes = {
  xs: 12,
  sm: 6,
  md: 4,
  lg: 4,
};

const Card = ({
  videoitemId,
  locationDisplayname,
  fps,
  date,
  camera,
  resolution,
  thumbnailsCount,
  duration,
  toggleModal,
}) => {
  const [thumbnailUrl, setThumbnailUrl] = useState(
    thumbnailsCount > 0
      ? getThumbnailUrl(videoitemId, 1)
      : null,
  );

  const [displayOverlay, setDisplayOverlay] = useState(false);
  const [displaySlider, setDisplaySlider] = useState(false);

  const handleSliderChange = useCallback((event) => setThumbnailUrl(
    getThumbnailUrl(videoitemId, parseInt(event.target.value, 10)),
  ), []);

  return (
    <Grid
      item
      key={videoitemId}
      xs={defaultCardSizes.xs}
      sm={defaultCardSizes.sm}
      md={defaultCardSizes.md}
      lg={defaultCardSizes.lg}
    >
      <div
        className={`${styles.card}`}
        onMouseLeave={() => setDisplaySlider(false)}
        onMouseEnter={() => setDisplaySlider(true)}
      >
        <Header
          date={date}
          locationDisplayname={locationDisplayname}
          openModal={(elementClicked) => toggleModal({
            openedFromComponent: 'thumbnailboxOuter',
            activeModalElement: elementClicked,
            innerElementId: videoitemId,
            optionalParams: null,
          })}
        />

        <div
          className={`${styles.thumbnail}`}
          onMouseEnter={() => setDisplayOverlay(true)}
          onMouseLeave={() => setDisplayOverlay(false)}
        >

          <Overlay display={displayOverlay} />

          {thumbnailsCount > 0
            ? <Image url={thumbnailUrl} />
            : <Placeholder />}

        </div>

        <Footer
          fps={fps}
          camera={camera}
          resolution={resolution}
          duration={duration}
          thumbnailsCount={thumbnailsCount}
          onSliderChange={handleSliderChange}
          displaySlider={displaySlider}
          onMouseEnter={() => setDisplaySlider(true)}
          onMouseLeave={() => setDisplaySlider(false)}
        />

      </div>
    </Grid>
  );
};

Card.propTypes = {
  locationDisplayname: PropTypes.string,
  videoitemId: PropTypes.string,
  fps: PropTypes.number,
  date: PropTypes.string,
  camera: PropTypes.string,
  resolution: PropTypes.string,
  thumbnailsCount: PropTypes.number,
  duration: PropTypes.number,
  toggleModal: PropTypes.func,
};

Card.defaultProps = {
  locationDisplayname: null,
  videoitemId: null,
  fps: null,
  date: null,
  camera: null,
  resolution: null,
  thumbnailsCount: null,
  duration: null,
  toggleModal: null,
};

export default Card;
