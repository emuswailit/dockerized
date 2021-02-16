import React from "react"
import ReactDOM from "react-dom"
import {Provider} from "react-redux"
import {
  BrowserRouter as Router,
  Routes,
  Switch,
  Redirect,
  Route,
} from "react-router-dom"

import store from "../components/store"
import {loadUser} from "../actions/auth"
import GenericSnackBar from "../components/common/GenericSnackBar"
import {MuiThemeProvider, createMuiTheme} from "@material-ui/core/styles"
import blueGrey from "@material-ui/core/colors/blueGrey"
import lightGreen from "@material-ui/core/colors/lightGreen"
import Hub from "./Hub"

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      themeType: "light",
    }
  }

  changeTheme() {
    if (this.state.themeType == "dark") {
      this.setState({themeType: "light"})
    } else {
      this.setState({themeType: "dark"})
    }
  }
  componentDidMount() {
    store.dispatch(loadUser())
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
        background: {
          default: "#f4f5fd",
        },
        type: this.state.themeType,
      },
    })
    return (
      <Provider store={store}>
        <GenericSnackBar />
        <Router>
          <MuiThemeProvider theme={theme}>
            <Switch>
              <Hub />
            </Switch>
          </MuiThemeProvider>
        </Router>
      </Provider>
    )
  }
}
ReactDOM.render(<App />, document.getElementById("react-app"))
