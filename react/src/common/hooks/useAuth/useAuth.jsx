import axios from 'axios';
import { useEffect, useState } from 'react';
import initialState from './initialState';
import {
  getInitalState,
  responseDataToStateObj,
  localStorageSave,
  localStorageClear,
  tokenSecondsLeft,
  tokenIsExpired,
  tokenIsExpiring,
} from './utils';
import urls from '../../../dev_urls';

const useAuth = () => {
  const [state, setState] = useState(() => getInitalState());

  const logIn = async ({ email, password }) => {
    if (state?.isLoggedIn) return;

    axios.post(urls.LOGIN, { email, password })
      .then((response) => {
        const stateObj = responseDataToStateObj(response?.data);
        setState(() => stateObj);
        localStorageSave(stateObj);
      })
      .catch((error) => {
        setState(() => ({ ...initialState, error: error.response }));
      });
  };

  const refresh = async (onRefresh) => {
    if (!state?.token?.refresh) {
      setState(() => ({
        ...initialState,
        status: 'ERROR',
        error: 'MISSING_REFRESH_TOKEN',
      }));

      return;
    }
    try {
      const { data } = await axios.post(urls.REFRESH, { refresh: state.token.refresh });
      if (!data?.access?.length) {
        setState(() => ({
          ...initialState,
          status: 'ERROR',
          error: 'TOKEN_OBTAIN_ERROR',
        }));
        localStorageClear();
      }

      const stateObj = {
        ...state,
        token: {
          ...state.token,
          access: data?.access,
        },
        status: 'OK',
      };

      setState(() => stateObj);
      localStorageSave(stateObj);

      if (onRefresh) onRefresh(data?.access);
    } catch (error) {
      setState(() => ({
        ...initialState,
        status: 'ERROR',
        error: error.response,
      }));
      if (onRefresh) onRefresh(error);
    }
  };

  const logOut = () => {
    localStorageClear();
    setState(() => initialState);
  };

  useEffect(() => {
    if (state?.status === 'OK') return;
    if (state?.status === 'EXPIRED' || state?.status === 'EXPIRING') refresh();
  }, [state]);

  return {
    headers: state?.token?.access?.length ? {
      Authorization: `Bearer ${state.token.access}`,
    } : {},
    user: state?.user,
    isLoggedIn: state?.isLoggedIn,
    logIn,
    logOut,
    refresh,
    status: state?.status,
    error: state?.error,
    tokenSecondsLeft: () => tokenSecondsLeft(state?.token?.access),
    tokenIsExpired: () => tokenIsExpired(state?.token?.access),
    tokenIsExpiring: () => tokenIsExpiring(state?.token?.access),
  };
};

export default useAuth;
