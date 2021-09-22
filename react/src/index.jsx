import React from 'react';
import ReactDOM from 'react-dom';
import { StylesProvider } from '@material-ui/styles';
import ThemeContext from './common/contexts/ThemeContext';

import './normalize.css';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <StylesProvider injectFirst>
      <ThemeContext>
        <App />
      </ThemeContext>
    </StylesProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);
