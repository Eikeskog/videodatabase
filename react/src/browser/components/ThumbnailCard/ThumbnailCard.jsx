import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Grid from '@material-ui/core/Grid';
import CalendarTodayIcon from '@material-ui/icons/CalendarToday';
import PlaceIcon from '@material-ui/icons/Place';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import SingleChip from '../../../common/components/Chips/SingleChip';
import { directories } from '../../../common/constants/constants';
import { secondsToHms, getThumbnailUrl } from '../../../common/utils/utils';
import { useActiveTheme } from '../../../common/contexts/ThemeContext';

import styles from './ThumbnailCard.module.css';

// needs cleanup
const PlaceholderImage = () => {
  const theme = useActiveTheme();
  return (
    <img
      src={`${directories.static_thumbnails}placeholder.jpg`}
      className={`${styles.thumbnailImg}`}
      alt="thumbnail-img"
      style={{ filter: theme === 'dark' && 'invert(100%)' }}
    />
  );
};

export const ThumbnailOverlay = () => (
  <div className={`${styles.overlayWrapper}`}>
    <div className={`${styles.overlayContainer}`}>
      <AccessTimeIcon />
    </div>
  </div>
);

const ThumbnailCard = ({
  locationDisplayname,
  videoitemId,
  fps,
  date,
  camera,
  resolution,
  thumbnailsCount,
  duration,
  toggleModal,
}) => {
  const durationFormatted = secondsToHms(duration);
  const firstThumbnailUrl = thumbnailsCount > 0 && `${directories.static_thumbnails}${videoitemId}/01.jpg`;

  const [thumbnailIndex, setThumbnailIndex] = useState(1);
  const [thumbnailUrl, setThumbnailUrl] = useState(firstThumbnailUrl);

  const thumbnailSize = {
    xs: 12,
    sm: 6,
    md: 4,
    lg: 4,
  };

  const handleModal = (elementClicked) => { // gjøre om til modal context ?
    const modalParams = {
      openedFromComponent: 'thumbnailboxOuter',
      activeModalElement: elementClicked,
      innerElementId: videoitemId,
      optionalParams: null,
    };
    toggleModal(modalParams);
  };

  const handleSliderChange = (event) => {
    const { value } = event.target;
    setThumbnailUrl(() => getThumbnailUrl(videoitemId, parseInt(value, 10)));
  };

  return (
    <Grid
      item
      key={videoitemId}
      xs={thumbnailSize.xs}
      sm={thumbnailSize.sm}
      md={thumbnailSize.md}
      lg={thumbnailSize.lg}
    >
      <div className={`${styles.thumbBox}`}>

        <div key="header" className={`${styles.header}`}>
          <div className={`${styles.left}`}>
            <span>
              <CalendarTodayIcon />
              {date}
            </span>
          </div>

          <div
            className={`${styles.right}`}
          >
            <span
              role="presentation"
              onClick={() => handleModal('locationDisplayname')}
            >
              <PlaceIcon />
              {locationDisplayname}
            </span>
          </div>

        </div>

        <div key="thumbnail" className={`${styles.thumbnail}`}>

          <ThumbnailOverlay
            thumbnailIndex={thumbnailIndex}
            setThumbnailIndex={setThumbnailIndex}
            thumbnail_count={thumbnailsCount}
          />

          { thumbnailsCount > 0 ? (
            <img
              src={thumbnailUrl}
              className={`${styles.thumbnailImg}`}
              alt="thumbnail-img"
            />
          ) : (
            <PlaceholderImage />
          )}

        </div>

        <div key="footer" className={`${styles.footer}`}>

          <div className={`${styles.left}`}>
            <span>
              <SingleChip>
                {fps}
                {' '}
                fps
              </SingleChip>
              <SingleChip>{durationFormatted}</SingleChip>
            </span>
          </div>

          <div className={`${styles.right}`}>
            <span>
              <SingleChip>{camera}</SingleChip>
              <SingleChip>{resolution}</SingleChip>
            </span>
          </div>

          {thumbnailsCount > 1 && (
            <div className={`${styles.sliderWrapper}`}>
              <div className={`${styles.sliderContent}`}>

                <input
                  className={`${styles.slider}`}
                  name="thumb-index"
                  type="range"
                  min={1}
                  max={thumbnailsCount}
                  defaultValue={1}
                  onChange={handleSliderChange}
                  aria-label="thumnail-slider"
                />

              </div>
            </div>
          )}

        </div>
      </div>
    </Grid>
  );
};

ThumbnailCard.propTypes = {
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

ThumbnailCard.defaultProps = {
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

export default ThumbnailCard;
