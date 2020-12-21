import * as actionTypes from "../actions/actionTypes";
import _ from "lodash";

const initialState = {
  distributors: [],
  count: 0,
  previous: "",
  next: "",
  update: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case actionTypes.GET_DISTRIBUTORS:
      //Check if an item is already in the array and exclude it from those to be added to the list to avoid duplicated
      let ids = new Set(state.distributors.map((e) => e.id));
      let newState = action.payload.distributors
        .filter((a) => !ids.has(a.id))
        .concat(state.distributors);

      return {
        ...state,
        distributors: newState,
        count: action.payload.count,
        previous: action.payload.previous,
        next: action.payload.next,
        update: false,
      };

    case actionTypes.DELETE_DISTRIBUTOR:
      return {
        ...state,
        //Added just for the sake of closing the edit modal
        //Remove the edited item from the array
        distributors: state.distributors.filter(
          (distributor) => distributor.id !== action.payload
        ),
        update: true,
      };

    case actionTypes.ADD_DISTRIBUTOR:
      return {
        ...state,
        distributors: state.distributors.concat(action.payload),
        update: true,
      };

    case actionTypes.EDIT_DISTRIBUTOR:
      return {
        ...state,
        update: false,
        //Remove the edited item from the array and then add the updated copy
        distributors: state.distributors
          .filter((distributor) => distributor.id !== action.payload.id)
          .concat(action.payload),

        update: true,
      };

    default:
      return state;
  }
}
