import initVideoitemModal from './Modals/VideoitemModal/initVideoitemModal';

const modalCatalog = {
  thumbnailboxOuter: {
    apiUrl: (videoitemId) => `http://localhost:8000/api/entry/videoitem/?pk=${videoitemId}`,
    getResponseHandler: (activeModalElement, optionalParams) => ({
      handler(json) {
        if (!Array.isArray(json) || json.length < 1) return null;
        const data = json[0];
        const Component = initVideoitemModal(data, activeModalElement, optionalParams);
        return Component;
      },
    }),
  },
};

export default modalCatalog;
