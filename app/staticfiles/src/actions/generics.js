import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET GENERICS
export const getGenerics = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/generics", tokenConfig(getState))
    .then((res) => {
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} generics entries retrieved from database!`,
            "success"
          )
        );
      } else {
        dispatch(
          showSnackbarMessage("No generics entries in the database!", "error")
        );
      }
      dispatch({
        type: actionTypes.GET_GENERICS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD GENERIC
export const addGeneric = (generic) => (dispatch, getState) => {
  axios
    .post("api/v1/drugs/generics/create", generic, tokenConfig(getState))
    .then((res) => {
      console.log("create generic", res);
      dispatch(
        showSnackbarMessage(
          "Generic successfully added!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.ADD_GENERIC,
        payload: res.data.generic,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.detail, "error"));
    });
};

//EDIT GENERIC
export const changeGeneric = (generic, id) => (dispatch, getState) => {
  axios
    .put(`api/v1/drugs/generics/${id}/update`, generic, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage(
          "Generic successfully updated!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.EDIT_GENERIC,
        payload: true,
        editUserSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE GENERIC
export const deleteGeneric = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/generics/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: actionTypes.DELETE_GENERIC,
        payload: id,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
