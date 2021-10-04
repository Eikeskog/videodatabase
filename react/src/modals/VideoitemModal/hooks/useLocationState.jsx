import { useState, useMemo } from 'react';
import { throttle } from 'lodash';

// early progress/simple demo
const useLocationState = ({
  videoitemId,
  lat: initalLat,
  lng: initalLng,
  nearbyItems: initialNearbyItems,
  locationDisplayname: initalLocationDisplayName,
  // onConfirmedDatabaseUpdate,
}) => {
  const [mapState, setMapState] = useState({
    center: {
      lat: initalLat,
      lng: initalLng,
    },
    zoom: 14,
    draggable: true,
  });

  const [markersState, setMarkersState] = useState({
    [videoitemId]: {
      lat: initalLat,
      lng: initalLng,
      draggable: false,
    },
  });

  const [nearbyItems, setNearbyItems] = useState(initialNearbyItems);
  const [locationDisplayname, setLocationDisplayname] = useState(initalLocationDisplayName);

  const handleConfirmedDatabaseUpdate = ({ params }) => {
    console.log('update', params);
  };

  const fetchNearbyItems = ({ id, lat, lng }) => {
    console.log('fetch', id, lat, lng);
    setNearbyItems();
  };

  const throttledFetchNearbyItems = useMemo(
    () => throttle(fetchNearbyItems, 1000),
    [],
  );

  const onMarkerChange = ({ id, lat, lng }) => {
    setMarkersState((prevState) => ({
      ...prevState,
      [id]: {
        lat,
        lng,
        draggable: true,
      },
    }));

    throttledFetchNearbyItems({ id, lat, lng });
  };

  const onMapChange = ({ center, zoom, draggable }) => {
    setMapState({
      center,
      zoom,
      draggable,
    });
  };

  const toggleDraggableMarker = () => {
    setMarkersState((prevState) => ({
      ...prevState,
      [videoitemId]: {
        ...prevState[videoitemId],
        draggable: !prevState[videoitemId].draggable,
      },
    }));
    console.log('test:', handleConfirmedDatabaseUpdate({ lat: 1, lng: 2 }));
  };

  return {
    mapState,
    markersState,
    draggableMarker: markersState?.[videoitemId]?.draggable,
    nearbyItems,
    locationDisplayname,
    setLocationDisplayname,
    onMapChange,
    onMarkerChange,
    toggleDraggableMarker,
  };
};

export default useLocationState;
