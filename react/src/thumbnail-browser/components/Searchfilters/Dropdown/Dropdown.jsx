import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';
import { motion, AnimatePresence } from 'framer-motion';
import styled from 'styled-components';
import Header from './Header/Header';
import useOnClickOutside from '../../../../common/hooks/useOnClickOutside';

import styles from './Dropdown.module.css';

const Container = styled(motion.div)`
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

const containerVariants = {
  initial: { opacity: 0.6, height: 'auto' },
  toggle: { opacity: 1, height: 'auto', transition: { type: 'easeIn', duration: 0.1 } },
  exit: { opacity: 0.6, height: 'auto', transition: { type: 'easeOut', duration: 0.1 } },
};

const Dropdown = ({
  filterType,
  InnerComponent,
}) => {
  const [expanded, setExpanded] = useState(false);
  const ref = useRef();

  useOnClickOutside(ref, (event) => {
    if (event.target.id.split('filter-dropdown-')?.[1] === filterType) return;
    setExpanded(false);
  });

  const toggle = () => setExpanded((prev) => !prev);

  return (
    <div className={`${styles.wrapper}`}>
      <Header
        filterType={filterType}
        onClick={toggle}
        expanded={expanded}
      />
      <div>
        <AnimatePresence>
          { expanded
          && (
          <Container
            initial="initial"
            animate="toggle"
            exit="exit"
            variants={containerVariants}
            ref={ref}
          >
            {InnerComponent}
          </Container>
          )}

        </AnimatePresence>
      </div>
    </div>
  );
};

const MemoizedDropdown = React.memo(Dropdown);

export default MemoizedDropdown;

Dropdown.propTypes = {
  filterType: PropTypes.string,
  InnerComponent: PropTypes.node,
};

Dropdown.defaultProps = {
  filterType: '',
  InnerComponent: null,
};
