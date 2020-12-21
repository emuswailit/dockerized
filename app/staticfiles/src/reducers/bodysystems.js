import * as actionTypes from "../actions/actionTypes";

const initialState = {
  bodysystems: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_BODY_SYSTEMS:
      console.log("reducer", action.payload);
      return {
        ...state,

        bodysystems: action.payload,
        update: false,
      };

    case actionTypes.DELETE_BODY_SYSTEM:
      return {
        ...state,
        bodysystems: state.bodysystems.filter(
          (bodysystem) => bodysystem.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_BODY_SYSTEM:
      return {
        ...state,
        bodysystems: state.bodysystems.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_BODY_SYSTEM:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
