import PropTypes from 'prop-types';
// import { useSearchfilters } from '../../../../browser/contexts/SearchfiltersContext';
import { useSearchfilters } from '../../../contexts/SearchfiltersContext';
import { renderCheckboxList } from './util';

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

export default Checkboxes;
