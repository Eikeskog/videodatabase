import React from 'react';
import Emoticon from '../Emoticon';
import ThemeToggler from '../ThemeToggler';
import Searchfilters from '../../../thumbnail-browser/components/Searchfilters/Searchfilters';
import FilterChips from '../../../thumbnail-browser/components/Searchfilters/FilterChips/FilterChips';
import Searchbar from '../Searchbar';
import Logo from '../Logo';
import { useSearchfilters } from '../../../thumbnail-browser/contexts/SearchfiltersContext';

import styles from './AppBar.module.css';

const AppBar = (/* {mode} */) => {
  const { activeSearchfilters, removeSearchfilter } = useSearchfilters();

  return (
    <div className={`${styles.wrapper}`}>
      <div className={`${styles.topOuterWrapper}`}>
        <div className={`${styles.topInnerWrapper}`}>
          <Logo />
          <div className={`${styles.hallo}`}>
            <ThemeToggler />
            <ThemeToggler />
            <ThemeToggler />
            <ThemeToggler />
          </div>
          <div className={`${styles.searchbarWrapper}`}>
            <div className={`${styles.searchbar}`}>
              <Searchbar />
              <div className={`${styles.hei}`}>
                <Emoticon />
              </div>
            </div>
          </div>
        </div>

      </div>

      <div className={`${styles.middleOuterWrapper}`}>
        <div className={`${styles.filterDropdownsWrapper}`}>
          <Searchfilters />
        </div>

      </div>

      <div>
        <FilterChips
          searchfilters={activeSearchfilters}
          removeSearchfilter={removeSearchfilter}
        />
      </div>

    </div>
  );
};

export default AppBar;
