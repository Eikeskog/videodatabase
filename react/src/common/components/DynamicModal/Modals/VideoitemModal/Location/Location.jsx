import React from 'react';
import PropTypes from 'prop-types';
import VerticalTabs from '../../../../TabbedContent/VerticalTabs/VerticalTabs';
import NearbyItems from './NearbyItems';
import Map from './Map';

const Location = ({
  mapCenter,
  videoitemId,
  locationDisplayname,
  nearbyItems,
}) => {
  // rough n messy sketch
  const map = {
    header: 'Kart',
    component: (
      <Map
        mapCenter={mapCenter}
        videoitemId={videoitemId}
        locationDisplayname={locationDisplayname}
        showMarker
      />
    ),
  };

  const info = {
    header: 'Om sted',
    component: <p>asdf</p>,
  };

  const nearby = {
    header: 'I nærheten',
    component: <NearbyItems nearbyItems={nearbyItems} />,
  };

  return <VerticalTabs tabsDict={{ map, info, nearby }} />;
};

Location.propTypes = {
  locationDisplayname: PropTypes.string,
  mapCenter: PropTypes.shape({
    lat: PropTypes.number,
    lng: PropTypes.number,
  }),
  videoitemId: PropTypes.string,
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

Location.defaultProps = {
  locationDisplayname: null,
  mapCenter: null,
  videoitemId: null,
  nearbyItems: null,
};

export default Location;
