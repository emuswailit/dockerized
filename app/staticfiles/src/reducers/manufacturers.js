import * as actionTypes from "../actions/actionTypes";

const initialState = {
  manufacturers: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_MANUFACTURERS:
      console.log("reducer", action.payload);
      return {
        ...state,

        manufacturers: action.payload,
        update: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_MANUFACTURER:
      return {
        ...state,
        manufacturers: state.manufacturers.filter(
          (manufacturer) => manufacturer.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_MANUFACTURER:
      return {
        ...state,
        manufacturers: state.manufacturers.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_MANUFACTURER:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
