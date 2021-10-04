import modalCatalog from './modalCatalog';

const initModal = ({
  openedFromComponent,
  innerElementId,
  activeModalElement,
  optionalParams,
}) => {
  const { apiUrl, getResponseHandler } = modalCatalog[openedFromComponent];
  const { handler } = getResponseHandler(activeModalElement, optionalParams);
  const url = apiUrl(innerElementId);

  return {
    apiUrl: url,
    handleResponse: handler,
  };
};

export default initModal;
