import * as actionTypes from "../actions/actionTypes";

const initialState = {
  drugclasses: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_DRUG_CLASSES:
      console.log("reducer", action.payload);
      return {
        ...state,

        drugclasses: action.payload,
        update: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_DRUG_CLASS:
      return {
        ...state,
        drugclasses: state.drugclasses.filter(
          (drugclass) => drugclass.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_DRUG_CLASS:
      return {
        ...state,
        drugclasses: state.drugclasses.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_DRUG_CLASS:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
