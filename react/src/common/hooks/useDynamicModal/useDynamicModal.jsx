import React, { useRef, useState } from 'react';
import Modal from '../../components/Modal/Modal';
import initModal from './initModal';
import { useUserContext } from '../../contexts/UserContext/UserContext';

const useDynamicModal = () => {
  const { useAuthorizedFetch } = useUserContext();
  const { authorizedFetch } = useAuthorizedFetch;

  const innerComponent = useRef();
  const [display, setDisplay] = useState(false);

  const setInnerComponent = (Component) => {
    innerComponent.current = Component;
    setDisplay(() => true);
  };

  const getInnerComponent = ({
    openedFromComponent,
    activeModalElement,
    innerElementId,
    optionalParams,
  }) => {
    const { apiUrl, handleResponse } = initModal({
      openedFromComponent,
      activeModalElement,
      innerElementId,
      optionalParams,
    });

    if (!apiUrl) return;

    authorizedFetch({
      method: 'get',
      url: apiUrl,
      handleResponse: (data) => { setInnerComponent(handleResponse(data)); },
      handleError: () => { setInnerComponent(<p>error..</p>); },
    });
  };

  const closeModal = () => setDisplay(() => false);

  return {
    modalContent: display ? (
      <Modal
        isOpen
        InnerComponent={innerComponent.current ?? <p>spinner :)</p>}
        closeModal={closeModal}
      />
    ) : null,
    getModal: getInnerComponent,
    closeModal,
  };
};

export default useDynamicModal;
