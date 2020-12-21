import * as actionTypes from "../actions/actionTypes";

const initialState = {
  token: localStorage.getItem("token"),
  isAuthenticated: false,
  isLoading: false,
  user: {},
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.USER_LOADING:
      return {
        ...state,
        isLoading: true,
      };
    case actionTypes.USER_LOADED:
      return {
        ...state,
        isAuthenticated: true,
        isLoading: false,
        user: action.payload,
      };
    case actionTypes.LOGIN_SUCCESS:
    case actionTypes.REGISTER_SUCCESS:
      localStorage.setItem("token", action.payload.token);
      return {
        ...state,

        isAuthenticated: true,
        isLoading: false,
        user: action.payload,
      };
    case actionTypes.AUTH_ERROR:
    case actionTypes.LOGIN_FAIL:
    case actionTypes.LOGOUT_SUCCESS:
    case actionTypes.REGISTER_FAIL:
      localStorage.removeItem("token");
      return {
        ...state,
        token: null,
        user: {},
        isAuthenticated: false,
        isLoading: false,
      };
    default:
      return state;
  }
}
