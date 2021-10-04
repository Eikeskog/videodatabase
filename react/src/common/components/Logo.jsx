import React from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';

const StyledLogo = styled(motion.div)`
  font-size: 1.2rem;
  padding: 20px;
  border-radius: 50px;
  border: none;
  background-color: #5c3aff;
  color: white;
`;
// #5c3aff

const Logo = () => (
  <StyledLogo
    whileHover={{ scale: 1.1 }}
    whileTap={{ scale: 0.9 }}
  >
    Videodatabase
  </StyledLogo>
);

export default Logo;
