import React from "react";
import { useDispatch, useSelector } from "react-redux";
import Snackbar from "@material-ui/core/Snackbar";
import IconButton from "@material-ui/core/IconButton";
import { Icon } from "@material-ui/core";
import { clearSnackbar } from "../../actions/snackbaractions";
import Alert from "@material-ui/lab/Alert";

export default function GenericSnackBar() {
  const dispatch = useDispatch();

  const { severity, successSnackbarMessage, successSnackbarOpen } = useSelector(
    (state) => state.snackbarreducer
  );

  function handleClose() {
    dispatch(clearSnackbar());
  }

  return (
    <Snackbar
      anchorOrigin={{
        vertical: "bottom",
        horizontal: "left",
      }}
      open={successSnackbarOpen}
      autoHideDuration={4000}
      onClose={handleClose}
      aria-describedby="client-snackbar"
    >
      <Alert severity={severity}>{successSnackbarMessage}</Alert>
    </Snackbar>
  );
}
