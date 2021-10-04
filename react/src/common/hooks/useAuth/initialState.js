const initialState = {
  token: {
    access: '',
    refresh: '',
  },
  user: {
    id: 0,
    username: '',
  },
  isLoggedIn: false,
  error: null,
  status: 'OK',
};

export default initialState;
