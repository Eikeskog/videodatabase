import React from 'react';
import { useVideoitemContext } from '../../context/context';

// simple demo
const NearbyItems = () => {
  const { useLocationState: { nearbyItems } } = useVideoitemContext();

  return (
    <div>
      {Object.values(nearbyItems['120']).map((res) => (
        <div key={res.gps_point_id}>
          <>
            {`${res.distance} meter unna:`}

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
};

export default NearbyItems;
