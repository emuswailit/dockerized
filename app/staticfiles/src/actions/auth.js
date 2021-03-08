import axios from "axios";

import * as actionTypes from "./actionTypes";
import { showSnackbarMessage } from "./snackbaractions";

// CHECK TOKEN & LOAD USER
export const loadUser = () => (dispatch, getState) => {

    if (tokenConfig(getState)==null) {
        dispatch({
            type: actionTypes.USER_LOADING_FAIL,
            payload:"Please login again"
           
        })
    }
  // User Loading

  dispatch({ type: actionTypes.USER_LOADING });

  axios
    .get("/api/v1/users/user", tokenConfig(getState))
    .then((res) => {
      console.log("User found: ", res.data);
      dispatch({
        type: actionTypes.USER_LOADED,
        payload: res.data,
      });
    })
    .catch((error) => {
     console.log("Ela",error.response && error.response.data.message ? error.response.data.message : error.message,)
      dispatch({
        type: actionTypes.USER_LOADING_FAIL,
        payload: error.response && error.response.data.message ? error.response.data.message : error.message,
      });
    });
};

// LOGIN USER
export const login = (email, password) => (dispatch) => {
  // Headers
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // Request Body
  const body = JSON.stringify({ email, password });
dispatch({
    type: actionTypes.LOGIN_REQUEST
})
  axios
    .post("/api/v1/users/signin/", body, config)
    .then((res) => {
      console.log("res", res);
      dispatch({
        type: actionTypes.LOGIN_SUCCESS,
        payload: res.data,
      });
    })

  
    .catch((error) => {
      dispatch({
          type: actionTypes.LOGIN_FAIL,
          payload:error.response && error.response.data.message ? error.response.data.message : error.message,
      })
    });
};

// LOGOUT USER
export const logout = () => (dispatch) => {
localStorage.removeItem('token')
  dispatch({
    type: actionTypes.LOGOUT_SUCCESS,
  });
};
// Setup config with token - helper function
export const tokenConfig = (getState) => {
  // Get token from local storage
  const token = localStorage.getItem("token");

  // Headers
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // If token, add to headers config
  if (token) {
    console.log("only token", token);
    config.headers["Authorization"] = `Bearer ${token}`;
  } else {
    return null
  }

  return config;
};
