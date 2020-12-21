import * as actionTypes from "../actions/actionTypes";

const initialState = { msg: "", status: "", theresError: false };

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_ERRORS:
      return {
        msg: action.message,
        status: action.status,
        theresError: true,
      };

    case actionTypes.CLEAR_ERRORS:
      return {
        msg: null,
        status: null,
        theresError: false,
      };

    default:
      return state;
  }
}
