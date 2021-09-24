import React from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import AccessTimeIcon from '@material-ui/icons/AccessTime';

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
      <AccessTimeIcon />
      <AccessTimeIcon />
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
