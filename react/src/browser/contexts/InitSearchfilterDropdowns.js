import { createContext } from 'react';

const InitSearchfilterDropdowns = createContext({
  camera: {},
  project: {},
  keyword: {},
  fps: {},
  disk: {},
  place: {},
});

export default InitSearchfilterDropdowns;
