import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Grid from '@material-ui/core/Grid';
import Overlay from './components/Overlay/Overlay';
import Footer from './components/Footer/Footer';
import Header from './components/Header/Header';
import { Image, Placeholder } from './components/Image/Image';
import { getThumbnailUrl } from '../../../common/utils/utils';

import styles from './Card.module.css';

const cardSizes = {
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

  const handleSliderChange = (event) => setThumbnailUrl(
    getThumbnailUrl(videoitemId, parseInt(event.target.value, 10)),
  );

  const openModal = (elementClicked) => toggleModal({
    openedFromComponent: 'thumbnailboxOuter',
    activeModalElement: elementClicked,
    innerElementId: videoitemId,
    optionalParams: null,
  });

  return (
    <Grid
      item
      key={videoitemId}
      xs={cardSizes.xs}
      sm={cardSizes.sm}
      md={cardSizes.md}
      lg={cardSizes.lg}
    >
      <div
        className={`${styles.card}`}
        onMouseLeave={() => setDisplaySlider(false)}
        onMouseEnter={() => setDisplaySlider(true)}
      >
        <Header
          date={date}
          locationDisplayname={locationDisplayname}
          openModal={openModal}
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
