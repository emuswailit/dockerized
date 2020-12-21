import axios from "axios";
import * as actionTypes from "./actionTypes";
import { tokenConfig } from "./auth";
import { showSnackbarMessage } from "./snackbaractions";
//GET DISTRIBUTORS
export const getDistributors = (url) => (dispatch, getState) => {
  axios
    .get(url, tokenConfig(getState))
    .then((res) => {
      console.log("res data", res.data);
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} distributors entries retrieved from database!`,
            "success",
            true,
            true
          )
        );
      } else {
        dispatch(
          showSnackbarMessage(
            "No distributor entries in the database!",
            "error"
          )
        );
      }
      dispatch({
        type: actionTypes.GET_DISTRIBUTORS,
        payload: {
          distributors: res.data.results,
          count: res.data.count,
          previous: res.data.previous,
          next: res.data.next,
        },
      });
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//ADD DISTRIBUTOR
export const addDistributor = (distributor) => (dispatch, getState) => {
  axios
    .post(
      "api/v1/drugs/distributors/create",
      distributor,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res.data);
      dispatch(
        showSnackbarMessage("Distributor successfully added!", "success")
      );
      dispatch({
        type: actionTypes.ADD_DISTRIBUTOR,
        payload: res.data.distributor,
      });
    })
    .catch((err) => {
      console.log("erroe", err);
      dispatch(showSnackbarMessage("err.response.data.message", "error"));
    });
};

//EDIT DISTRIBUTOR
export const changeDistributor = (distributor, id) => (dispatch, getState) => {
  console.log("Begining distributor update");
  axios
    .put(
      `api/v1/drugs/distributors/${id}/update`,
      distributor,
      tokenConfig(getState)
    )
    .then((res) => {
      console.log("res", res);
      showSnackbarMessage("Distributor successfully updated!", "success");
      dispatch({
        type: actionTypes.EDIT_DISTRIBUTOR,
        payload: res.data,
      });
    })
    .catch((err) => {
      console.log("err", err);
      // dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};

//DELETE DISTRIBUTOR
export const deleteDistributor = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/drugs/distributors/${id}/update`, tokenConfig(getState))
    .then((res) => {
      dispatch(
        showSnackbarMessage("Distributor successfully deleted!", "success")
      );
      dispatch({
        type: actionTypes.DELETE_DISTRIBUTOR,
        payload: id,
      });
    })
    .catch((err) => {
      console.log(err.response.data);
      dispatch(showSnackbarMessage(err.response.data.message, "error"));
    });
};
