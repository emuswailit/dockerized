import * as actionTypes from "../actions/actionTypes"

const initialState = {
  categories: [],
  update: false,
}

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_CATEGORIES:
      return {
        ...state,

        categories: action.payload,
        update: false,
      }

    case actionTypes.DELETE_CATEGORY:
      return {
        ...state,
        categories: state.categories.filter(
          (category) => category.id !== action.payload
        ),
        update: true,
      }

    case actionTypes.ADD_CATEGORY:
      return {
        ...state,
        categories: state.categories.concat(action.payload),
        update: true,
      }

    case actionTypes.EDIT_CATEGORY:
      return {
        ...state,
        update: action.payload,
        update: true,
      }

    default:
      return state
  }
}
