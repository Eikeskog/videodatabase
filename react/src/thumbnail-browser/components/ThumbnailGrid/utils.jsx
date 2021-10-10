import React from 'react';
import { localeDateStringNorwegianBugFix } from '../../../common/utils/utils';
import Card from '../Card/Card';

const renderCards = (data, toggleModal) => {
  if (!data) return <></>;
  return data.map((item) => (
    <Card
      key={item.videoitem_id}
      toggleModal={toggleModal}
      videoitemId={item.videoitem_id}
      duration={item.exif_duration_sec}
      locationDisplayname={
          item.location_displayname_short
            ? item.location_displayname_short
            : 'Ukjent sted'
        }
      camera={
          item.exif_camera
            ? item.exif_camera
            : 'Ukjent'
        }
      exif_duration_hhmmss={item.exif_duration_hhmmss}
      fps={Math.floor(item.exif_fps)}
      date={
          localeDateStringNorwegianBugFix(
            item.exif_last_modified, 'long',
          )
        }
      thumbnailsCount={
          item.static_thumbnail_count
            ? item.static_thumbnail_count
            : 0
        }
      resolution={
          item.exif_resolution
            ? item.exif_resolution
            : item.exif_dimensions
        }
      geotag_old_id={item.geotag_old}
    />
  ));
};
export default renderCards;
