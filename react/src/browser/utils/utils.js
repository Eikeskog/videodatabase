import { modelNames } from '../../common/constants/constants';
import { isEmpty } from '../../common/utils/utils';

const prepareRestApiParams = (searchfilters) => {
  const params = {};
  Object.keys(searchfilters).forEach((filterType) => {
    if (!isEmpty(searchfilters[filterType])) {
      params[`${modelNames[filterType]}__in`] = Object.keys(searchfilters[filterType]).join(',');
    }
  });
  return params;
};

export default prepareRestApiParams;

// export const flattenFilterMap = (obj) => {
//   if (!obj || isEmpty(obj)) return null;

//   return Object.keys(obj)
//     .forEach((filterType) => {
//       Object.keys(obj[filterType]).map((id) => (
//         { type: filterType, id, name: obj[filterType][id] }
//       ));
//     });
// };
