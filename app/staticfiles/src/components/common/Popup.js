import React from "react"
import {
  Dialog,
  DialogTitle,
  DialogContent,
  makeStyles,
  Typography,
  Grid,
} from "@material-ui/core"
import CloseIcon from "@material-ui/icons/Close"
import Controls from "../controls/Control"

const useStyles = makeStyles((theme) => ({
  dialogWrapper: {
    padding: theme.spacing(2),
    position: "absolute",
    top: theme.spacing(5),
  },
  dialogTitle: {
    paddingRight: "0px",
  },
}))

export default function Popup(props) {
  const {title, children, openPopup, setOpenPopup} = props
  const classes = useStyles()

  return (
    <Grid container>

      <Grid item xs ={12}>
      <Dialog
      open={openPopup}
      maxWidth="md"
      classes={{paper: classes.dialogWrapper}}
    >
      <DialogTitle className={classes.dialogTitle}>
        <div style={{display: "flex"}}>
          <Typography variant="h6" component="div" style={{flexGrow: 1}}>
            {title}
          </Typography>
          <Controls.ActionButton
            color="secondary"
            onClick={() => {
              setOpenPopup(false)
            }}
          >
            <CloseIcon />
          </Controls.ActionButton>
        </div>
      </DialogTitle>
      <DialogContent dividers>{children}</DialogContent>
    </Dialog>
      </Grid>
    </Grid>
    
  )
}
