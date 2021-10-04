import React from 'react';
import PropTypes from 'prop-types';

const Emoticon = ({ onClick }) => (
  <div
    style={{
      cursor: 'pointer',
      display: 'flex',
      fontFamily: 'Times New Roman',
      fontSize: '24px',
    }}
    role="presentation"
    onClick={onClick}
  >
    ⚙
  </div>
);

Emoticon.propTypes = {
  onClick: PropTypes.func,
};

Emoticon.defaultProps = {
  onClick: null,
};

export default Emoticon;
