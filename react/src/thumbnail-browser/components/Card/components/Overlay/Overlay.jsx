import React from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import styles from './Overlay.module.css';

const Overlay = ({ display }) => (
  <motion.div
    className={`${styles.wrapper}`}
    animate={{
      opacity: display ? 1 : 0,
    }}
    initial={false}
    transition="easeIn"
  >
    <div className={`${styles.container}`}>
      <FontAwesomeIcon icon="fa-regular fa-heart" />
      <FontAwesomeIcon icon="fa-solid fa-circle-info" />
      {/* <FontAwesomeIcon icon="fa-solid fa-heart" /> */}
    </div>
  </motion.div>
);

Overlay.propTypes = {
  display: PropTypes.bool,
};

Overlay.defaultProps = {
  display: null,
};

export default Overlay;
