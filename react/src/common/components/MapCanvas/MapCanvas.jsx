import React, { useState, useEffect } from 'react';
import GoogleMapReact from 'google-map-react';
import PropTypes from 'prop-types';
import GMAPS_TOKEN from '../../../dev_settings';
import Marker from './Marker';

const MapCanvas = ({
  center: initalMapCenter,
  zoom: initialMapZoom,
  markers,
  onMarkerChange,
}) => {
  const [mapState, setMapState] = useState({
    center: [initalMapCenter.lat, initalMapCenter.lng],
    zoom: initialMapZoom,
    draggable: true,
  });

  const [markerPositions, setMarkerPositions] = useState(null);
  const [markerEvents, setMarkerEvents] = useState(null);
  const [markerColors, setMarkerColors] = useState(null);
  const [markerSizes, setMarkerSizes] = useState(null);

  useEffect(() => {
    if (!markers) return;

    const positions = {};
    const events = {};
    const colors = {};
    const sizes = {};

    Object.keys(markers).forEach((markerId) => {
      const marker = markers[markerId];
      positions[markerId] = { lat: marker.lat, lng: marker.lng, draggable: marker?.draggable };
      events[markerId] = marker?.markerEvents;
      colors[markerId] = marker?.color;
      sizes[markerId] = marker?.size;
    });

    // });

    // const initialMarkers = markers;

    // const positionsState = {};
    // const eventsState = {};
    // const colorsState = {};
    // const sizesState = {};

    // Object.entries(initialMarkers).forEach((([markerId, markerProps]) => {
    //   positionsState[markerId] = {
    //     lat: markerProps?.lat,
    //     lng: markerProps?.lng,
    //     draggable: markerProps?.draggable,
    //   };
    //   eventsState[markerId] = markerProps?.markerEvents;
    //   colorsState[markerId] = markerProps?.color;
    //   sizesState[markerId] = markerProps?.size;
    // }));

    // console.log('testing', positionsState);
    // console.log('markers', markers);

    setMarkerPositions(positions);
    setMarkerEvents(events);
    setMarkerColors(colors);
    setMarkerSizes(sizes);
  }, [markers]);

  const onChange = ({ center, zoom }) => {
    setMapState((prevState) => ({
      ...prevState,
      center,
      zoom,
    }));
  };

  const onMarkerInteraction = (childKey, _/* childProps */, mouse) => {
    setMapState((prevState) => ({ ...prevState, draggable: false }));

    if (markerPositions?.[childKey]?.draggable) {
      setMarkerPositions((prevState) => (
        { ...prevState, [childKey]: { lat: mouse.lat, lng: mouse.lng, draggable: true } }
      ));
    }
  };

  const onMarkerMouseUp = (childKey, _, mouse) => {
    setMapState((prevState) => ({ ...prevState, draggable: true }));

    if (!markerPositions?.[childKey]?.draggable) return;

    setMarkerPositions((prevState) => (
      { ...prevState, [childKey]: { lat: mouse.lat, lng: mouse.lng, draggable: true } }
    ));

    if (onMarkerChange) onMarkerChange(childKey, mouse.lat, mouse.lng);
  };

  // const handleApiLoaded = (map, maps) => {
  //   map.controls[maps.ControlPosition.TOP_LEFT].push(<h1>LOL</h1>);
  // };
  // const controlButtonDiv = document.createElement('div');

  // const handleOnLoad = (map, maps) => {

  //   const triangleCoords = [
  //     { lat: 58.199, lng: 5.601 },
  //     { lat: 58.699, lng: 5.801 },
  //     { lat: 58.099, lng: 5.501 },
  //     { lat: 58.299, lng: 5.301 },
  //   ];

  //   const bermudaTriangle = new maps.Polygon({
  //     paths: triangleCoords,
  //     strokeColor: '#FF0000',
  //     strokeOpacity: 0.8,
  //     strokeWeight: 2,
  //     fillColor: '#FF0000',
  //     fillOpacity: 0.35,
  //     draggable: true,
  //     geodesic: true,
  //   });
  //   bermudaTriangle.setMap(map);
  // };

  return (
    <GoogleMapReact
      // onGoogleApiLoaded={({ map, maps }) => handleOnLoad(map, maps)}
      mapTypeId="terrain"
      draggable={mapState.draggable}
      gestureHandling="greedy"
      bootstrapURLKeys={{ key: GMAPS_TOKEN }}
      onChange={onChange}
      center={mapState.center}
      zoom={mapState.zoom}
      onChildMouseDown={onMarkerInteraction}
      onChildMouseUp={onMarkerMouseUp}
      onChildMouseMove={onMarkerInteraction}
      onZoomAnimationEnd={onChange}
      onZoomAnimationStart={onChange}
      yesIWantToUseGoogleMapApiInternals
    >
      { markerPositions && Object.keys(markerPositions).map((key) => (
        <Marker
          key={key}
          lat={markerPositions?.[key]?.lat}
          lng={markerPositions?.[key]?.lng}
          markerEvents={markerEvents?.[key]}
          draggable={markerPositions?.[key].draggable}
          color={markerColors?.[key]}
          size={markerSizes?.[key]}
        />
      )) }

    </GoogleMapReact>
  );
};

MapCanvas.propTypes = {
  center: PropTypes.shape({
    lat: PropTypes.number,
    lng: PropTypes.number,
  }),
  zoom: PropTypes.number,
  markers: PropTypes.objectOf(
    PropTypes.shape({
      lat: PropTypes.number,
      lng: PropTypes.number,
      color: PropTypes.string,
      size: PropTypes.number,
      draggable: PropTypes.bool,
      markerEvents: PropTypes.objectOf(
        PropTypes.func,
      ),
    }),
  ),
  onMarkerChange: PropTypes.func,
};

MapCanvas.defaultProps = {
  center: null,
  zoom: null,
  markers: null,
  onMarkerChange: null,
};

export default MapCanvas;
