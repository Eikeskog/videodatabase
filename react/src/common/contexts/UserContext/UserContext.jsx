import React, {
  createContext,
  useContext,
  useCallback,
  // useEffect,
} from 'react';
import PropTypes from 'prop-types';

import useAuth from '../../hooks/useAuth/useAuth';
import useAuthorizedFetch from '../../hooks/useAuthorizedFetch/useAuthorizedFetch';

const Context = createContext({
  useAuth: () => {},
  useAuthorizedFetch: () => {},
});

export const useUserContext = () => useContext(Context);

const UserContext = ({ children }) => {
  const auth = useAuth();
  const authorizedFetch = useCallback(useAuthorizedFetch(auth), [auth]);
  // const userLists = useUserListsState(authorizedFetch);

  return (
    <Context.Provider
      value={{
        useAuth: useCallback(auth, [auth.headers, auth.isLoggedIn]),
        useAuthorizedFetch: useCallback(authorizedFetch, [auth.headers, auth.isLoggedIn]),
        // : useCallback(authorizedFetch, [auth.headers, auth.isLoggedIn]),
        // useAuthorizedFetch: authorizedFetch,
        // useUserLists: userLists,
      }}
    >
      {children}
    </Context.Provider>
  );
};

UserContext.propTypes = {
  children: PropTypes.node.isRequired,
};

export default UserContext;
