import * as actionTypes from "../actions/actionTypes";

const initialState = {
  products: [],
  loading: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_PRODUCTS:
      console.log("reducer", action.payload);
      return {
        ...state,

        products: action.payload,
        loading: false, //Has the purpose of resetting the update redux variable for reloading drug classes
      };

    case actionTypes.DELETE_PRODUCT:
      return {
        ...state,
        products: state.products.filter(
          (product) => product.id !== action.payload
        ),
        loading: true,
      };

      case actionTypes.ADD_PRODUCT_REQUEST:
        return {
          ...state,
          products: state.products,
          loading: true,
          error: null
        };
    case actionTypes.ADD_PRODUCT_SUCCESS:
      return {
        ...state,
        products: state.products.concat(action.payload),
        loading: false,
        
      };

    case actionTypes.ADD_PRODUCT_FAIL:
        return {
          ...state,
          products: state.products,
          loading: false,
          error: action.payload
        };

    case actionTypes.EDIT_PRODUCT:
      return {
        ...state,
        loading: action.payload,
        loading: true,
      };

    default:
      return state;
  }
}
