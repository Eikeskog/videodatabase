import React from 'react';
import { useLocationContext } from '../context/locationContext';

// simple json demo
const NearbyItems = () => {
  const { nearbyItems } = useLocationContext();

  return (
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
};

export default NearbyItems;
