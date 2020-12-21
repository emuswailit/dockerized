import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET DRUG SUB CLASSES
export const getDrugSubClasses = () => (dispatch, getState) => {
  axios
    .get("api/v1/drugs/drug-sub-classes", tokenConfig(getState))
    .then((res) => {
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} drug sub class entries retrieved from database!`,
            "success"
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No drug sub class entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_DRUG_SUB_CLASSES,
        payload: res.data.results,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD DRUG CLASS
export const addDrugSubClass = (drugsubclass) => (dispatch, getState) => {
  axios
    .post(
      "api/v1/drugs/drug-sub-classes/create",
      drugsubclass,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res);
      dispatch(
        showSnackbarMessage(
          "Drug sub class successfully added!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.ADD_DRUG_SUB_CLASS,
        payload: res.data.drug_sub_class,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.detail, "error"));
    });
};

//EDIT DRUG CLASS
export const changeDrugSubClass = (drugsubclass, id) => (
  dispatch,
  getState
) => {
  axios
    .put(
      `api/v1/drugs/drug-sub-classes/${id}/update`,
      drugsubclass,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch(
        showSnackbarMessage(
          "Drug sub class successfully updated!",
          "success",
          true,
          true
        )
      );
      dispatch({
        type: actionTypes.EDIT_DRUG_SUB_CLASS,
        payload: true,
        editUserSuccessful: true,
      });
    })
    .catch((err) => {
      console.log("err", err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE DRUG_SUB_CLASS
export const deleteDrugSubClass = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/drug-sub-classes/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: actionTypes.DELETE_DRUG_SUB_CLASS,
        payload: id,
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
