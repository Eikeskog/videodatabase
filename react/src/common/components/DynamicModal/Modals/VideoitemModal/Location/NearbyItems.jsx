import React from 'react';
import PropTypes from 'prop-types';

// simple json demo
const NearbyItems = ({ nearbyItems }) => (
  <div>
    {Object.values(nearbyItems['120']).map((res) => (
      <div key={res.gps_point_id}>
        <>
          {res.distance}
          {' '}
          meter unna:
          {res.videoitems.map((videoitem) => (
            <p key={videoitem}>
              {videoitem}
            </p>
          ))}
        </>
      </div>
    ))}
  </div>
);

NearbyItems.propTypes = {
  nearbyItems: PropTypes.objectOf(
    PropTypes.arrayOf(
      PropTypes.shape({
        gps_point_id: PropTypes.number,
        lat: PropTypes.number,
        lng: PropTypes.number,
        distance: PropTypes.oneOfType([
          PropTypes.string,
          PropTypes.number,
        ]),
        videoitems: PropTypes.arrayOf(
          PropTypes.string,
        ),
      }),
    ),
  ),
};

NearbyItems.defaultProps = {
  nearbyItems: {},
};

export default NearbyItems;
