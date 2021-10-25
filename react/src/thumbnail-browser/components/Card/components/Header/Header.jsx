import React from 'react';
import PropTypes from 'prop-types';

import styles from './Header.module.css';

const Left = ({ children }) => (
  <div className={`${styles.left}`}>
    <span>
      {children}
    </span>
  </div>
);

const Right = ({ children, onClick }) => (
  <div className={`${styles.right}`}>
    <span
      role="presentation"
      onClick={onClick}
    >
      {children}
    </span>
  </div>
);

const Header = ({
  locationDisplayname,
  date,
  openModal,
}) => (
  <div className={`${styles.header}`}>
    <Left>{date}</Left>
    <Right
      onClick={() => openModal('locationDisplayname')}
    >
      {locationDisplayname}
    </Right>
  </div>
);

export default Header;

Header.propTypes = {
  date: PropTypes.string,
  locationDisplayname: PropTypes.string,
  openModal: PropTypes.func,
};

Header.defaultProps = {
  date: null,
  locationDisplayname: null,
  openModal: null,
};

Left.propTypes = {
  children: PropTypes.node,
};

Left.defaultProps = {
  children: null,
};

Right.propTypes = {
  children: PropTypes.node,
  onClick: PropTypes.func,
};

Right.defaultProps = {
  children: null,
  onClick: null,
};
