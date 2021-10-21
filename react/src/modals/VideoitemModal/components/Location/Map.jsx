import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import ControlledMapCanvas from '../../../../common/components/MapCanvas/ControlledMapCanvas';
import { useVideoitemContext } from '../../context/context';

const MapContainer = styled(motion.div)`
  height: ${(props) => props.height};
  width: ${(props) => props.width};
  border-radius: 8px;
  overflow: hidden;
`;

// simple demo
const Map = () => {
  const [showNearbyItems, setShowNearbyItems] = useState(false);

  const {
    useLocationState: {
      locationDisplayname,
      setLocationDisplayname,
      onMapChange,
      onMarkerChange,
      mapState,
      markersState,
      toggleDraggableMarker,
      draggableMarker,
    },
  } = useVideoitemContext();

  return (
    <div>
      <MapContainer
        height="320px"
        width="70%"
        animate={{
          width: showNearbyItems
            ? '70%'
            : '100%',
        }}
        initial={false}
        transition="spring"
      >
        <ControlledMapCanvas
          mapState={mapState}
          markersState={markersState}
          onMarkerChange={onMarkerChange}
          onMapChange={onMapChange}
          draggable
        />
      </MapContainer>

      <div
        style={{
          position: 'absolute',
          top: '0',
          background: 'black',
          fontSize: '18px',
          color: 'white',
        }}
      >
        {locationDisplayname}
      </div>

      <div style={{ position: 'absolute', bottom: '0', background: 'rgba(0,0,0,0.2)' }}>
        <button
          type="button"
          onClick={toggleDraggableMarker}
          style={{
            padding: '8px',
            margin: '6px',
            borderRadius: '12px',
          }}
        >
          { draggableMarker ? 'Lagre ny posisjon' : 'Endre posisjon' }
        </button>

        <button
          type="button"
          style={{
            padding: '8px',
            margin: '6px',
            borderRadius: '12px',
          }}
          onClick={() => setShowNearbyItems((prev) => !prev)}
        >
          Vis i nærheten
        </button>

        <button
          type="button"
          style={{
            padding: '8px',
            margin: '6px',
            borderRadius: '12px',
          }}
          onClick={() => setLocationDisplayname('test')}
        >
          Vis fra samme filmappe
        </button>

      </div>
    </div>
  );
};

export default Map;
