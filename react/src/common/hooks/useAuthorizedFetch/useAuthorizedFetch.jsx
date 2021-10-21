import axios from 'axios';
import { useState, useCallback } from 'react';

const useAuthorizedFetch = (auth) => {
  const {
    headers,
    isLoggedIn,
    tokenIsExpiring,
    refresh,
  } = auth;
  const [isFetching, setIsFetching] = useState(null);

  const authorizedFetch = useCallback(({
    method = 'get',
    url,
    params = {},
    body = {},
    updatedHeaders,
    handleResponse,
    handleError,
  }) => {
    if (!isLoggedIn) return;

    setIsFetching(url);

    const request = async () => {
      try {
        const { data } = await axios({
          method,
          url,
          headers: updatedHeaders ?? headers,
          params,
          data: body,
        });
        handleResponse(data);
        setIsFetching(null);
      } catch (error) {
        setIsFetching(null);
        handleError(error);
      }
    };

    if (!tokenIsExpiring() || updatedHeaders) {
      request();
    } else {
      refresh((jwt) => authorizedFetch({
        method,
        url,
        params,
        body,
        updatedHeaders: {
          ...headers,
          Authorization: `Bearer ${jwt}`,
        },
        handleResponse,
        handleError,
      }));
    }
  }, [isLoggedIn, headers]);

  return {
    authorizedFetch,
    isFetching,
  };
};

export default useAuthorizedFetch;
