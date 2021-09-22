import React, {
  createContext, useContext, useReducer, useEffect,
} from 'react';
import PropTypes from 'prop-types';
import ThemeReducer from './ThemeReducer';

const initialValue = {
  theme: localStorage.getItem('theme') || 'light',
  name: localStorage.getItem('name') || '',
};

const Context = createContext({
  state: initialValue,
  dispatch: () => undefined,
});

export const useThemeContext = () => useContext(Context);

export const useActiveTheme = () => useThemeContext().state.theme;

const ThemeContext = ({ children }) => {
  const [state, dispatch] = useReducer(ThemeReducer, initialValue);

  useEffect(() => {
    localStorage.setItem('theme', state.theme);
  }, [state.theme]);

  return (
    <Context.Provider value={{ state, dispatch }}>
      {children}
    </Context.Provider>
  );
};

ThemeContext.propTypes = {
  children: PropTypes.node,
};

ThemeContext.defaultProps = {
  children: null,
};

export default ThemeContext;
