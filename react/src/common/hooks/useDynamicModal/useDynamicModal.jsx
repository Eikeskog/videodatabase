import React, {
  useRef, useState, useCallback, useMemo,
} from 'react';
import Modal from '../../components/Modal/Modal';
import initModal from './initModal';
import { useUserContext } from '../../contexts/UserContext/UserContext';

const useDynamicModal = () => {
  const innerComponent = useRef();
  const [display, setDisplay] = useState(false);

  const {
    useAuth: { isLoggedIn },
    useAuthorizedFetch: { authorizedFetch },
  } = useUserContext();

  const setInnerComponent = useCallback((Component) => {
    innerComponent.current = Component;
    if (!Component) return;
    setDisplay(() => true);
  }, []);

  const getInnerComponent = useCallback(({
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
  }, [isLoggedIn]);

  const closeModal = useCallback(() => {
    setDisplay(() => false);
    setInnerComponent(null);
  }, []);

  return {
    modalContent: display ? (
      <Modal
        isOpen
        InnerComponent={innerComponent.current ?? <p>spinner :)</p>}
        closeModal={closeModal}
      />
    ) : null,
    getModal: useMemo(() => getInnerComponent, [isLoggedIn]),
    closeModal: useMemo(() => closeModal, [display]),
  };
};

export default useDynamicModal;
