import axios from "axios";

import * as actionTypes from "./actionTypes";
import { showSnackbarMessage } from "./snackbaractions";

// CHECK TOKEN & LOAD USER
export const loadUser = () => (dispatch, getState) => {
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
    .catch((err) => {
      console.log("user error", err);
      // dispatch({
      //   type: actionTypes.AUTH_ERROR,
      // });
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

  axios
    .post("/api/v1/users/signin/", body, config)
    .then((res) => {
      console.log("res", res);
      dispatch({
        type: actionTypes.LOGIN_SUCCESS,
        payload: res.data,
      });
    })

    localStorage.setItem('userInfo', JSON.stringify(data))
    .catch((err) => {
      console.log("erorr", err);
    });
};

// LOGOUT USER
export const logout = () => (dispatch) => {
  
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
    console.log("There is no token");
  }

  return config;
};
