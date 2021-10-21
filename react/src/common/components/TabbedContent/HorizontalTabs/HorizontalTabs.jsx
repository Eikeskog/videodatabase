import React, { useMemo, useState } from 'react';
import PropTypes from 'prop-types';
import { AnimatePresence, motion } from 'framer-motion';
import styled from 'styled-components';
import { headerLeftOffset, headerStyle } from './util';

import styles from './HorizontalTabs.module.css';

const AnimatedLine = styled(motion.div)`
  height: 4px;
  position: absolute;
  top: 30px;
  border: 0;
  margin: 0;
  padding: 0;
  width: ${(props) => props.width};
  left: ${(props) => props.left};
`;

const variants = {
  initial: { opacity: 0 },
  isOpen: { opacity: 1, transition: { type: 'spring', duration: 0.3 } },
  exit: { opacity: 0 },
};

const ActiveComponent = ({ style, children }) => (
  <AnimatePresence>
    <motion.div
      variants={variants}
      initial="initial"
      animate="isOpen"
      exit="exit"
      className={`${styles.content}`}
      transition="easeIn"
      style={style}
    >

      {children}

    </motion.div>
  </AnimatePresence>

);

ActiveComponent.propTypes = {
  children: PropTypes.node,
  style: PropTypes.objectOf(PropTypes.string),
};

ActiveComponent.defaultProps = {
  children: null,
  style: {},
};

const TabHeader = ({
  id,
  index,
  label,
  onClick,
  tabsCount,
  headerWidth,
}) => {
  const style = useMemo(() => headerStyle({ tabsCount, index, headerWidth }), []);

  return (
    <span
      style={style}
      role="presentation"
      onClick={onClick}
      aria-label={id}
    >
      {label}
    </span>
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
  const [activeTab, setActiveTab] = useState(() => initialActiveTab ?? Object.keys(tabsDict)[0]);
  const [linePosition, setLinePosition] = useState('0');

  const tabsCount = Object.keys(tabsDict).length;
  const headerWidth = useMemo(() => `${Math.floor((100 / tabsCount)).toString()}%`, []);

  const onTabClick = (index, key) => {
    setLinePosition(() => headerLeftOffset({ tabsCount, index }));
    setActiveTab(key);
  };

  const tabHeaders = useMemo(() => Object.keys(tabsDict).map(
    (key, index) => (
      <TabHeader
        key={key}
        id={key}
        index={index}
        label={tabsDict[key]?.header}
        onClick={() => onTabClick(index, key)}
        headerWidth={headerWidth}
        tabsCount={tabsCount}
      />
    ),
  ), []);

  return (
    <div className={`${styles.container}`}>
      <div className={`${styles.tabs}`}>

        {tabHeaders}

        <AnimatedLine
          className={`${styles.line}`}
          left={linePosition}
          width={headerWidth}
          animate={{
            left: linePosition,
            transition: 'spring',
          }}
        />

      </div>

      <ActiveComponent>
        {tabsDict[activeTab]?.component}
      </ActiveComponent>

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
