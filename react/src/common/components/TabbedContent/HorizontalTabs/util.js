export const headerLeftOffset = ({ tabsCount, index }) => `${(100 / tabsCount) * index}%`;

export const headerStyle = ({ tabsCount, index, headerWidth }) => ({
  width: headerWidth,
  left: headerLeftOffset({ tabsCount, index }),
});
