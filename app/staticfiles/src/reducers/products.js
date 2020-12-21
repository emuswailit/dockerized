import * as actionTypes from "../actions/actionTypes";

const initialState = {
  products: [],
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_PRODUCTS:
      console.log("reducer", action.payload);
      return {
        ...state,

        products: action.payload,
        update: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_PRODUCT:
      return {
        ...state,
        products: state.products.filter(
          (product) => product.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_PRODUCT:
      return {
        ...state,
        products: state.products.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_PRODUCT:
      return {
        ...state,
        update: action.payload,
        update: true,
      };

    default:
      return state;
  }
}
