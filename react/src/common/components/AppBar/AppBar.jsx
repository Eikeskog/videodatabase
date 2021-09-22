import React from 'react';
import Emoticon from '../Emoticon';
import ThemeToggler from '../ThemeToggler';
import FilterDropdownsPanel from '../../../browser/components/SearchfilterDropdowns/FilterDropdownsPanel';
import SearchfilterChips from '../../../browser/components/SearchfilterChips';
import Searchbar from '../Searchbar';
import Logo from '../Logo';
import { useSearchfilters } from '../../../browser/contexts/SearchfiltersContext';

import styles from './AppBar.module.css';

const AppBar = (/* {mode} */) => {
  // super bad css
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
          <FilterDropdownsPanel />
        </div>

      </div>

      <div>
        <SearchfilterChips
          searchfilters={activeSearchfilters}
          removeSearchfilter={removeSearchfilter}
        />
      </div>

    </div>
  );
};

export default AppBar;
