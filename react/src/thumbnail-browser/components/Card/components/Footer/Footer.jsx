import React from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import SingleChip from '../../../../../common/components/Chips/SingleChip';
import Slider from '../Slider/Slider';
import { secondsToHms } from '../../../../../common/utils/utils';
import styles from './Footer.module.css';

const Left = ({ display, children }) => (
  <motion.div
    className={`${styles.left}`}
    animate={{
      opacity: display
        ? 1
        : 0,
    }}
    initial={false}
  >
    <span>
      {children}
    </span>
  </motion.div>
);

const Right = ({ display, children }) => (
  <motion.div
    className={`${styles.right}`}
    animate={{
      opacity: display
        ? 1
        : 0,
    }}
    initial={false}
  >
    <span>
      {children}
    </span>
  </motion.div>
);

const Footer = ({
  duration,
  camera,
  resolution,
  fps,
  thumbnailsCount,
  onSliderChange,
  displaySlider,
  onMouseEnter,
  onMouseLeave,
}) => (
  <div
    className={`${styles.footer}`}
    onMouseEnter={onMouseEnter}
    onMouseLeave={onMouseLeave}
  >
    <Left display={!displaySlider}>
      <SingleChip>{`${fps} fps`}</SingleChip>
      <SingleChip>{`${secondsToHms(duration)}`}</SingleChip>
    </Left>

    <Right display={!displaySlider}>
      <SingleChip>{camera}</SingleChip>
      <SingleChip>{resolution}</SingleChip>
    </Right>

    {thumbnailsCount > 1 && (
      <Slider
        display={displaySlider}
        maxValue={thumbnailsCount}
        onChange={onSliderChange}
      />
    )}

  </div>
);

Footer.propTypes = {
  duration: PropTypes.number,
  camera: PropTypes.string,
  resolution: PropTypes.string,
  fps: PropTypes.number,
  thumbnailsCount: PropTypes.number,
  onSliderChange: PropTypes.func,
  displaySlider: PropTypes.bool,
  onMouseEnter: PropTypes.func,
  onMouseLeave: PropTypes.func,
};

Footer.defaultProps = {
  duration: null,
  camera: null,
  resolution: null,
  fps: null,
  thumbnailsCount: null,
  onSliderChange: null,
  displaySlider: null,
  onMouseEnter: null,
  onMouseLeave: null,
};

Left.propTypes = {
  children: PropTypes.node,
  display: PropTypes.bool,
};

Left.defaultProps = {
  children: null,
  display: null,
};

Right.propTypes = {
  children: PropTypes.node,
  display: PropTypes.bool,
};

Right.defaultProps = {
  children: null,
  display: null,
};

export default Footer;
