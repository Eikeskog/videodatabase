import React from 'react';
import PropTypes from 'prop-types';
import styles from './SingleChip.module.css';

const SingleChip = ({
  children,
  customStyle,
  events,
}) => (
  <button
    type="button"
    style={customStyle}
    className={`${styles.singleChip}`}
    onClick={events.onClick}
  >
    {children}
  </button>
);

export default SingleChip;

SingleChip.propTypes = {
  children: PropTypes.node,
  customStyle: PropTypes.objectOf(
    PropTypes.string,
  ),
  events: PropTypes.shape({
    onClick: PropTypes.func,
  }),
};

SingleChip.defaultProps = {
  children: null,
  customStyle: {},
  events: {
    onClick: null,
  },
};
