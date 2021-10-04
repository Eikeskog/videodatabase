import { directories } from '../constants/constants';

export const capitalizeFirstChar = (str) => {
  if (!str || typeof str !== 'string') return null;
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const isEmpty = (obj) => {
  if (!obj || typeof obj !== 'object') return true;
  return Object.keys(obj).length === 0;
};

export const removeLeadingDigits = (str) => {
  if (!str || typeof str !== 'string') return null;
  return str.replace(/^\d+\s*/, '').replace(/^\.s*/, '').trim();
};

export const shortenLocalPath = (str) => {
  if (!str || typeof str !== 'string') return null;
  const slashIndexes = [...str.matchAll(new RegExp('/', 'gi'))].map((a) => a.index);

  const projectFolderName = str.slice(slashIndexes[1] + 1, slashIndexes[2]);
  const rolltype = str.slice(slashIndexes[3] + 1, slashIndexes[4]);
  const relativePath = str.slice(slashIndexes[4] + 1);

  const strFormat = `${removeLeadingDigits(projectFolderName)}/${relativePath} (${removeLeadingDigits(rolltype)})`;
  return strFormat;
};

export const secondsToHms = (seconds) => {
  let str = '';

  const h = ((seconds - (seconds % 3600)) / 3600) % 60;
  const m = ((seconds - (seconds % 60)) / 60) % 60;
  const s = seconds % 60;

  if (h) str += (`${h.toString()}t `);
  if (m) str += (`${m.toString()}m `);
  if (s) str += (`${s.toString()}s`);

  return str;
};

export const getThumbnailUrl = (videoitemId, thumbnailIndex) => {
  if (!videoitemId || !thumbnailIndex) return null;
  const format = thumbnailIndex.toString().padStart(2, '0');
  return `${directories.static_thumbnails}/${videoitemId}/${format}.jpg`;
};

export const arrFirstItem = (array) => {
  if (!array || typeof array !== 'object' || !array.length) return null;
  return array[0];
};

export const strPrepend = (str, prepend) => prepend + str;

export const prependDictionaryKeys = (obj, prepend) => {
  if (!obj || typeof obj !== 'object' || isEmpty(obj)) return null;

  const prependedDictionary = {};
  Object.keys(obj).forEach((key) => {
    prependedDictionary[strPrepend(key, prepend)] = obj[key];
  });
  return prependedDictionary;
};

export const prependedKeysDictFromSingleEntryJsonList = (
  jsonList, prependBy,
) => (
  prependDictionaryKeys(arrFirstItem(jsonList), prependBy)
);

export const localeDateStringNorwegianBugFix = (date, longOrShort = 'short', allNumerical) => {
  const monthNames = [
    { short: 'jan.', long: 'januar' },
    { short: 'feb.', long: 'februar' },
    { short: 'mars', long: 'mars' },
    { short: 'april', long: 'april' },
    { short: 'mai', long: 'mai' },
    { short: 'juni', long: 'juni' },
    { short: 'juli', long: 'juli' },
    { short: 'aug.', long: 'august' },
    { short: 'sep.', long: 'september' },
    { short: 'okt.', long: 'oktober' },
    { short: 'nov.', long: 'november' },
    { short: 'des.', long: 'desember' },
  ];

  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const month = (dateObj.getMonth() + 1).toString();
  const daynumber = dateObj.getDate().toString();
  const year = dateObj.getFullYear().toString();

  if (allNumerical) {
    if (longOrShort === 'long') {
      return `${daynumber}/${month}-${year}`;
    }
    return `${daynumber}/${month}-${year.substring(2)}`;
  }
  return `${daynumber}. ${monthNames[month][longOrShort]} ${year}`;
};

export const dateRangeToSearchParameter = (startDate, endDate) => {
  const format = (date) => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    const month = (dateObj.getMonth() + 1).toString();
    const daynumber = dateObj.getDate().toString();
    const year = dateObj.getFullYear().toString();
    return `${year}-${month}-${daynumber}`;
  };

  return `${format(startDate)}_${format(endDate)}`;
};

export const dateRangeToString = (startDate, endDate, locale = 'no-NO') => {
  if (locale === 'no-NO') {
    const localeBugFix = (date) => (localeDateStringNorwegianBugFix(date, 'short', true));
    if (startDate.toString() === endDate.toString()) {
      return `${localeBugFix(startDate)}`;
    }
    return `${localeBugFix(startDate)} - ${localeBugFix(endDate)}`;
  }
  return null;
};
