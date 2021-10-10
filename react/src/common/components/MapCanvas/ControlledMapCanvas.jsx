import React, { useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import GoogleMapReact from 'google-map-react';
import Marker from './Marker';
import GMAPS_TOKEN from '../../../dev_settings';
import dark from './styles';

const ControlledMapCanvas = ({
  mapState,
  markersState,
  onMapChange,
  onMarkerChange,
}) => {
  const onChange = useCallback(({ center, zoom }) => {
    onMapChange({ center, zoom, draggable: mapState.draggable });
  }, [mapState, markersState]);

  const onMarkerInteraction = useCallback(
    (childKey, _/* childProps */, mouse) => {
      if (!markersState?.[childKey]?.draggable) return;

      onMarkerChange({
        id: childKey,
        lat: mouse.lat,
        lng: mouse.lng,
      });
    }, [markersState],
  );

  const onMarkerInteractionStart = (childKey, _, mouse) => {
    if (!markersState?.[childKey]?.draggable) return;

    onMapChange({
      center: mapState.center,
      zoom: mapState.zoom,
      draggable: false,
    });

    onMarkerChange({
      id: childKey,
      lat: mouse.lat,
      lng: mouse.lng,
    });
  };

  const onMarkerInteractionEnd = () => {
    onMapChange({
      center: mapState.center,
      zoom: mapState.zoom,
      draggable: true,
    });
  };

  const markers = useMemo(
    () => !!Object.keys(markersState).length
      && Object.keys(markersState).map((markerId) => (
        <Marker
          key={markerId}
          lat={markersState[markerId]?.lat}
          lng={markersState[markerId]?.lng}
          draggable={markersState[markerId]?.draggable}
        />
      )), [markersState],
  );

  return (
    <GoogleMapReact
      options={{
        backgroundColor: 'black',
        mapTypeId: 'satellite',
        styles: dark,
      }}
      draggable={mapState.draggable}
      bootstrapURLKeys={{ key: GMAPS_TOKEN }}
      onChange={onChange}
      center={mapState.center}
      zoom={mapState.zoom}
      onChildMouseDown={onMarkerInteractionStart}
      onChildMouseUp={onMarkerInteractionEnd}
      onChildMouseMove={onMarkerInteraction}
      onZoomAnimationEnd={onChange}
      onZoomAnimationStart={onChange}
      yesIWantToUseGoogleMapApiInternals
    >
      {markers}
    </GoogleMapReact>
  );
};

ControlledMapCanvas.propTypes = {
  mapState: PropTypes.shape({
    center: PropTypes.shape({
      lat: PropTypes.number,
      lng: PropTypes.number,
    }),
    zoom: PropTypes.number,
    draggable: PropTypes.bool,
  }),
  onMapChange: PropTypes.func,
  onMarkerChange: PropTypes.func,
  markersState: PropTypes.objectOf(
    PropTypes.shape({
      lat: PropTypes.number,
      lng: PropTypes.number,
      draggable: PropTypes.bool,
      // color: PropTypes.string,
      // size: PropTypes.number,
      // events: PropTypes.objectOf(
      //   PropTypes.func,
      // ),
    }),
  ),
};

ControlledMapCanvas.defaultProps = {
  mapState: null,
  onMapChange: null,
  onMarkerChange: null,
  markersState: null,
};

const MemoizedControlledMapCanvas = React.memo(ControlledMapCanvas);

export default MemoizedControlledMapCanvas;
