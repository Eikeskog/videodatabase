import React from 'react';
import PropTypes from 'prop-types';

const SingleChip = ({ events, children }) => (
  <div
    role="presentation"
    onClick={events.onClick}
    className="single-chip"
  >
    {children}
  </div>
);

export default SingleChip;

SingleChip.propTypes = {
  children: PropTypes.node,
  events: PropTypes.shape({
    onClick: PropTypes.func,
  }),
};

SingleChip.defaultProps = {
  children: null,
  events: {},
};
