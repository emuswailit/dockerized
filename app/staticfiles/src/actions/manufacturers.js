import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET MANUFACTURERS
export const getManufacturers = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/manufacturers", tokenConfig(getState))
    .then((res) => {
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} manufacturer entries retrieved from database!`,
            "success"
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No manufacturer entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_MANUFACTURERS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD DRUG CLASS
export const addManufacturer = (manufacturer) => (dispatch, getState) => {
  axios
    .post(
      "api/v1/drugs/manufacturers/create",
      manufacturer,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res);
      dispatch(
        showSnackbarMessage(
          "Manufacturers successfulyy added!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.ADD_MANUFACTURER,
        payload: res.data.manufacturer,
        submissionSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err);
      dispatch(showSnackbarMessage("An error occurred", "error"));
    });
};

//EDIT DRUG CLASS
export const changeManufacturer = (manufacturer, id) => (
  dispatch,
  getState
) => {
  axios
    .put(
      `api/v1/drugs/manufacturers/${id}/update`,
      manufacturer,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch(
        showSnackbarMessage(
          "Manufacturers successfully updated!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.EDIT_MANUFACTURER,
        payload: true,
        editUserSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE MANUFACTURER
export const deleteManufacturer = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/manufacturers/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: actionTypes.DELETE_MANUFACTURER,
        payload: id,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
