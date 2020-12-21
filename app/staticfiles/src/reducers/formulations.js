import * as actionTypes from "../actions/actionTypes";

const initialState = {
  formulations: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_FORMULATIONS:
      console.log("reducer", action.payload);
      return {
        ...state,

        formulations: action.payload,
        update: false,
      };

    case actionTypes.DELETE_FORMULATION:
      return {
        ...state,
        formulations: state.formulations.filter(
          (instruction) => instruction.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_FORMULATION:
      return {
        ...state,
        formulations: state.formulations.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_FORMULATION:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
