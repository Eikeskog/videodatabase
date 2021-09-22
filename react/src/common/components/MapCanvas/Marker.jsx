import React from 'react';
import { motion } from 'framer-motion';
import './Marker.css';
import PropTypes from 'prop-types';

const StaticMarker = ({ markerEvents }) => (
  <div
    role="presentation"
    onClick={markerEvents?.onClick}
  >
    <div className="marker-wrapper">
      <div className="marker-pin" />
      <div className="marker-pin-shade" />
    </div>
  </div>
);

const DraggableMarker = ({ markerEvents }) => (
  <motion.div
    onClick={markerEvents?.onClick}
    whileHover={{ scale: 1.6 }}
    whileTap={{ scale: 1.7 }}
    transition={{ type: 'spring', duration: 0.15 }}
  >
    <div className="marker-wrapper">
      <div className="marker-pin" />
      <div className="marker-pulse" />
    </div>
  </motion.div>
);

StaticMarker.propTypes = {
  markerEvents: PropTypes.shape({
    onClick: PropTypes.func,
  }),
};

StaticMarker.defaultProps = {
  markerEvents: null,
};

DraggableMarker.propTypes = {
  markerEvents: PropTypes.shape({
    onClick: PropTypes.func,
  }),
};

DraggableMarker.defaultProps = {
  markerEvents: null,
};

const Marker = ({
  markerEvents,
  draggable = false,
}) => (
  draggable === true
    ? <DraggableMarker markerEvents={markerEvents} />
    : <StaticMarker markerEvents={markerEvents} />
);

Marker.propTypes = {
  draggable: PropTypes.bool,
  markerEvents: PropTypes.shape({
    onClick: PropTypes.func,
  }),
};

Marker.defaultProps = {
  draggable: false,
  markerEvents: null,
};

export default Marker;
