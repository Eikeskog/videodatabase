import initialState from './initialState';

export const responseDataToStateObj = (data) => {
  if (!data || !data?.access || !data?.user?.username?.length) return initialState;

  return {
    token: {
      access: data?.access,
      refresh: data?.refresh,
    },
    user: {
      id: data?.user?.id,
      username: data?.user?.username,
    },
    isLoggedIn: !!data?.user?.id,
    error: null,
    status: 'OK',
  };
};

export const localStorageLoad = () => {
  const json = JSON.parse(localStorage.getItem('user'));
  if (!json || !json?.token || !json?.token?.access?.length) return null;

  return json;
};

export const localStorageSave = (state) => {
  if (!state?.token || !state?.token?.access?.length) return;
  const json = JSON.stringify(state);
  localStorage.setItem('user', json);
};

export const localStorageClear = () => {
  localStorage.removeItem('user');
};

export const parseJwt = (jwt) => JSON.parse(atob(jwt.split('.')[1]));

export const tokenSecondsLeft = (jwt) => {
  if (!jwt.length || typeof jwt !== 'string' || !jwt.includes('.')) return 0;
  const decodedToken = parseJwt(jwt);
  if (!decodedToken?.exp) return 0;
  const exp = new Date(decodedToken.exp * 1000);
  return (exp.getTime() - Date.now()) / 1000;
};

export const tokenIsExpired = (jwt) => tokenSecondsLeft(jwt) <= 0;

export const tokenIsExpiring = (jwt) => tokenSecondsLeft(jwt) < 30;

export const getInitalState = () => {
  const localState = localStorageLoad();
  if (!localState?.token?.refresh?.length || !localState?.token?.access?.length) {
    return initialState;
  }
  const { refresh, access } = localState.token;

  if (tokenIsExpired(refresh)) {
    localStorageClear();
    return initialState;
  }

  if (tokenIsExpired(access)) {
    return { ...localState, status: 'EXPIRED' };
  }

  if (tokenIsExpiring(access)) {
    return { ...localState, status: 'EXPIRING' };
  }

  return localState;
};
