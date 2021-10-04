import React, { useState } from 'react';
import * as locales from 'react-date-range/dist/locale';
import { DateRange } from 'react-date-range';
import SingleChip from '../Chips/SingleChip';
// import { useSearchfilters } from '../../../browser/contexts/SearchfiltersContext';
import { useSearchfilters } from '../../../thumbnail-browser/contexts/SearchfiltersContext';
import { dateRangeToString, dateRangeToSearchParameter } from '../../utils/utils';

import 'react-date-range/dist/styles.css';
import './DateRangePicker.css';

const DateRangePicker = () => {
  const [state, setState] = useState([
    {
      startDate: new Date(),
      endDate: new Date(),
      key: 'selection',
    },
  ]);
  const { addSearchfilter } = useSearchfilters();

  const chipLabel = dateRangeToString(state[0].startDate, state[0].endDate);
  const searchParameter = dateRangeToSearchParameter(state[0].startDate, state[0].endDate);

  return (
    <>
      <div>
        <DateRange
          showDateDisplay={false}
          onChange={(item) => setState([item.selection])}
          moveRangeOnFirstSelection={false}
          ranges={state}
          locale={locales.nb}
          rangeColors={['#404040', '#000000', '#000000']}
          maxDate={new Date()}
        />

        <div style={{
          textAlign: 'center',
        }}
        >
          { state[0].endDate !== null && (
          <>
            <SingleChip>
              {chipLabel}
            </SingleChip>

            <SingleChip
              customStyle={{
                cursor: 'pointer',
                fontSize: '1.5em',
                width: '1.5em',
                height: '1.5em',
                borderRadius: '50%',
                backgroundColor: 'teal',
              }}
              events={{
                onClick: () => addSearchfilter(
                  'dateRange',
                  searchParameter,
                  chipLabel,
                ),
              }}
            >
              +
            </SingleChip>
          </>
          )}

        </div>
      </div>
    </>
  );
};

export default DateRangePicker;
