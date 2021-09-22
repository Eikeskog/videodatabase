import React, { useState } from 'react';
import PropTypes from 'prop-types';
import MapCanvas from '../../../../MapCanvas/MapCanvas';

const Map = ({
  videoitemId,
  mapCenter,
  showMarker,
  locationDisplayname,
}) => {
  // rough n messy sketch
  const [draggable, setDraggable] = useState(false);

  const [latLng, setLatLng] = useState({
    lat: parseFloat(mapCenter?.lat),
    lng: parseFloat(mapCenter?.lng),
  });

  const marker = showMarker && {
    [videoitemId]: {
      lat: latLng.lat,
      lng: latLng.lng,
      markerEvents: {
        onClick: () => null,
      },
      draggable,
    },
    // ...nearbyItemsMarkers
  };

  const handleMapMarkerChange = (_, lat, lng) => {
    setLatLng({ lat, lng });
  };

  return (
    <div>
      <div style={{
        height: '400px',
        width: '100%',
        borderRadius: '8px',
        overflow: 'hidden',
      }}
      >
        <MapCanvas
          onMarkerChange={handleMapMarkerChange}
          zoom={14}
          center={mapCenter}
          markers={marker}
          draggable
        />
      </div>

      <div style={{
        position: 'absolute', top: '0', background: 'black', fontSize: '18px', color: 'white',
      }}
      >
        {locationDisplayname}
      </div>

      <div style={{ position: 'absolute', bottom: '0', background: 'rgba(0,0,0,0.2)' }}>
        <button
          type="button"
          onClick={() => setDraggable((prevState) => !prevState)}
          style={{
            padding: '8px',
            margin: '6px',
            borderRadius: '12px',
          }}
        >
          { draggable ? 'Lagre ny posisjon' : 'Endre posisjon' }
        </button>

        <button
          type="button"
          style={{
            padding: '8px',
            margin: '6px',
            borderRadius: '12px',
          }}
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
        >
          Vis fra samme filmappe
        </button>

      </div>
    </div>
  );
};

Map.propTypes = {
  videoitemId: PropTypes.string,
  mapCenter: PropTypes.shape({
    lat: PropTypes.number,
    lng: PropTypes.number,
  }),
  showMarker: PropTypes.bool,
  locationDisplayname: PropTypes.string,
};

Map.defaultProps = {
  videoitemId: null,
  mapCenter: {},
  showMarker: false,
  locationDisplayname: '',
};

export default Map;
