import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET BODY SYSTEMS
export const getBodySystems = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/body-systems", tokenConfig(getState))
    .then((res) => {
      console.log("results", res);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} body systems entries retrieved from database!`,
            "success",
            true,
            true
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No body system entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_BODY_SYSTEMS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      console.log(err)
      // dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD BODY_SYSTEM
export const addBodySystem = (bodysystem) => (dispatch, getState) => {
  axios
    .post("api/v1/drugs/body-systems/create", bodysystem, tokenConfig(getState))
    .then((res) => {
      console.log("res", res.data);
      dispatch(
        showSnackbarMessage("Body system successfully added!", "success")
      );
      dispatch({
        type: actionTypes.ADD_BODY_SYSTEM,
        payload: res.data.body_system,
      });
    })
    .catch((err) => {
      console.log("errr", err);
      dispatch(showSnackbarMessage("err.response.data.message", "error"));
    });
};

//EDIT BODY_SYSTEM
export const changeBodySystem = (bodysystem, id) => (dispatch, getState) => {
  axios
    .put(`api/v1/drugs/body-systems/${id}`, bodysystem, tokenConfig(getState))
    .then((res) => {
      showSnackbarMessage("Body system successfully updated!", "success");
      dispatch({
        type: actionTypes.EDIT_BODY_SYSTEM,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE BODY_SYSTEM
export const deleteBodySystem = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/body-systems/${id}`, tokenConfig(getState))
    .then((res) => {

      console.log("Rsponse ", res)
      dispatch(
        showSnackbarMessage("Body system successfully deleted!", "success")
      );
      dispatch({
        type: actionTypes.DELETE_BODY_SYSTEM,
        payload: id,
      });
    })
    .catch((err) => {
      console.log("Delete error", err)
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
