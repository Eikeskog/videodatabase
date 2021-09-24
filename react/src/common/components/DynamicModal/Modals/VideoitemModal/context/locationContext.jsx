import React, {
  createContext,
  useContext,
  useState,
  useMemo,
} from 'react';
import PropTypes from 'prop-types';
import { throttle } from 'lodash';

const Context = createContext({
  mapState: {},
  markersState: {},
  draggableMarker: false,
  locationDisplayname: () => {},
  setLocationDisplayname: () => {},
  onMapChange: () => {},
  onMarkerChange: () => {},
  toggleDraggableMarker: () => {},
});

export const useLocationContext = () => useContext(Context);

const LocationContext = ({
  videoitemId,
  lat: initalLat,
  lng: initalLng,
  nearbyItems,
  locationDisplayname: initalLocationDisplayName,
  children,
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

  const [locationDisplayname, setLocationDisplayname] = useState(initalLocationDisplayName);

  const handleConfirmedDatabaseUpdate = ({ params }) => {
    console.log('update', params);
  };

  const fetchNearbyItems = ({ id, lat, lng }) => {
    console.log('fetch', id, lat, lng);
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

  return (
    <Context.Provider value={{
      mapState,
      markersState,
      draggableMarker: markersState?.[videoitemId]?.draggable,
      nearbyItems,
      locationDisplayname,
      setLocationDisplayname,
      onMapChange,
      onMarkerChange,
      toggleDraggableMarker,
    }}
    >
      {children}
    </Context.Provider>
  );
};

LocationContext.propTypes = {
  videoitemId: PropTypes.string,
  locationDisplayname: PropTypes.string,
  lat: PropTypes.number,
  lng: PropTypes.number,
  nearbyItems: PropTypes.objectOf(
    PropTypes.arrayOf(
      PropTypes.shape({
        distance: PropTypes.oneOfType([
          PropTypes.string,
          PropTypes.number,
        ]),
        gps_point_id: PropTypes.number,
        lat: PropTypes.number,
        lng: PropTypes.number,
        videoitems: PropTypes.arrayOf(
          PropTypes.string,
        ),
      }),
    ),
  ),
  children: PropTypes.node,
};

LocationContext.defaultProps = {
  videoitemId: null,
  locationDisplayname: null,
  lat: null,
  lng: null,
  nearbyItems: null,
  children: null,
};

export default LocationContext;
