import React from 'react';
import PropTypes from 'prop-types';
import { Fade } from '@material-ui/core';
import VideoitemContext from './context/context';
import HorizontalTabs from '../../common/components/TabbedContent/HorizontalTabs/HorizontalTabs';
import File from './components/File/File';
import Tags from './components/Tags/Tags';
import Location from './components/Location/Location';

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
    component: <Fade in><Location /></Fade>,
  };

  const date = {
    header: 'Dato',
    component: <Fade in><p>test1</p></Fade>,
  };

  const file = {
    header: 'Filinfo',
    component: <Fade in><File json={localPaths} /></Fade>,
  };

  const lists = {
    header: 'Lister',
    component: <Fade in><p>test3</p></Fade>,
  };

  const itemTags = {
    header: 'Tags',
    component: <Fade in><Tags tags={tags} /></Fade>,
  };

  const timeline = {
    header: 'Tidslinje',
    component: <Fade in><p>test5</p></Fade>,
  };
  return (
    <VideoitemContext
      videoitemId={videoitemId}
      locationDisplayname={locationDisplayname}
      lat={mapCenter.lat}
      lng={mapCenter.lng}
      nearbyItems={nearbyItems}
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
  // return (
  //   <LocationContext
  //     videoitemId={videoitemId}
  //     locationDisplayname={locationDisplayname}
  //     lat={mapCenter.lat}
  //     lng={mapCenter.lng}
  //     nearbyItems={nearbyItems}
  //   >
  //     <HorizontalTabs
  //       tabsDict={{
  //         location,
  //         date,
  //         file,
  //         lists,
  //         itemTags,
  //         timeline,
  //       }}
  //     />
  //   </LocationContext>
  // );
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
