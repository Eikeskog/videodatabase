import React from 'react';
import PropTypes from 'prop-types';
import { useSearchfilters } from '../../../contexts/SearchfiltersContext';
import useTypingHints from '../../../../common/hooks/useTypingHints';
import { renderCheckboxList, renderTypingHints } from './util';

import styles from './SearchableCheckboxList.module.css';

const SearchableCheckboxList = ({
  filterType,
  initialValues,
}) => {
  const {
    activeSearchfilters,
    toggleActiveSearchfilter,
  } = useSearchfilters();

  const typingHints = useTypingHints(filterType);

  return (
    <>
      <input
        className={styles.textInput}
        type="text"
        ref={typingHints.ref}
        onChange={typingHints.onChange}
        placeholder="Søk i database"
      />

      {typingHints.isTyping
        ? renderTypingHints({
          typingHints,
          filterType,
          activeSearchfilters,
          toggleActiveSearchfilter,
        })
        : renderCheckboxList({
          filterType,
          initialValues,
          activeSearchfilters,
          toggleActiveSearchfilter,
        })}

    </>
  );
};

SearchableCheckboxList.propTypes = {
  filterType: PropTypes.string,
  initialValues: PropTypes.objectOf(PropTypes.string),
};

SearchableCheckboxList.defaultProps = {
  filterType: '',
  initialValues: {},
};

export default SearchableCheckboxList;
