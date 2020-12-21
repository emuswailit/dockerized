import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET POSOLOGIES
export const getPosologies = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/posologies", tokenConfig(getState))
    .then((res) => {
      console.log("res data", res.data);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} posologies entries retrieved from database!`,
            "success",
            true,
            true
          )
        );
      } else {
        dispatch(
          showSnackbarMessage("No posology entries in the database!", "error")
        );
      }
      dispatch({
        type: actionTypes.GET_POSOLOGIES,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD POSOLOGY
export const addPosology = (posology) => (dispatch, getState) => {
  axios
    .post("api/v1/drugs/posologies/create", posology, tokenConfig(getState))
    .then((res) => {
      console.log("res", res.data);
      dispatch(showSnackbarMessage("Posology successfully added!", "success"));
      dispatch({
        type: actionTypes.ADD_POSOLOGY,
        payload: res.data.posology,
      });
    })
    .catch((err) => {
      console.log("erroe", err);
      dispatch(showSnackbarMessage("err.response.data.message", "error"));
    });
};

//EDIT POSOLOGY
export const changePosology = (posology, id) => (dispatch, getState) => {
  axios
    .put(
      `api/v1/drugs/posologies/${id}/update`,
      posology,
      tokenConfig(getState)
    )
    .then((res) => {
      showSnackbarMessage("Posology successfully updated!", "success");
      dispatch({
        type: actionTypes.EDIT_POSOLOGY,
      });
    })
    .catch((err) => {
      console.log("error", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE POSOLOGY
export const deletePosology = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/posologies/${id}/update`, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage("Posology successfully deleted!", "success")
      );
      dispatch({
        type: actionTypes.DELETE_POSOLOGY,
        payload: id,
      });
    })
    .catch((err) => {
      console.log(err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
