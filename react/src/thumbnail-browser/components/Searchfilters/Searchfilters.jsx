import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './Searchfilters.module.css';
import urls from '../../../dev_urls';
import { renderInitial } from './utils';

const Searchfilters = () => {
  const [dropdowns, setDropdowns] = useState();

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await axios.get(urls.SEARCHFILTERS);
      setDropdowns(() => data?.[0] && renderInitial(data[0]));
    };
    fetchInitial();
  }, []);

  return (
    <div className={`${styles.headers}`}>
      {dropdowns}
    </div>
  );
};

const MemoizedSearchfilters = React.memo(Searchfilters);

export default MemoizedSearchfilters;
