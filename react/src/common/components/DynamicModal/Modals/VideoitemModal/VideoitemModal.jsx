import React from 'react';
import PropTypes from 'prop-types';
import HorizontalTabs from '../../../TabbedContent/HorizontalTabs/HorizontalTabs';
import Location from './Location/Location';
import File from './File/File';
import Tags from './Tags/Tags';

const VideoitemModal = ({
  locationDisplayname,
  mapCenter,
  videoitemId,
  nearbyItems,
  localPaths,
  tags,
}) => {
  const location = {
    header: 'Sted',
    component: (
      <Location
        locationDisplayname={locationDisplayname}
        mapCenter={mapCenter}
        videoitemId={videoitemId}
        nearbyItems={nearbyItems}
      />
    ),
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
    component: <p>test3</p>,
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
};

VideoitemModal.defaultProps = {
  locationDisplayname: null,
  mapCenter: null,
  videoitemId: null,
  nearbyItems: null,
  localPaths: null,
  tags: null,
};

export default VideoitemModal;

// return (
//   <HorizontalTabs tabsDict={horizontalTabs} />
// );
