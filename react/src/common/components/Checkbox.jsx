import React from 'react';
import PropTypes from 'prop-types';

const Checkbox = ({
  id,
  label,
  checked,
  onClick,
}) => (
  <li
    role="option"
    key={`cb-${id}`}
    onClick={onClick}
    onKeyPress={(e) => e.preventDefault()}
    aria-selected={checked === true}
  >
    <input
      type="checkbox"
      checked={checked === true}
      readOnly
    />
    <label htmlFor={label}>
      {label}
    </label>
  </li>
);

export default Checkbox;

Checkbox.propTypes = {
  id: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
  ]),
  label: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
  ]),
  checked: PropTypes.bool,
  onClick: PropTypes.func,
};

Checkbox.defaultProps = {
  id: 0,
  label: '',
  checked: false,
  onClick: null,
};
