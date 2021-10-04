import React, {
  createContext,
  useContext,
  // useState,
  // useMemo,
} from 'react';
// import { throttle } from 'lodash';
// import { useLocationContext } from './locationContext';

import { defaultProps, propTypes } from '../props/props';
import useLocationState from '../hooks/useLocationState';

const Context = createContext({
  location: {},
  mapState: {},
  markersState: {},
  draggableMarker: false,
  locationDisplayname: () => {},
  setLocationDisplayname: () => {},
  onMapChange: () => {},
  onMarkerChange: () => {},
  toggleDraggableMarker: () => {},
});

export const useVideoitemContext = () => useContext(Context);

const VideoitemContext = ({
  videoitemId,
  lat: initalLat,
  lng: initalLng,
  nearbyItems,
  locationDisplayname: initalLocationDisplayName,
  userLists: initialUserLists,
  children,
}) => {
  const locationState = useLocationState({
    videoitemId,
    lat: initalLat,
    lng: initalLng,
    nearbyItems,
    locationDisplayname: initalLocationDisplayName,
    userLists: initialUserLists,
  });

  return (
    <Context.Provider
      value={{
        useLocationState: locationState,
        userLists: initialUserLists,
        videoitemId,
      }}
    >
      {children}
    </Context.Provider>
  );
};

VideoitemContext.propTypes = propTypes;

VideoitemContext.defaultProps = defaultProps;

export default VideoitemContext;
