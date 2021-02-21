import * as actionTypes from "./actionTypes"
export const setErrors = (response_code, response_message, errors) => {
  return (dispatch) => {
    dispatch({
      type: actionTypes.GET_ERRORS,
      response_code,
      response_message,
      errors,
    })
  }
}

export const clearErrors = () => {
  return (dispatch) => {
    dispatch({
      type: actionTypes.CLEAR_ERRORS,
    })
  }
}
