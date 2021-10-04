import { createRef } from 'react';

const useMultipleRefs = (refNames = []) => {
  const refs = refNames.reduce((a, x) => ({ ...a, [x]: createRef() }), {});

  const onChange = (e) => {
    const { name, value } = e.target;
    refs[name] = value;
  };

  return { refs, onChange };
};

export default useMultipleRefs;
