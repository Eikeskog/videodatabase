import React from 'react';
import PropTypes from 'prop-types';
import { svgIconsBase64 } from '../constants/constants';

const SvgIcon = ({ icon }) => (
  <img
    alt={`svg-icon-${icon}`}
    className="unicode-icon"
    src={`data:image/png;base64,${svgIconsBase64[icon]}`}
  />
);

SvgIcon.propTypes = {
  icon: PropTypes.string,
};

SvgIcon.defaultProps = {
  icon: '',
};

export default SvgIcon;
