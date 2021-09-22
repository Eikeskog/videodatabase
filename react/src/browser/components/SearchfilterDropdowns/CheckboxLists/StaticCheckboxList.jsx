import PropTypes from 'prop-types';
import { useSearchfilters } from '../../../contexts/SearchfiltersContext';
import { renderCheckboxList } from './util';

const StaticCheckboxList = ({
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

StaticCheckboxList.propTypes = {
  filterType: PropTypes.string,
  initialValues: PropTypes.objectOf(PropTypes.string),
};

StaticCheckboxList.defaultProps = {
  filterType: '',
  initialValues: {},
};

export default StaticCheckboxList;
