import React from 'react';
import PropTypes from 'prop-types';
import { DIRECTORIES } from '../../../../../common/constants/constants';
import styles from './Image.module.css';

export const Image = ({ url }) => (
  <img
    src={url}
    className={`${styles.image}`}
    alt="thumbnail"
  />
);

export const Placeholder = () => (
  <img
    src={`${DIRECTORIES.static_thumbnails}/placeholder.jpg`}
    className={`${styles.placeholder}`}
    alt="placeholder"
  />
);

Image.propTypes = {
  url: PropTypes.string,
};

Image.defaultProps = {
  url: null,
};
