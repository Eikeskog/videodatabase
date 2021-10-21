import React from 'react';
import Location from './components/Location/Location';
import File from './components/File/File';
import Lists from './components/Lists/Lists';
import Tags from './components/Tags/Tags';

const tabsDict = ({ localPaths, tags }) => ({
  location: {
    header: 'Sted',
    component: <Location />,
  },
  date: {
    header: 'Dato',
    component: <p>test1</p>,
  },
  file: {
    header: 'Filinfo',
    component: <File json={localPaths} />,
  },
  lists: {
    header: 'Lister',
    component: <Lists />,
  },
  itemTags: {
    header: 'Tags',
    component: <Tags tags={tags} />,
  },
  timeline: {
    header: 'Tidslinje',
    component: <p>test5</p>,
  },
});

export default tabsDict;
