import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET FREQUENCIES
export const getFrequencies = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/frequencies", tokenConfig(getState))
    .then((res) => {
      console.log("res data", res.data);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} frequencies entries retrieved from database!`,
            "success",
            true,
            true
          )
        );
      } else {
        dispatch(
          showSnackbarMessage("No frequency entries in the database!", "error")
        );
      }
      dispatch({
        type: actionTypes.GET_FREQUENCIES,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD FREQUENCY
export const addFrequency = (frequency) => (dispatch, getState) => {
  axios
    .post("api/v1/drugs/frequencies/create", frequency, tokenConfig(getState))
    .then((res) => {
      console.log("res", res.data);
      dispatch(showSnackbarMessage("Frequency successfully added!", "success"));
      dispatch({
        type: actionTypes.ADD_FREQUENCY,
        payload: res.data.frequency,
      });
    })
    .catch((err) => {
      console.log("error", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.detail, "error"));
    });
};

//EDIT FREQUENCY
export const changeFrequency = (frequency, id) => (dispatch, getState) => {
  axios
    .put(
      `api/v1/drugs/frequencies/${id}/update`,
      frequency,
      tokenConfig(getState)
    )
    .then((res) => {
      showSnackbarMessage("Frequency successfully updated!", "success");
      dispatch({
        type: actionTypes.EDIT_FREQUENCY,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE FREQUENCY
export const deleteFrequency = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/frequencies/${id}/update`, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage("Frequency successfully deleted!", "success")
      );
      dispatch({
        type: actionTypes.DELETE_FREQUENCY,
        payload: id,
      });
    })
    .catch((err) => {
      console.log(err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
