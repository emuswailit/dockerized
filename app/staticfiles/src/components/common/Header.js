import React, { useEffect, Fragment } from "react";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import { loadUser } from "../../actions/auth";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import Users from "../Users/Users";
import Login from "../../components/Login";
import Register from "./Register";
import { Switch, Route } from "react-router-dom";
import Dashboard from "../Users/Dashboard";
import BodySystems from "../Drugs/BodySystems";
import DrugClasses from "../Drugs/DrugClasses";
import Distributors from "../Drugs/Distributors";
import Posologies from "../Drugs/Posologies";
import Frequencies from "../Drugs/Frequencies";
import Instructions from "../Drugs/Instructions";
import DrugSubClasses from "../Drugs/DrugSubClasses";
import Formulations from "../Drugs/Formulations";
import Generics from "../Drugs/Generics";
import Products from "../Drugs/Products";
import Preparations from "../Drugs/Preparations";
import Manufacturers from "../Drugs/Manufacturers";
import Home from "../Home";
import { Grid } from "@material-ui/core";
import Pricing from "./Pricing";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },

  paper: {
    padding: theme.spacing(2),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
}));

const Header = (props) => {
  const classes = useStyles();

  // useEffect(() => {
  //   props.loadUser();
  // }, []);
  const { user, isAuthenticated } = props.auth;

  let toDiaplay = null;
  {
    if (isAuthenticated) {
      toDiaplay = (
        <Fragment>
          <Dashboard user={props.auth.user} />

          <Switch>
          
            <Route exact path="/users" component={Users} />
            <Route exact path="/body_systems" component={BodySystems} />
            <Route exact path="/drug_classes" component={DrugClasses} />
            <Route exact path="/distributors" component={Distributors} />
            <Route exact path="/posologies" component={Posologies} />
            <Route exact path="/frequencies" component={Frequencies} />
            <Route exact path="/instructions" component={Instructions} />
            <Route exact path="/sub_classes" component={DrugSubClasses} />
            <Route exact path="/formulations" component={Formulations} />
            <Route exact path="/generics" component={Generics} />
            <Route exact path="/preparations" component={Preparations} />
            <Route exact path="/manufacturers" component={Manufacturers} />
            <Route exact path="/products" component={Products} />
            <Route exact path="/" component={Home} />
          </Switch>
        </Fragment>
      );
    } else {
      <Switch>
          
            <Route exact path="/register" component={Register} />
            <Route exact path="/pricing" component={Pricing} />
            <Route exact path="/login" component={Login} />
          </Switch>
      toDiaplay = <Login />;
    }
  }

  return (
    <div className={classes.root}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          {toDiaplay}
        </Grid>
      </Grid>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    auth: state.auth,
  };
};
export default connect(mapStateToProps, { loadUser })(Header);
