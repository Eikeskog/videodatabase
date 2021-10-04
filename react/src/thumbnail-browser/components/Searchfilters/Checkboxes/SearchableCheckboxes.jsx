import React from 'react';
import PropTypes from 'prop-types';
import { useSearchfilters } from '../../../contexts/SearchfiltersContext';
import useTypingHints from '../../../../common/hooks/useTypingHints';
import { renderCheckboxList, renderTypingHints } from './util';

import styles from './SearchableCheckboxList.module.css';

const SearchableCheckboxes = ({
  filterType,
  initialValues,
}) => {
  const {
    activeSearchfilters,
    toggleActiveSearchfilter,
  } = useSearchfilters();

  const typingHints = useTypingHints();

  return (
    <>
      <input
        className={styles.textInput}
        type="text"
        ref={typingHints.ref}
        onChange={() => typingHints.onChange(filterType)}
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

SearchableCheckboxes.propTypes = {
  filterType: PropTypes.string,
  initialValues: PropTypes.objectOf(PropTypes.string),
};

SearchableCheckboxes.defaultProps = {
  filterType: '',
  initialValues: {},
};

export default SearchableCheckboxes;
