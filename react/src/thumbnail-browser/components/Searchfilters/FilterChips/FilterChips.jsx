import React from 'react';
import { Chips, Chip } from '../../../../common/components/Chips/Chips';
import UnicodeIcon from '../../../../common/components/UnicodeIcon';
import { useSearchfilters } from '../../../contexts/SearchfiltersContext';

const FilterChips = () => {
  const {
    activeSearchfilters,
    removeSearchfilter,
  } = useSearchfilters();

  const handleClick = (filterType, id) => removeSearchfilter(filterType, id);
  const chipLabel = (filterType, id) => activeSearchfilters[filterType][id];

  return (
    <Chips>
      { Object.keys(activeSearchfilters)
        .map((filterType) => Object.keys(activeSearchfilters[filterType])
          .map((filterId) => (
            <Chip
              key={`${filterType}-${filterId}`}
              onClick={() => handleClick(filterType, filterId)}
            >
              {`${chipLabel(filterType, filterId)}`}

              <UnicodeIcon
                symbol="x"
              />

            </Chip>
          )))}
    </Chips>
  );
};

export default FilterChips;
