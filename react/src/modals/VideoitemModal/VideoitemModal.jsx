import React from 'react';
import PropTypes from 'prop-types';
import VideoitemContext from './context/context';
import HorizontalTabs from '../../common/components/TabbedContent/HorizontalTabs/HorizontalTabs';
import tabsDict from './tabsDict';

// early progress/simple demo
const VideoitemModal = ({
  locationDisplayname,
  mapCenter,
  videoitemId,
  nearbyItems,
  localPaths,
  userLists,
  tags,
}) => (
  <VideoitemContext
    videoitemId={videoitemId}
    locationDisplayname={locationDisplayname}
    lat={mapCenter.lat}
    lng={mapCenter.lng}
    nearbyItems={nearbyItems}
    userLists={userLists}
  >
    <HorizontalTabs
      tabsDict={tabsDict({ localPaths, tags })}
    />

  </VideoitemContext>
);

VideoitemModal.propTypes = {
  videoitemId: PropTypes.string,
  locationDisplayname: PropTypes.string,
  mapCenter: PropTypes.shape({
    lat: PropTypes.number,
    lng: PropTypes.number,
  }),
  nearbyItems: PropTypes.objectOf(
    PropTypes.arrayOf(
      PropTypes.shape({
        distance: PropTypes.oneOfType([
          PropTypes.string,
          PropTypes.number,
        ]),
        gps_point_id: PropTypes.number,
        lat: PropTypes.number,
        lng: PropTypes.number,
        videoitems: PropTypes.arrayOf(
          PropTypes.string,
        ),
      }),
    ),
  ),
  localPaths: PropTypes.arrayOf(
    PropTypes.shape({
      path: PropTypes.string,
      disk: PropTypes.shape({
        id: PropTypes.string,
        name: PropTypes.string,
      }),
      project: PropTypes.shape({
        id: PropTypes.string,
        name: PropTypes.string,
      }),
      directory: PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        path: PropTypes.string,
        rolltype: PropTypes.string,
        videoitems: PropTypes.arrayOf(
          PropTypes.shape({
            id: PropTypes.string,
            lat: PropTypes.number,
            lng: PropTypes.number,
            thumbnail_count: PropTypes.number,
          }),
        ),
      }),
    }),
  ),
  tags: PropTypes.arrayOf(
    PropTypes.shape({
      tag_id: PropTypes.number,
      tag_label: PropTypes.string,
    }),
  ),
  userLists: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      modified: PropTypes.string,
      user_id: PropTypes.string,
      label: PropTypes.string,
    }),
  ),
};

VideoitemModal.defaultProps = {
  locationDisplayname: null,
  mapCenter: null,
  videoitemId: null,
  nearbyItems: null,
  localPaths: null,
  tags: null,
  userLists: null,
};

export default VideoitemModal;
