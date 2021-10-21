import React from 'react';
import PropTypes from 'prop-types';
import { useSearchfilters } from '../../../contexts/SearchfiltersContext';
import { renderCheckboxList } from './utils';

const Checkboxes = ({
  filterType,
  initialValues,
}) => {
  const {
    activeSearchfilters,
    toggleActiveSearchfilter,
  } = useSearchfilters();

  return renderCheckboxList({
    filterType,
    initialValues,
    activeSearchfilters,
    toggleActiveSearchfilter,
  });
};

Checkboxes.propTypes = {
  filterType: PropTypes.string,
  initialValues: PropTypes.objectOf(PropTypes.string),
};

Checkboxes.defaultProps = {
  filterType: '',
  initialValues: {},
};

const MemoizedCheckboxes = React.memo(Checkboxes);

export default MemoizedCheckboxes;
