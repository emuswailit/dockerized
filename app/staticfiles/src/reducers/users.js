import * as actionTypes from "../actions/actionTypes";

const initialState = {
  users: [],
  update: false,
  submissionSuccessful: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_USERS:
      console.log("reducer", action.payload);
      return {
        ...state,

        users: action.payload,
        update: false,
      };

    case actionTypes.DELETE_USER:
      return {
        ...state,
        users: state.users.filter((user) => user.id !== action.payload),
      };

    case actionTypes.ADD_USER:
      return {
        ...state,
        users: state.users.concat(action.payload),
        submissionSuccessful: action.submissionSuccessful,
      };

    case actionTypes.EDIT_USER:
      return {
        ...state,
        update: action.payload,
        editUserSuccessful: action.editUserSuccessful,
      };

    case actionTypes.CLEAR_USERS:
      return {
        ...state,
        users: [],
      };

    default:
      return state;
  }
}
