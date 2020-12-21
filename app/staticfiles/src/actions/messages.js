import * as actionTypes from "./actionTypes";

export const createMessage = (msg, severity) => {
  return {
    type: actionTypes.CREATE_MESSAGE,
    message: msg,
    severity: severity,
  };
};

// RETURN ERRORS
export const returnErrors = (msg, status) => {
  return {
    type: actionTypes.GET_ERRORS,
    message: msg,
    status: status,
  };
};

// RETURN ERRORS
export const clearErrors = () => {
  return {
    type: actionTypes.CLEAR_ERRORS,
    message: null,
    status: null,
  };
};
