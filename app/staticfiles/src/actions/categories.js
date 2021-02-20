import axios from "axios"
import * as actionTypes from "./actionTypes"
import {tokenConfig} from "./auth"
import {showSnackbarMessage} from "./snackbaractions"
//GET BODY SYSTEMS
export const getCategories = () => (dispatch, getState) => {
  axios
    .get("api/v1/utilities/categories", tokenConfig(getState))
    .then((res) => {
      if (res.data.results.length > 0) {
        dispatch(
          showSnackbarMessage(
            `${res.data.results.length} categories  retrieved from database!`,
            "success",
            true,
            true
          )
        )
      } else {
        dispatch(
          showSnackbarMessage("No category entries in the database!", "error")
        )
      }
      dispatch({
        type: actionTypes.GET_CATEGORIES,
        payload: res.data.results,
      })
    })
    .catch((err) => {
      console.log(err)
      // dispatch(showSnackbarMessage(err.response.data.message, "error"));
    })
}

//ADD CATEGORY
export const addCategory = (category) => (dispatch, getState) => {
  axios
    .post("api/v1/utilities/categories/create", category, tokenConfig(getState))
    .then((res) => {
      console.log("res", res.data)
      dispatch(showSnackbarMessage("Category successfully added!", "success"))
      dispatch({
        type: actionTypes.ADD_CATEGORY,
        payload: res.data.category,
      })
    })
    .catch((err) => {
      console.log("errr", err)
      dispatch(showSnackbarMessage("err.response.data.message", "error"))
    })
}

//EDIT CATEGORY
export const changeCategory = (category, id) => (dispatch, getState) => {
  axios
    .put(`api/v1/utilities/categories/${id}`, category, tokenConfig(getState))
    .then((res) => {
      showSnackbarMessage("Category successfully updated!", "success")
      dispatch({
        type: actionTypes.EDIT_CATEGORY,
      })
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"))
    })
}

//DELETE CATEGORY
export const deleteCategory = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/utilities/categories/${id}`, tokenConfig(getState))
    .then((res) => {
      console.log("Rsponse ", res)
      dispatch(showSnackbarMessage("Category successfully deleted!", "success"))
      dispatch({
        type: actionTypes.DELETE_CATEGORY,
        payload: id,
      })
    })
    .catch((err) => {
      console.log("Delete error", err)
      dispatch(showSnackbarMessage(err.response.data.message, "error"))
    })
}
