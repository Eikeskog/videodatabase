import urls from '../../../dev_urls';
import initVideoitemModal from '../../../modals/VideoitemModal/initVideoitemModal';

const modalCatalog = {
  thumbnailboxOuter: {
    apiUrl: (videoitemId) => `${urls.SINGLE_VIDEOITEM}?pk=${videoitemId}`,
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
