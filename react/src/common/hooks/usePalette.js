import * as dark from '../palettes/dark.module.css';
import * as light from '../palettes/light.module.css';

import { useActiveTheme } from '../contexts/ThemeContext';

const usePalette = () => {
  const palettes = {
    dark,
    light,
  };
  const activeTheme = useActiveTheme();
  return palettes[activeTheme].colors;
};

export default usePalette;
