import React from 'react';
import SearchableCheckboxes from './Checkboxes/SearchableCheckboxes';
import Checkboxes from './Checkboxes/Checkboxes';
import DateRangePicker from '../../../common/components/DateRangePicker/DateRangePicker';
import Dropdown from './Dropdown/Dropdown';

export const getInnerComponent = ({ filterType, initalData }) => {
  if (filterType === 'dateRange') return <DateRangePicker />;

  if (initalData[filterType]?.count > 10) {
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

export const renderInitial = (initalData) => (
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
