import * as actionTypes from "../actions/actionTypes"

const initialState = {
  users: [],
  update: false,
  response_code: null,
}

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_USERS:
      console.log("reducer", action.payload)
      return {
        ...state,
        user: null,
        users: action.payload,
        update: false,
        errors: [],
      }

    case actionTypes.DELETE_USER:
      return {
        ...state,
        users: state.users.filter((user) => user.id !== action.payload),
      }

    case actionTypes.ADD_USER:
      return {
        ...state,

        errors: [],
        user: action.user,
        users: state.users.concat(action.user),
        response_code: action.response_code,
        response_message: action.response_message,
        errors: action.errors,
      }

    case actionTypes.EDIT_USER:
      return {
        ...state,
        errors: [],
        user: action.user,
        // users: state.users.concat(action.user),
        response_code: action.response_code,
        response_message: action.response_message,
        errors: action.errors,
      }

    case actionTypes.CLEAR_USERS:
      return {
        ...state,
        users: [],
      }

    default:
      return state
  }
}
