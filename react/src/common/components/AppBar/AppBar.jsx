import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Emoticon from '../Emoticon';
import ThemeToggler from '../ThemeToggler';
import Searchfilters from '../../../thumbnail-browser/components/Searchfilters/Searchfilters';
import FilterChips from '../../../thumbnail-browser/components/Searchfilters/FilterChips/FilterChips';
import Searchbar from '../Searchbar';
import Logo from '../Logo';
import { useSearchfilters } from '../../../thumbnail-browser/contexts/SearchfiltersContext';
import { useUserContext } from '../../contexts/UserContext/UserContext';

import styles from './AppBar.module.css';

// demo / early development
const AppBar = (/* {mode} */) => {
  const { activeSearchfilters, removeSearchfilter } = useSearchfilters();
  const { useAuth: { user, logOut } } = useUserContext();

  return (
    <div className={`${styles.wrapper}`}>
      <div className={`${styles.topOuterWrapper}`}>
        <div className={`${styles.topInnerWrapper}`}>
          <Logo />
          {user?.username ? (
            <p>
              Hei,
              {' '}
              {user.username}
            </p>
          ) : <p>Logg inn</p> }
          <div className={`${styles.leftIcons}`}>
            <ThemeToggler />

            <FontAwesomeIcon
              icon="fa-solid fa-hashtag"
              style={{ fontSize: '1.75em', color: 'darkgray' }}
            />
            <FontAwesomeIcon icon="fa-regular fa-rectangle-list" style={{ fontSize: '1.75em', color: 'darkgray' }} />
            <FontAwesomeIcon icon="fa-solid fa-hard-drive" style={{ fontSize: '1.75em', color: 'darkgray' }} />

            <FontAwesomeIcon icon="fa-solid fa-map-marked-alt" style={{ fontSize: '1.75em', color: 'darkgray' }} />
          </div>
          <div className={`${styles.searchbarWrapper}`}>
            <div className={`${styles.searchbar}`}>
              <Searchbar />
              <div className={`${styles.rightIcons}`}>
                <Emoticon onClick={logOut} />
                <FontAwesomeIcon icon="fa-solid fa-user" />
                <FontAwesomeIcon icon="fa-solid fa-table-cells-large" />
                <FontAwesomeIcon icon="fa-solid fa-pencil" />
                <FontAwesomeIcon icon="fa-solid fa-user-gear" />
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
