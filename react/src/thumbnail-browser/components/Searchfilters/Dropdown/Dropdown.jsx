import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';
import { motion, AnimatePresence } from 'framer-motion';
import styled from 'styled-components';
import useOnClickOutside from '../../../../common/hooks/useOnClickOutside';
import { capitalizeFirstChar } from '../../../../common/utils/utils';
import { languages } from '../../../../common/constants/constants';

import styles from './Dropdown.module.css';

const ContentContainer = styled(motion.div)`
  position: absolute;
  max-width: 400px;
  min-width: 140px;
  height: min-content;
  width: min-content;
  padding: 0;
  margin: 0;
  overflow: hidden;
  background-color: var(--tertiary);
  border-radius: 4px;
  display: flex;
  justify-content: top;
  flex-direction: column;
  cursor: pointer;
  box-shadow: 0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22);
`;

const contentContainerVariants = {
  initial: { opacity: 0.6, height: 'auto' },
  toggle: { opacity: 1, height: 'auto', transition: { type: 'easeIn', duration: 0.1 } },
  exit: { opacity: 0.6, height: 'auto', transition: { type: 'easeOut', duration: 0.1 } },
};

const Header = ({
  filterType,
  toggle,
  onClick,
}) => {
  const label = `${capitalizeFirstChar(languages.NO.filterTypes[filterType])}`;

  return (
    <button
      type="button"
      id={`filter-dropdown-${filterType}`}
      className={toggle
        ? `${styles.dropdownHeader} ${styles.active}`
        : `${styles.dropdownHeader}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

const Dropdown = ({
  filterType,
  InnerComponent,
}) => {
  const [toggle, setToggle] = useState(false);
  const ref = useRef();

  useOnClickOutside(ref, (event) => {
    if (event.target.id.split('filter-dropdown-')?.[1] === filterType) return;
    setToggle(false);
  });

  const handleToggle = () => setToggle((prev) => !prev);

  return (
    <div className={`${styles.dropdownOuterWrapper}`}>
      <Header
        filterType={filterType}
        onClick={handleToggle}
        toggle={toggle}
      />
      <div>
        <AnimatePresence>
          { toggle
          && (
          <ContentContainer
            initial="initial"
            animate="toggle"
            exit="exit"
            variants={contentContainerVariants}
            ref={ref}
          >
            {InnerComponent}
          </ContentContainer>
          )}

        </AnimatePresence>
      </div>
    </div>
  );
};

export default Dropdown;

Header.propTypes = {
  filterType: PropTypes.string,
  toggle: PropTypes.bool,
  onClick: PropTypes.func,
};

Header.defaultProps = {
  filterType: '',
  toggle: false,
  onClick: null,
};

Dropdown.propTypes = {
  filterType: PropTypes.string,
  InnerComponent: PropTypes.node,
};

Dropdown.defaultProps = {
  filterType: '',
  InnerComponent: null,
};
