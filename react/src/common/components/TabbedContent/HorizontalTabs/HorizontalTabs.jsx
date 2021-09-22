import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import { headerLeftOffset, headerStyle } from './util';

import styles from './HorizontalTabs.module.css';

const AccentLine = styled(motion.hr)`
  height: 4px;
  position: absolute;
  top: 44px;
  border: 0;
  margin: 0;
  padding: 0;
  width: ${(props) => props.width};
  left: ${(props) => props.left};
`;

const ActiveComponent = ({ tabsDict, activeTab }) => (
  <div
    className={`${styles.content}`}
  >
    {tabsDict[activeTab]?.component}
  </div>
);

ActiveComponent.propTypes = {
  tabsDict: PropTypes.objectOf(
    PropTypes.shape({
      header: PropTypes.string,
      component: PropTypes.node,
    }),
  ),
  activeTab: PropTypes.string,
};

ActiveComponent.defaultProps = {
  tabsDict: {},
  activeTab: null,
};

const TabHeader = ({
  id,
  index,
  label,
  onClick,
  tabsCount,
  headerWidth,
}) => {
  const style = headerStyle({ tabsCount, index, headerWidth });

  return (
    <>
      <input
        aria-label={id}
        type="radio"
        style={style}
        onClick={onClick}
        readOnly
      />

      <span style={style}>
        {label}
      </span>

    </>
  );
};

TabHeader.propTypes = {
  id: PropTypes.string,
  index: PropTypes.number,
  label: PropTypes.string,
  onClick: PropTypes.func,
  tabsCount: PropTypes.number,
  headerWidth: PropTypes.string,
};

TabHeader.defaultProps = {
  id: '',
  index: 0,
  label: '',
  onClick: null,
  tabsCount: 0,
  headerWidth: null,
};

const HorizontalTabs = ({
  tabsDict,
  initialActiveTab,
}) => {
  const [activeTab, setActiveTab] = useState(initialActiveTab || Object.keys(tabsDict)[0]);
  const [linePosition, setLinePosition] = useState('0');

  const tabsCount = Object.keys(tabsDict).length;
  const headerWidth = `${(100 / tabsCount).toString()}%`;

  const onTabClick = (index, key) => {
    setLinePosition(() => headerLeftOffset({ tabsCount, index }));
    setActiveTab(key);
  };

  return (
    <div className={`${styles.container}`}>
      <div className={`${styles.tabs}`}>

        { Object.keys(tabsDict).map((key, index) => (
          <TabHeader
            key={key}
            id={key}
            index={index}
            label={tabsDict[key]?.header}
            onClick={() => onTabClick(index, key)}
            headerWidth={headerWidth}
            tabsCount={tabsCount}
          />
        ))}

        <AccentLine
          className={`${styles.line}`}
          left={linePosition}
          width={headerWidth}
          animate={{
            left: linePosition,
            transition: 'spring',
          }}
        />

      </div>

      <div className={`${styles.content}`}>
        {tabsDict[activeTab]?.component}
      </div>

    </div>
  );
};

HorizontalTabs.propTypes = {
  tabsDict: PropTypes.objectOf(
    PropTypes.shape({
      header: PropTypes.string,
      component: PropTypes.node,
    }),
  ),
  initialActiveTab: PropTypes.string,
};

HorizontalTabs.defaultProps = {
  tabsDict: {},
  initialActiveTab: null,
};

export default HorizontalTabs;
