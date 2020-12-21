import * as actionTypes from "../actions/actionTypes";
const initialState = {
  loading: false,
  success: false,
  failure: false,
  showForm: true,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.LOADING:
      return {
        ...state,
        loading: action.loading,
        success: action.success,
        failure: action.failure,
        showForm: action.showForm,
      };

    default:
      return state;
  }
}
