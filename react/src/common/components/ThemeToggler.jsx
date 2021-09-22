import React from 'react';
import { useThemeContext } from '../contexts/ThemeContext';

const ThemeToggler = () => {
  const { state, dispatch } = useThemeContext();
  // unnecessary with reducer here
  const handleTheme = () => {
    dispatch({ type: 'CHANGE_THEME', payload: state.theme === 'light' ? 'dark' : 'light' });
  };

  return (
    <div
      style={{
        cursor: 'pointer',
        display: 'flex',
        fontFamily: 'Times New Roman',
        fontSize: '26px',
      }}
      role="presentation"
      onClick={() => handleTheme()}
    >
      {state.theme === 'light' ? '🌝' : '🌚'}
    </div>
  );
};

export default ThemeToggler;
