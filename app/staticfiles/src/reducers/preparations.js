import * as actionTypes from "../actions/actionTypes";

const initialState = {
  preparations: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_PREPARATIONS:
      console.log("reducer", action.payload);
      return {
        ...state,

        preparations: action.payload,
        update: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_PREPARATION:
      return {
        ...state,
        preparations: state.preparations.filter(
          (preparation) => preparation.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_PREPARATION:
      return {
        ...state,
        preparations: state.preparations.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_PREPARATION:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
