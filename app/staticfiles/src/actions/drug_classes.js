import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET DRUG CLASSES
export const getDrugClasses = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/drug-classes", tokenConfig(getState))
    .then((res) => {
      console.log("drug_classes", res);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} drug class entries retrieved from database!`,
            "success"
          )
        );
      } else {
        dispatch(
          showSnackbarMessage("No drug class entries in the database!", "error")
        );
      }
      dispatch({
        type: actionTypes.GET_DRUG_CLASSES,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD DRUG CLASS
export const addDrugClass = (drugclass) => (dispatch, getState) => {
  axios
    .post("api/v1/drugs/drug-classes/create", drugclass, tokenConfig(getState))
    .then((res) => {
      console.log("res", res);
      dispatch(
        showSnackbarMessage(
          "Drug class successfulyy added!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.ADD_DRUG_CLASS,
        payload: res.data.drug_class,
        submissionSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err);
      dispatch(showSnackbarMessage("An error occurred", "error"));
    });
};

//EDIT DRUG CLASS
export const changeDrugClass = (drugclass, id) => (dispatch, getState) => {
  axios
    .put(`api/v1/drugs/drug-classes/${id}`, drugclass, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage(
          "Drug class successfully updated!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.EDIT_DRUG_CLASS,
        payload: true,
        editUserSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE DRUG_CLASS
export const deleteDrugClass = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/drug-classes/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: actionTypes.DELETE_DRUG_CLASS,
        payload: id,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
