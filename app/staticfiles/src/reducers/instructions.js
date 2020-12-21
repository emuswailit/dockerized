import * as actionTypes from "../actions/actionTypes";

const initialState = {
  instructions: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_INSTRUCTIONS:
      console.log("reducer", action.payload);
      return {
        ...state,

        instructions: action.payload,
        update: false,
      };

    case actionTypes.DELETE_INSTRUCTION:
      return {
        ...state,
        instructions: state.instructions.filter(
          (instruction) => instruction.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_INSTRUCTION:
      return {
        ...state,
        instructions: state.instructions.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_INSTRUCTION:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
