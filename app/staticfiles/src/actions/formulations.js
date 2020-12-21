import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET FORMULATIONS
export const getFormulations = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/formulations", tokenConfig(getState))
    .then((res) => {
      console.log("formulations", res);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} formulations entries retrieved from database!`,
            "success",
            true,
            true
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No formulation entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_FORMULATIONS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD FORMULATION
export const addFormulation = (formulation) => (dispatch, getState) => {
  axios
    .post(
      "api/v1/drugs/formulations/create",
      formulation,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res.data);
      dispatch(
        showSnackbarMessage("Formulation successfully added!", "success")
      );
      dispatch({
        type: actionTypes.ADD_FORMULATION,
        payload: res.data.formulation,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage("err.response.data.message", "error"));
    });
};

//EDIT FORMULATION
export const changeFormulation = (formulation, id) => (dispatch, getState) => {
  axios
    .put(
      `api/v1/drugs/formulations/${id}/update`,
      formulation,
      tokenConfig(getState)
    )
    .then((res) => {
      showSnackbarMessage("Formulation successfully updated!", "success");
      dispatch({
        type: actionTypes.EDIT_FORMULATION,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE FORMULATION
export const deleteFormulation = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/formulations/${id}/update`, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage("Formulation successfully deleted!", "success")
      );
      dispatch({
        type: actionTypes.DELETE_FORMULATION,
        payload: id,
      });
    })
    .catch((err) => {
      console.log(err);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
