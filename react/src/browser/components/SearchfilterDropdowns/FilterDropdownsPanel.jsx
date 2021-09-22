import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchableCheckboxList from './CheckboxLists/SearchableCheckboxList';
import StaticCheckboxList from './CheckboxLists/StaticCheckboxList';
import DateRangePicker from '../../../common/components/DateRangePicker/DateRangePicker';
import FilterDropdown from './FilterDropdown';
import styles from './FilterDropdowns.module.css';

const getInnerComponent = ({ filterType, initalData }) => {
  const enableSearch = initalData[filterType]?.count > 10;

  if (filterType === 'dateRange') return <DateRangePicker />;

  if (enableSearch) {
    return (
      <SearchableCheckboxList
        filterType={filterType}
        initialValues={initalData[filterType]?.items}
      />
    );
  }
  return (
    <StaticCheckboxList
      filterType={filterType}
      initialValues={initalData[filterType]?.items}
    />
  );
};

const renderInitial = (initalData) => (
  Object.keys(initalData)
    .map((filterType) => {
      const InnerComponent = getInnerComponent({ filterType, initalData });

      return (
        <FilterDropdown
          key={filterType}
          filterType={filterType}
          initialValues={initalData[filterType]?.items}
          enableSearch={initalData[filterType]?.count > 10}
          InnerComponent={InnerComponent}
        />
      );
    })
);

const FilterDropdownsPanel = () => {
  const [dropdowns, setDropdowns] = useState();

  useEffect(() => {
    const url = 'http://localhost:8000/api/init/searchfilter_dropdowns/';
    const fetchInitial = async () => {
      const { data } = await axios.get(url);
      setDropdowns(() => data?.[0] && renderInitial(data[0]));
    };
    fetchInitial();
  }, []);

  return (
    <div className={`${styles.headers}`}>
      <span>
        Filtrer søk:
      </span>
      {dropdowns}
    </div>
  );
};

export default FilterDropdownsPanel;
