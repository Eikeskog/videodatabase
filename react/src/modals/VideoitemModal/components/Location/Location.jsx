import React from 'react';
import VerticalTabs from '../../../../common/components/TabbedContent/VerticalTabs/VerticalTabs';
import NearbyItems from './NearbyItems';
import Map from './Map';

// not implemented
const map = {
  header: 'Kart',
  component: <Map />,
};

const info = {
  header: 'Om sted',
  component: <p>asdf</p>,
};

const nearby = {
  header: 'I nærheten',
  component: <NearbyItems />,
};

const Location = () => <VerticalTabs tabsDict={{ map, info, nearby }} />;

export default Location;
