import axios from 'axios';
import { useState } from 'react';

const useAuthorizedFetch = (auth) => {
  const {
    headers,
    isLoggedIn,
    tokenIsExpiring,
    refresh,
  } = auth;
  const [isFetching, setIsFetching] = useState(null);

  const authorizedFetch = ({
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
  };

  return {
    authorizedFetch,
    isFetching,
  };
};

export default useAuthorizedFetch;
