import React from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';

import styles from './Slider.module.css';

const Slider = ({
  maxValue,
  onChange,
  display,
}) => (
  <div className={`${styles.outerWrapper}`}>
    <motion.div
      className={`${styles.innerWrapper}`}
      animate={{
        opacity: display
          ? 1
          : 0,
      }}
      initial={false}
      transition="easeIn"
    >
      <input
        className={`${styles.slider}`}
        type="range"
        min={1}
        max={maxValue}
        defaultValue={1}
        onChange={onChange}
        aria-label="thumbnail-slider"
      />

    </motion.div>
  </div>
);

Slider.propTypes = {
  maxValue: PropTypes.number,
  onChange: PropTypes.func,
  display: PropTypes.bool,
};

Slider.defaultProps = {
  maxValue: null,
  onChange: null,
  display: null,
};

export default Slider;
