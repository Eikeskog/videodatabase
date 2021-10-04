import React from 'react';
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
  const onChange = ({ center, zoom }) => {
    onMapChange({ center, zoom, draggable: mapState.draggable });
  };

  const onMarkerInteraction = (childKey, _/* childProps */, mouse) => {
    if (!markersState?.[childKey]?.draggable) return;

    onMarkerChange({
      id: childKey,
      lat: mouse.lat,
      lng: mouse.lng,
    });
  };

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

  return (
    <GoogleMapReact
      options={{
        backgroundColor: 'black',
        mapTypeId: 'satellite',
        styles: dark,
      }}
      mapTypeId="terrain"
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

      { !!Object.keys(markersState).length && Object.keys(markersState).map((key) => (
        <Marker
          key={key}
          lat={markersState[key]?.lat}
          lng={markersState[key]?.lng}
          draggable={markersState[key]?.draggable}
          // events={markersState[key]?.events}
          // color={markersState[key]?.color}
          // size=markersState[key]?.size}
        />
      )) }

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

export default ControlledMapCanvas;
