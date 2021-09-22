import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import Modal from '../Modal/Modal';
import initModal from './initModal';

const DynamicModal = ({
  openedFromComponent,
  activeModalElement,
  innerElementId,
  optionalParams,
  closeModal,
}) => {
  const [innerComponent, setInnerComponent] = useState(null);

  useEffect(() => {
    const { apiUrl, handleResponse } = initModal(
      openedFromComponent,
      innerElementId,
      activeModalElement,
      optionalParams,
    );
    if (!apiUrl) return;

    const fetch = async () => {
      const res = await axios.get(apiUrl);
      setInnerComponent(() => handleResponse(res.data));
    };

    fetch();
  }, []);

  return (
    <Modal
      isOpen
      InnerComponent={innerComponent || <p>spinner :)</p>}
      closeModal={closeModal}
    />
  );
};

DynamicModal.propTypes = {
  openedFromComponent: PropTypes.string,
  activeModalElement: PropTypes.string,
  innerElementId: PropTypes.string,
  optionalParams: PropTypes.objectOf(
    PropTypes.string,
  ),
  closeModal: PropTypes.func,
};

DynamicModal.defaultProps = {
  openedFromComponent: null,
  activeModalElement: null,
  innerElementId: null,
  optionalParams: null,
  closeModal: null,
};

export default DynamicModal;
