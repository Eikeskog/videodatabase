const ThemeReducer = (state, action) => {
  switch (action.type) {
    case 'CHANGE_THEME':
      return { ...state, theme: action.payload };
    case 'CHANGE_NAME':
      return { ...state, name: action.payload };
    default:
      return state;
  }
};

export default ThemeReducer;
