import * as actionTypes from "./actionTypes";
export const showSnackbarMessage = (message, severity, success, update) => {
  return (dispatch) => {
    dispatch({
      type: actionTypes.SNACKBAR_SUCCESS,
      message,
      severity,
      success,
      update,
    });
  };
};

export const clearSnackbar = () => {
  return (dispatch) => {
    dispatch({
      type: actionTypes.SNACKBAR_CLEAR,
    });
  };
};
