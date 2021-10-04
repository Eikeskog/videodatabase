import { useRef, useState } from 'react';

import { useUserContext } from '../contexts/UserContext/UserContext';
import urls from '../../dev_urls';

const BASE_URL = urls.TYPING_HINTS;

const fetch = async ({
  authorizedFetch, itemType, ref, handleResponse, handleError,
}) => {
  authorizedFetch({
    method: 'get',
    url: `${BASE_URL}${itemType}/?s=${ref?.current?.value}`,
    handleResponse,
    handleError,
  });
};

const useTypingHints = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [results, setResults] = useState([]);

  const { useAuthorizedFetch } = useUserContext();
  const { authorizedFetch } = useAuthorizedFetch;

  const ref = useRef();

  const handleResponse = (data) => {
    setResults(() => data);
    setIsLoading(false);
  };

  const handleError = (error) => {
    console.log(error);
    setIsLoading(false);
  };

  const onChange = (itemType) => {
    if (!ref?.current?.value) {
      setIsTyping(false);
      setIsLoading(false);
      return;
    }
    setIsTyping(true);
    setIsLoading(true);
    fetch({
      authorizedFetch, itemType, ref, handleResponse, handleError,
    });
  };

  const resetHints = () => {
    setIsTyping(false);
    setIsLoading(false);
    setResults([]);
  };

  return {
    ref,
    isTyping,
    onChange,
    results,
    isLoading,
    resetHints,
  };
};

export default useTypingHints;
