import React, {
  createContext,
  useContext,
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
  const authorizedFetch = useAuthorizedFetch(auth);

  return (
    <Context.Provider
      value={{
        useAuth: auth,
        useAuthorizedFetch: authorizedFetch,
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
