import { modelNames } from '../../common/constants/constants';
import { isEmpty } from '../../common/utils/utils';

const prepareRestParams = (searchfilters) => {
  const params = {};
  Object.keys(searchfilters).forEach((filterType) => {
    if (!isEmpty(searchfilters[filterType])) {
      params[`${modelNames[filterType]}__in`] = Object.keys(searchfilters[filterType]).join(',');
    }
  });
  return params;
};

export default prepareRestParams;
