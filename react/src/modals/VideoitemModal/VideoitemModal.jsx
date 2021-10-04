import React from 'react';
import PropTypes from 'prop-types';
import VideoitemContext from './context/context';
import HorizontalTabs from '../../common/components/TabbedContent/HorizontalTabs/HorizontalTabs';
import File from './components/File/File';
import Tags from './components/Tags/Tags';
import Location from './components/Location/Location';
import Lists from './components/Lists/Lists';

// early progress/simple demo
const VideoitemModal = ({
  locationDisplayname,
  mapCenter,
  videoitemId,
  nearbyItems,
  localPaths,
  userLists,
  tags,
}) => {
  const location = {
    header: 'Sted',
    component: <Location />,
  };

  const date = {
    header: 'Dato',
    component: <p>test1</p>,
  };

  const file = {
    header: 'Filinfo',
    component: <File json={localPaths} />,
  };

  const lists = {
    header: 'Lister',
    component: <Lists />,
  };

  const itemTags = {
    header: 'Tags',
    component: <Tags tags={tags} />,
  };

  const timeline = {
    header: 'Tidslinje',
    component: <p>test5</p>,
  };
  return (
    <VideoitemContext
      videoitemId={videoitemId}
      locationDisplayname={locationDisplayname}
      lat={mapCenter.lat}
      lng={mapCenter.lng}
      nearbyItems={nearbyItems}
      userLists={userLists}
    >
      <HorizontalTabs
        tabsDict={{
          location,
          date,
          file,
          lists,
          itemTags,
          timeline,
        }}
      />
    </VideoitemContext>
  );
};

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
