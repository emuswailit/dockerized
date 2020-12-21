import * as actions from "./actionTypes";

// SET LOADING
export const startLoading = () => {
  return {
    type: actions.LOADING,
    loading: true,
    success: false,
    failure: false,
    showForm: true,
  };
};

// TERMINATE ACTION WITH SUCCESS
export const endLoadingSuccess = () => {
  return {
    type: actions.LOADING,
    loading: false,
    success: true,
    failure: false,
    showForm: false,
  };
};

// TERMINATE ACTION WITH FAILURE

export const endLoadingFailure = () => {
  return {
    type: actions.LOADING,
    loading: false,
    success: false,
    failure: true,
    showForm: true,
  };
};
