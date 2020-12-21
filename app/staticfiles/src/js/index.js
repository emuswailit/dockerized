import React, { Fragment } from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import {
  BrowserRouter as Router,
  Routes,
  Switch,
  Redirect,
  Route,
} from "react-router-dom";
import { Button } from "@material-ui/core";
import store from "../components/store";
import Header from "../components/common/Header";
import { loadUser } from "../actions/auth";
import GenericSnackBar from "../components/common/GenericSnackBar";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import blueGrey from "@material-ui/core/colors/blueGrey";
import lightGreen from "@material-ui/core/colors/lightGreen";
import PublicRoute from "./PublicRoute";
import PrivateRoute from "./PrivateRoute";
import Home from "../components/Home";
import Login from "../components/Login";
import Dashboard from "../components/Users/Dashboard";
import Dashy from "./Dashy";
import Users from "../components/Users/Users";
import Register from "../components/common/Register";
import BodySystems from "../components/Drugs/BodySystems";
import DrugClasses from "../components/Drugs/DrugClasses";
import Distributors from "../components/Drugs/Distributors";
import Posologies from "../components/Drugs/Posologies";
import Frequencies from "../components/Drugs/Frequencies";
import DrugSubClasses from "../components/Drugs/DrugSubClasses";
import Formulations from "../components/Drugs/Formulations";
import Generics from "../components/Drugs/Generics";
import Preparations from "../components/Drugs/Preparations";
import Manufacturers from "../components/Drugs/Manufacturers";
import Products from "../components/Drugs/Products";
import Instructions from "../components/Drugs/Instructions";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      themeType: "dark",
    };
  }

  changeTheme() {
    if (this.state.themeType == "dark") {
      this.setState({ themeType: "light" });
    } else {
      this.setState({ themeType: "dark" });
    }
  }
  componentDidMount() {
    store.dispatch(loadUser());
    console.log(this.props)
  }
  render() {
    let theme = createMuiTheme({
      palette: {
        primary: {
          light: lightGreen[300],
          main: lightGreen[500],
          dark: lightGreen[700],
        },
        secondary: {
          light: blueGrey[300],
          main: blueGrey[500],
          dark: blueGrey[700],
        },
        type: this.state.themeType,
      },
    });
    return (
      <Provider store={store}>
        <GenericSnackBar />
        <Router>
          <MuiThemeProvider theme={theme}>
            <Fragment>
         
        <Switch>
          <PublicRoute restricted={false} component={Home} path="/" exact />
          <PublicRoute restricted={false} component={Register} path="/register" exact />
          <PublicRoute restricted={true} component={Login} path="/login" exact />
          <PrivateRoute component={Dashy} path="/dashboard" exact  />
          <PrivateRoute component={Users} path="/users" exact  />
            <PrivateRoute exact path="/body_systems" component={BodySystems} />
            <PrivateRoute exact path="/drug_classes" component={DrugClasses} />
            <PrivateRoute exact path="/distributors" component={Distributors} />
            <PrivateRoute exact path="/posologies" component={Posologies} />
            <PrivateRoute exact path="/frequencies" component={Frequencies} />
            <PrivateRoute exact path="/instructions" component={Instructions} />
            <PrivateRoute exact path="/sub_classes" component={DrugSubClasses} />
            <PrivateRoute exact path="/formulations" component={Formulations} />
            <PrivateRoute exact path="/generics" component={Generics} />
            <PrivateRoute exact path="/preparations" component={Preparations} />
            <PrivateRoute exact path="/manufacturers" component={Manufacturers} />
            <PrivateRoute exact path="/products" component={Products} />
        </Switch>
     
              <Button
                title="Change Themes"
                variant="contained"
                color="secondary"
                onClick={() => {
                  this.changeTheme();
                }}
              >
                Change Theme
              </Button>
            </Fragment>
          </MuiThemeProvider>
        </Router>
      </Provider>
    );
  }
}
ReactDOM.render(<App />, document.getElementById("react-app"));
