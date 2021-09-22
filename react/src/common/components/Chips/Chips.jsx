import React from 'react';
import PropTypes from 'prop-types';
import { chips, chip } from './Chips.module.css';

export const Chip = ({
  id,
  className,
  style,
  onClick,
  children,
}) => (
  <button
    type="button"
    key={id}
    className={className ? `${chip} ${className}` : `${chip}`}
    style={style}
    onClick={onClick}
  >
    {children}
  </button>
);

export const Chips = ({
  className,
  style,
  children,
}) => (
  <div
    className={
      className ? `${chips} ${className}`
        : `${chips}`
      }
    style={style}
  >
    {children}
  </div>
);

Chips.propTypes = {
  className: PropTypes.string,
  style: PropTypes.string,
  children: PropTypes.node,
};

Chips.defaultProps = {
  className: null,
  style: null,
  children: null,
};

Chip.propTypes = {
  id: PropTypes.string,
  className: PropTypes.string,
  style: PropTypes.string,
  children: PropTypes.node,
  onClick: PropTypes.func,
};

Chip.defaultProps = {
  id: null,
  className: null,
  style: null,
  children: null,
  onClick: null,
};
