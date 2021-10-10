import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { fontAwesomeIconsTest } from '../../../constants/constants';

import styles from './VerticalTabs.module.css';

const VerticalTabs = ({ tabsDict, initialActiveTab }) => {
  const [activeTab, setActiveTab] = useState(initialActiveTab || Object.keys(tabsDict)[0]);

  const onTabClick = (key) => {
    setActiveTab(key);
  };

  return (
    <div className={`${styles.grid}`}>
      <div className={`${styles.panel}`}>
        <div className={`${styles.panelInner}`}>
          { Object.keys(tabsDict).map((key, index) => (
            <React.Fragment key={key}>
              <div
                role="presentation"
                className={activeTab === key
                  ? `${styles.header} ${styles.active}`
                  : `${styles.header}`}
                onClick={() => onTabClick(key)}
              >

                <div className={`${styles.icon}`}>
                  <i
                    className={`fa ${fontAwesomeIconsTest[index]}`}
                  />
                </div>

                <div
                  role="presentation"
                  aria-label={key}
                  className={`${styles.label}`}
                >
                  {tabsDict[key].header}
                </div>

              </div>
            </React.Fragment>
          ))}
        </div>
      </div>
      <div className={`${styles.component}`}>
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
