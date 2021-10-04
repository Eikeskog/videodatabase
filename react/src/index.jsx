import React from 'react';
import ReactDOM from 'react-dom';
import { StylesProvider } from '@material-ui/styles';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import ThemeContext from './common/contexts/ThemeContext';
import './normalize.css';

import App from './App';
import UserContext from './common/contexts/UserContext/UserContext';

library.add(fas, fab, far);

ReactDOM.render(
  <React.StrictMode>
    <StylesProvider injectFirst>
      <UserContext>
        <ThemeContext>
          <App />
        </ThemeContext>
      </UserContext>
    </StylesProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);
