import React from 'react';
import AppBar from './common/components/AppBar/AppBar';
import LoginForm from './common/components/Auth/Login/Login';
import ThumbnailBrowser from './thumbnail-browser/ThumbnailBrowser';
import SearchfiltersContext from './thumbnail-browser/contexts/SearchfiltersContext';
import { useUserContext } from './common/contexts/UserContext/UserContext';
import useDynamicModal from './common/hooks/useDynamicModal/useDynamicModal';

import usePalette from './common/hooks/usePalette';
import styles from './App.module.css';

const App = () => {
  const palette = usePalette();
  const { modalContent, getModal } = useDynamicModal();
  const { useAuth: { isLoggedIn, logIn } } = useUserContext();

  if (!isLoggedIn) {
    return <LoginForm logIn={logIn} />;
  }

  return (
    <SearchfiltersContext>
      <div className={`${palette} ${styles.app}`}>
        <AppBar />

        { modalContent
          && modalContent }

        <ThumbnailBrowser toggleModal={getModal} />
      </div>
    </SearchfiltersContext>
  );
};

export default App;
