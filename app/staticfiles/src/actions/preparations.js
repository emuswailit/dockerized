import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET PREPARATIONS
export const getPreparations = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/preparations", tokenConfig(getState))
    .then((res) => {
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} preparation entries retrieved from database!`,
            "success"
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No preparation entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_PREPARATIONS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD PREPARATION
export const addPreparation = (preparation) => (dispatch, getState) => {
  axios
    .post(
      "api/v1/drugs/preparations/create",
      preparation,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res);
      dispatch(
        showSnackbarMessage(
          "Preparation successfully added!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.ADD_PREPARATION,
        payload: res.data.preparation,
      });
    })
    .catch((err) => {
      console.log("err", err);
      dispatch(showSnackbarMessage(err.response.data.detail, "error"));
    });
};

//EDIT PREPARATION
export const changePreparation = (preparation, id) => (dispatch, getState) => {
  axios
    .put(
      `api/v1/drugs/preparations/${id}/update`,
      preparation,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch(
        showSnackbarMessage(
          "Preparation successfully updated!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.EDIT_PREPARATION,
        payload: true,
        editUserSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE PREPARATION
export const deletePreparation = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/preparations/${id}/update`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: actionTypes.DELETE_PREPARATION,
        payload: id,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
