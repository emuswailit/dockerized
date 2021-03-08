import React, { useState, useEffect, Fragment } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Paper from "@material-ui/core/Paper";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { login } from "../actions/auth";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import { Form, useForm } from "./common/useForm";
import Controls from "./controls/Control";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="https://material-ui.com/">
        Mobipharma
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100vh",
  },
  image: {
    backgroundImage: "url(https://source.unsplash.com/random)",
    backgroundRepeat: "no-repeat",
    backgroundColor:
      theme.palette.type === "light"
        ? theme.palette.grey[50]
        : theme.palette.grey[900],
    backgroundSize: "cover",
    backgroundPosition: "center",
  },
  paper: {
    margin: theme.spacing(8, 4),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));
const initialFValues = {

  email: "",
  password: "",

}


const SignInSide = (props) => {
    console.log(props);
  const classes = useStyles();

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();


  const loginUser = () => {
    props.login(email, password);
  };


  const registerUser = () => {
    console.log("To registration");
  props.history.push("/register")
  };

  useEffect(() => {
    if (props.auth.isAuthenticated) {
      <Redirect to="/" />;
    }
  }, []);

  const validate = (fieldValues = values) => {
    let temp = {...errors}
    if ("password" in fieldValues)
      temp.password = fieldValues.password ? "" : "Password is required"
    if ('email' in fieldValues)
      temp.email = (/$^|.+@.+..+/).test(fieldValues.email) ? "" : "Email is not valid."
      setErrors({
        ...temp,
      })
  
      if (fieldValues == values) return Object.values(temp).every((x) => x == "")
  }

  const {
    values,
    setValues,
    handleInputChange,
    errors,
    setErrors,
    resetForm,
  } = useForm(initialFValues, true, validate)


  const handleSubmit = (e) => {
    e.preventDefault()
    console.log("Not validated")
    if (validate())
    props.login(values.email, values.password)
  }
  return (
    <Fragment>
     
      {props.auth.isAuthenticated ? (
        <Redirect to="/" />
      ) : (
        <Grid container component="main" className={classes.root}>
          <CssBaseline />
          <Grid item xs={false} sm={4} md={7} className={classes.image} />
          <Grid
            item
            xs={12}
            sm={8}
            md={5}
            component={Paper}
            elevation={6}
            square
          >
            <div className={classes.paper}>
              <Avatar className={classes.avatar}>
                <LockOutlinedIcon />
              </Avatar>
              <Typography component="h1" variant="h5">
                Sign in
              </Typography>
              <Form onSubmit={handleSubmit}>
      <Grid container>
        <Grid item xs={12}>
        <Controls.Input
            variant="outlined"
            label="Email"
            name="email"
            value={values.email}
            onChange={handleInputChange}
            error={errors.email}
          />
                <Controls.Input
            variant="outlined"
            label="Password"
            name="password"
            type="password"
            value={values.password}
            onChange={handleInputChange}
            error={errors.password}
          />
         
            <Controls.Button width='80%' type="submit" text="Submit" />
            {props.auth.error && <h3 variant='primary'>{props.auth.error}</h3>}
      
          </Grid>
          </Grid>
          </Form>
            </div>
          </Grid>
        </Grid>
      )}
    </Fragment>
  );
};

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps, { login })(SignInSide);
