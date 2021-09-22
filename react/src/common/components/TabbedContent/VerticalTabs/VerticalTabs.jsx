import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { fontAwesomeIconsTest } from '../../../constants/constants';
import tabPanelBorderRadiusFix from './util';

import styles from './VerticalTabs.module.css';

const VerticalTabs = ({ tabsDict, initialActiveTab }) => {
  const [activeTab, setActiveTab] = useState(initialActiveTab || Object.keys(tabsDict)[0]);
  const tabsCount = Object.keys(tabsDict).length;

  const onTabClick = (index, key) => {
    setActiveTab(key);
  };

  return (
    <div className={`${styles.container}`}>
      <div className={`${styles.tabs}`}>
        <div className={`${styles.wrapper}`}>
          { Object.keys(tabsDict).map((key, index) => (
            <React.Fragment key={key}>
              <input
                type="radio"
                aria-label={key}
                checked={activeTab === key}
                onClick={() => onTabClick(index, key)}
                readOnly
              />

              <span style={
                (index === tabsCount - 1)
                  ? tabPanelBorderRadiusFix
                  : null
                }
              >
                { tabsDict[key].header }
              </span>

              <i className={`fa ${fontAwesomeIconsTest[index]}`} />

            </React.Fragment>
          ))}

        </div>
      </div>

      <div className={`${styles.content}`}>
        {tabsDict[activeTab].component}
      </div>
    </div>

  );
};

VerticalTabs.propTypes = {
  tabsDict: PropTypes.objectOf(
    PropTypes.shape({
      header: PropTypes.string,
      component: PropTypes.node,
    }),
  ),
  initialActiveTab: PropTypes.string,
};

VerticalTabs.defaultProps = {
  tabsDict: {},
  initialActiveTab: null,
};

export default VerticalTabs;
