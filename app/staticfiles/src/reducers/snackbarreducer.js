import * as actionTypes from "../actions/actionTypes";

const snackbarreducer = (
  state = { success: false, update: false, loading: false },
  action
) => {
  switch (action.type) {
    case actionTypes.SNACKBAR_SUCCESS:
      return {
        ...state,
        update: action.update,
        success: action.success,
        severity: action.severity,
        successSnackbarOpen: true,
        successSnackbarMessage: action.message,
        loading: true,
      };
    case actionTypes.SNACKBAR_CLEAR:
      return {
        ...state,
        update: false,
        success: false,
        severity: "",
        successSnackbarOpen: false,
        errorSnackbarOpen: false,
        infoSnackbarOpen: false,
        loading: false,
      };
    default:
      return state;
  }
};

export default snackbarreducer;
