import React from 'react';
import PropTypes from 'prop-types';
import { capitalizeFirstChar } from '../../../../../common/utils/utils';
import { TRANSLATIONS } from '../../../../../common/constants/constants';
import styles from './Header.module.css';

const Header = React.memo(({
  filterType,
  expanded,
  onClick,
}) => {
  const label = `${capitalizeFirstChar(TRANSLATIONS.NO.filterTypes[filterType])}`;

  return (
    <button
      type="button"
      id={`filter-dropdown-${filterType}`}
      className={expanded
        ? `${styles.header} ${styles.active}`
        : `${styles.header}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
});

Header.propTypes = {
  filterType: PropTypes.string,
  expanded: PropTypes.bool,
  onClick: PropTypes.func,
};

Header.defaultProps = {
  filterType: '',
  expanded: false,
  onClick: null,
};

export default Header;
