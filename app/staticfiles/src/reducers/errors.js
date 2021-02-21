import * as actionTypes from "../actions/actionTypes"

const initialState = {response_message: null, response_code: null, errors: []}

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_ERRORS:
      return {
        response_message: action.response_message,
        response_code: action.response_code,
        errors: action.errors,
      }

    case actionTypes.CLEAR_ERRORS:
      return {
        response_message: null,
        response_code: null,
        errors: [],
      }

    default:
      return state
  }
}
