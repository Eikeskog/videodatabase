import React from 'react';
import PropTypes from 'prop-types';

// simple json demo
const Tags = ({ tags }) => (
  tags.map((tag) => (
    <p key={tag.tag_id}>
      {tag.tag_label}
    </p>
  ))
);

export default Tags;

Tags.propTypes = {
  tags: PropTypes.arrayOf(
    PropTypes.shape({
      tag_id: PropTypes.number,
      tag_label: PropTypes.string,
    }),
  ),
};

Tags.defaultProps = {
  tags: [],
};
