import React from 'react';
import VideoitemModal from './VideoitemModal';

const initVideoitemModal = (
  data,
) => {
  const {
    gmaps_gps_point: gpsPoint,
    nearby_items: nearbyItems,
    location_displayname: locationDisplayname,
    videoitem_id: videoitemId,
    local_paths: localPaths,
    userlist_set: userLists,
    tags,
  } = data;

  if (!gpsPoint || !gpsPoint?.geotag_lvl_1) return <span>not implemented</span>;

  return (
    <VideoitemModal
      videoitemId={videoitemId}
      mapCenter={{
        lat: parseFloat(gpsPoint?.lat),
        lng: parseFloat(gpsPoint?.lng),
      }}
      locationDisplayname={locationDisplayname}
      nearbyItems={nearbyItems}
      localPaths={localPaths}
      userLists={userLists}
      tags={tags}
    />
  );
};

export default initVideoitemModal;
