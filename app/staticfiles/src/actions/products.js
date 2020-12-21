import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET PRODUCTS
export const getProducts = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/products", tokenConfig(getState))
    .then((res) => {
      console.log("products", res);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} products entries retrieved from database!`,
            "success"
          )
        );
      } else {
        dispatch(
          showSnackbarMessage("No products entries in the database!", "error")
        );
      }
      dispatch({
        type: actionTypes.GET_PRODUCTS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD PRODUCT
export const addProduct = (product) => (dispatch, getState) => {
  axios
    .post("api/v1/drugs/products/create", product, tokenConfig(getState))
    .then((res) => {
      console.log("res", res);
      dispatch(
        showSnackbarMessage(
          "Product successfully added!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.ADD_PRODUCT,
        payload: res.data.product,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.detail, "error"));
    });
};

//EDIT PRODUCT
export const changeProduct = (product, id) => (dispatch, getState) => {
  axios
    .put(`api/v1/drugs/products/${id}/update`, product, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage(
          "Product successfully updated!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.EDIT_PRODUCT,
        payload: true,
        editUserSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE PRODUCT
export const deleteProduct = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/products/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: actionTypes.DELETE_PRODUCT,
        payload: id,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
