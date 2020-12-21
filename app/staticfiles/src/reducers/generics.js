import * as actionTypes from "../actions/actionTypes";

const initialState = {
  generics: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_GENERICS:
      console.log("reducer", action.payload);
      return {
        ...state,

        generics: action.payload,
        update: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_GENERIC:
      return {
        ...state,
        generics: state.generics.filter(
          (generic) => generic.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_GENERIC:
      return {
        ...state,
        generics: state.generics.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_GENERIC:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
