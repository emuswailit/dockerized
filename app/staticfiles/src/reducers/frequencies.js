import * as actionTypes from "../actions/actionTypes";

const initialState = {
  frequencies: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_FREQUENCIES:
      return {
        ...state,

        frequencies: action.payload,
        update: false,
      };

    case actionTypes.DELETE_FREQUENCY:
      return {
        ...state,
        frequencies: state.frequencies.filter(
          (frequency) => frequency.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_FREQUENCY:
      return {
        ...state,
        frequencies: state.frequencies.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_FREQUENCY:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
