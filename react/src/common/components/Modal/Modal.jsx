import React, { useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import PropTypes from 'prop-types';
import styles from './Modal.module.css';
import useOnClickOutside from '../../hooks/useOnClickOutside';

const Overlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 5000;
`;

const ModalContainer = styled(motion.div)`
  width: 50%;
  min-width: 400px;
  max-height: 600px;
  min-height: 500px;
  position: absolute;
  overflow: hidden;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 12px;
  z-index: 6000;
`;

const CloseButton = styled.svg`
  width: 20px;
  height: 20px;
  float: right;
  display: block;
  position: relative;
  margin-right: 12px;
  margin-top: 12px;
  cursor: pointer;
  z-index: 99999;
  &:hover {
    background: red;
  }
`;

const variants = {
  initial: { opacity: 0 },
  isOpen: { opacity: 1, transition: { duration: 0.1 } },
  exit: { opacity: 0 },
};

const Modal = ({
  closeModal,
  InnerComponent,
  isOpen,
}) => {
  const ref = useRef();

  useOnClickOutside(ref, () => {
    closeModal();
  });

  return (
    <AnimatePresence>
      {isOpen && (
        <Overlay
          initial="initial"
          animate="isOpen"
          exit="exit"
          variants={variants}
        >
          <ModalContainer ref={ref} className={`${styles.container}`}>
            <div style={{ width: '100%', zIndex: '9999' }}>
              <CloseButton
                onClick={closeModal}
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20.39 20.39"
              >
                <title>close</title>
                <line
                  x1="19.39"
                  y1="19.39"
                  x2="1"
                  y2="1"
                  fill="none"
                  stroke="#5c3aff"
                  strokeLinecap="round"
                  strokeMiterlimit="10"
                  strokeWidth="2"
                />
                <line
                  x1="1"
                  y1="19.39"
                  x2="19.39"
                  y2="1"
                  fill="none"
                  stroke="#5c3aff"
                  strokeLinecap="round"
                  strokeMiterlimit="10"
                  strokeWidth="2"
                />
              </CloseButton>
            </div>
            <div style={{ position: 'relative', padding: '20px' }}>
              {InnerComponent}
            </div>
          </ModalContainer>
        </Overlay>
      )}
    </AnimatePresence>
  );
};

export default Modal;

Modal.propTypes = {
  closeModal: PropTypes.func,
  InnerComponent: PropTypes.node,
  isOpen: PropTypes.bool,
};

Modal.defaultProps = {
  closeModal: null,
  InnerComponent: null,
  isOpen: false,
};
