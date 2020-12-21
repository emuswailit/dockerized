import { CREATE_MESSAGE } from "../actions/actionTypes";

const initialState = { messages: "", theresMessage: false };

export default function (state = initialState, action) {
  switch (action.type) {
    case CREATE_MESSAGE:
      return {
        ...state,
        message: action.message,
        severity: action.severity,
      };
    default:
      return state;
  }
}
