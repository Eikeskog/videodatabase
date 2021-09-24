import React, { useState } from 'react';
import axios from 'axios';
import AppBar from './common/components/AppBar/AppBar';
import DynamicModal from './common/components/DynamicModal/DynamicModal';
import ThumbnailBrowser from './thumbnail-browser/ThumbnailBrowser';
import SearchfiltersContext from './thumbnail-browser/contexts/SearchfiltersContext';
import usePalette from './common/hooks/usePalette';

import styles from './App.module.css';

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

const App = () => {
  const palette = usePalette();
  const [modal, setModal] = useState(null);

  const toggleModal = ({
    openedFromComponent,
    activeModalElement,
    innerElementId,
    optionalParams,
  }) => {
    setModal(
      <DynamicModal
        closeModal={() => setModal(null)}
        openedFromComponent={openedFromComponent}
        activeModalElement={activeModalElement}
        innerElementId={innerElementId}
        optionalParams={optionalParams}
      />,
    );
  };

  return (
    <SearchfiltersContext>
      <div className={`${palette} ${styles.app}`}>
        <AppBar />
        { modal && modal }
        <ThumbnailBrowser toggleModal={toggleModal} />
      </div>
    </SearchfiltersContext>
  );
};

export default App;
