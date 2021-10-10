import React, {
  createContext,
  useContext,
} from 'react';

import { videoitemProps, videoitemDefaultProps } from '../props/props';
import useLocationState from '../hooks/useLocationState';

const Context = createContext({
  useLocationState: () => {},
  userLists: {},
  videoitemId: null,
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

VideoitemContext.propTypes = videoitemProps;

VideoitemContext.defaultProps = videoitemDefaultProps;

export default VideoitemContext;
