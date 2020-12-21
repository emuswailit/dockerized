import * as actionTypes from "../actions/actionTypes";

const initialState = {
  posologies: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_POSOLOGIES:
      return {
        ...state,

        posologies: action.payload,
        update: false,
      };

    case actionTypes.DELETE_POSOLOGY:
      return {
        ...state,
        posologies: state.posologies.filter(
          (posology) => posology.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_POSOLOGY:
      return {
        ...state,
        posologies: state.posologies.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_POSOLOGY:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
