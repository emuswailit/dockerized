import axios from "axios"
import * as actionTypes from "./actionTypes"
import {createMessage, returnErrors, clearErrors} from "./messages"
import {tokenConfig} from "./auth"
import {startLoading, endLoadingSuccess, endLoadingFailure} from "./utility"
import {showSnackbarMessage} from "./snackbaractions"

//GET USERS
export const getUsers = () => (dispatch, getState) => {
  dispatch(showSnackbarMessage("God is great", "error", true))
  axios
    .get("api/v1/users/users/", tokenConfig(getState))
    .then((res) => {
      console.log("res", res)
      dispatch(
        showSnackbarMessage("Users succesfully retrieved!", "success", true)
      )
      dispatch({
        type: actionTypes.GET_USERS,
        payload: res.data.results,
      })
      // dispatch(createMessage("Users succesfully retrieved", "success"));
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"))
    })
}

//ADD USER
export const addUser = (user) => (dispatch, getState) => {
  axios
    .post("api/v1/users/register/", user, tokenConfig(getState))
    .then((res) => {
      // dispatch(showSnackbarMessage("User successfully added!", "success", true))
      
        dispatch({
          type: actionTypes.ADD_USER,
          user: res.data.user,
          response_code: res.data.response_code,
          response_message: res.data.response_message,
          errors: res.data.errors,
        })
      
      
    })
    .catch((err) => {
      console.log("From err", err)
    })
}

//EDIT USER
export const changeUser = (user, id) => (dispatch, getState) => {
  axios
    .put(`api/v1/users/users/${id}/update`, user, tokenConfig(getState))
    .then((res) => {

      console.log("Update res", res)
  
      dispatch({
        type: actionTypes.EDIT_USER,
     
      })
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"))
    })
}

//DELETE USER
export const deleteUser = (id) => (dispatch, getState) => {
  axios
    .delete(`api/v1/users/users/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch(showSnackbarMessage("User succesfully deleted", "success"))
      console.log("deleted", res)
      dispatch({
        type: actionTypes.DELETE_USER,
        payload: id,
      })
    })
    .catch((err) => {
      dispatch(showSnackbarMessage(err.response.data.message, "error"))
    })
}
