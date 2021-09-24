import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchableCheckboxes from './Checkboxes/SearchableCheckboxes';
import Checkboxes from './Checkboxes/Checkboxes';
import DateRangePicker from '../../../common/components/DateRangePicker/DateRangePicker';
import Dropdown from './Dropdown/Dropdown';
import styles from './Searchfilters.module.css';

const getInnerComponent = ({ filterType, initalData }) => {
  const enableSearch = initalData[filterType]?.count > 10;

  if (filterType === 'dateRange') return <DateRangePicker />;

  if (enableSearch) {
    return (
      <SearchableCheckboxes
        filterType={filterType}
        initialValues={initalData[filterType]?.items}
      />
    );
  }
  return (
    <Checkboxes
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
        <Dropdown
          key={filterType}
          filterType={filterType}
          initialValues={initalData[filterType]?.items}
          enableSearch={initalData[filterType]?.count > 10}
          InnerComponent={InnerComponent}
        />
      );
    })
);

const Searchfilters = () => {
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

export default Searchfilters;
