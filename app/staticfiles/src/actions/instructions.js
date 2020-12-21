import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET INSTRUCTIONS
export const getInstructions = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/instructions", tokenConfig(getState))
    .then((res) => {
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} instructions entries retrieved from database!`,
            "success",
            true,
            true
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No instruction entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_INSTRUCTIONS,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD INSTRUCTION
export const addInstruction = (instruction) => (dispatch, getState) => {
  axios
    .post(
      "api/v1/drugs/instructions/create",
      instruction,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res.data);
      dispatch(
        showSnackbarMessage("Instruction successfully added!", "success")
      );
      dispatch({
        type: actionTypes.ADD_INSTRUCTION,
        payload: res.data.instruction,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage("err.response.data.message", "error"));
    });
};

//EDIT INSTRUCTION
export const changeInstruction = (instruction, id) => (dispatch, getState) => {
  axios
    .put(
      `api/v1/drugs/instructions/${id}/update`,
      instruction,
      tokenConfig(getState)
    )
    .then((res) => {
      showSnackbarMessage("Instruction successfully updated!", "success");
      dispatch({
        type: actionTypes.EDIT_INSTRUCTION,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE INSTRUCTION
export const deleteInstruction = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/instructions/${id}/update`, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage("Instruction successfully deleted!", "success")
      );
      dispatch({
        type: actionTypes.DELETE_INSTRUCTION,
        payload: id,
      });
    })
    .catch((err) => {
      console.log(err);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
