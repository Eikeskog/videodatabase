import React, {
  createContext, useContext, useEffect, useState,
} from 'react';
import PropTypes from 'prop-types';
import prepareRestApiParams from '../utils/utils';

// localStorage.clear()

const initialValue = {
  activeSearchfilters:
  JSON.parse(localStorage.getItem('activeSearchfilters'))
  || {
    camera: {},
    dateRange: {},
    keyword: {},
    project: {},
    fps: {},
    disk: {},
    location: {},
  },
  restApiParams: JSON.parse(localStorage.getItem('activeSearchfiltersApiParams'))
  || {},
};

const Context = createContext({
  ...initialValue,
  addSearchfilter: () => {},
  removeSearchfilter: () => {},
  toggleActiveSearchfilter: () => {},
});

export const useSearchfilters = () => useContext(Context);

const SearchfiltersContext = ({ children }) => {
  const [active, setActive] = useState(initialValue.activeSearchfilters);
  const [restApiParams, setRestApiParams] = useState(initialValue.restApiParams);

  const addFilter = (filterType, id, name) => {
    if (!Object.keys(initialValue.activeSearchfilters).includes(filterType)) return;
    setActive((prevState) => (
      { ...prevState, [filterType]: { ...prevState[filterType], [id]: name } }
    ));
  };

  const removeFilter = (filterType, id) => {
    const newState = active[filterType];
    if (!newState) return;
    delete newState[id];
    setActive((prevState) => ({ ...prevState, [filterType]: newState }));
  };

  const toggleFilter = (filterType, id, name) => {
    if (active?.[filterType]?.[id]) {
      removeFilter(filterType, id);
    } else {
      addFilter(filterType, id, name);
    }
  };

  useEffect(() => {
    localStorage.setItem('activeSearchfilters', JSON.stringify(active));
    setRestApiParams(prepareRestApiParams(active));
  }, [active]);

  useEffect(() => {
    localStorage.setItem('activeSearchfiltersApiParams', JSON.stringify(restApiParams));
  }, [restApiParams]);

  return (
    <Context.Provider value={{
      activeSearchfilters: active,
      restApiParams,
      addSearchfilter: addFilter,
      removeSearchfilter: removeFilter,
      toggleActiveSearchfilter: toggleFilter,
    }}
    >
      {children}
    </Context.Provider>
  );
};

SearchfiltersContext.propTypes = {
  children: PropTypes.node,
};

SearchfiltersContext.defaultProps = {
  children: null,
};

export default SearchfiltersContext;
