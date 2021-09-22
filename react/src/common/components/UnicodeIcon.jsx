import React from 'react';
import PropTypes from 'prop-types';
import { unicodeSymbols } from '../constants/constants';
import { unicodeIcon } from './UnicodeIcon.module.css';

const UnicodeIcon = ({ symbol, onClick }) => {
  const unicode = unicodeSymbols[symbol];
  const char = unicode || symbol;
  return (
    <span
      role="presentation"
      onClick={onClick}
      className={unicodeIcon}
    >
      {char}

    </span>
  );
};

UnicodeIcon.propTypes = {
  symbol: PropTypes.string,
  onClick: PropTypes.func,
};

UnicodeIcon.defaultProps = {
  symbol: '',
  onClick: () => null,
};

export default UnicodeIcon;
