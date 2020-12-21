import * as actionTypes from "../actions/actionTypes";

const initialState = {
  drugsubclasses: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_DRUG_SUB_CLASSES:
      console.log("reducer", action.payload);
      return {
        ...state,

        drugsubclasses: action.payload,
        update: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_DRUG_SUB_CLASS:
      return {
        ...state,
        drugsubclasses: state.drugsubclasses.filter(
          (drugsubclass) => drugsubclass.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_DRUG_SUB_CLASS:
      return {
        ...state,
        drugsubclasses: state.drugsubclasses.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_DRUG_SUB_CLASS:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
