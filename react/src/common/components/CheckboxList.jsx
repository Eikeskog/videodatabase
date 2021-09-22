import React from 'react';
import PropTypes from 'prop-types';
import './CheckboxList.css';

const CheckboxList = ({ children }) => (
  <ul className="checkbox-list">
    {children}
  </ul>
);

CheckboxList.propTypes = {
  children: PropTypes.node,
};

CheckboxList.defaultProps = {
  children: null,
};

export default CheckboxList;
