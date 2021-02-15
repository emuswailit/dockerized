import React, {Fragment} from "react"
import {Route, Redirect} from "react-router-dom"
import {connect} from "react-redux"
import Navigation from "../components/common/Navigation"

const PrivateRoute = ({component: Component, auth, ...rest}) => (
  <Route
    {...rest}
    render={(props) => {
      console.log("auth", auth)
      if (auth.isLoading) {
        return <h2>Loading...</h2>
      } else if (!auth.isAuthenticated) {
        console.log("user not authenticated!")
        return <Redirect to="/login" />
      } else {
        console.log("Logged in..")
        console.log("props..", props)
        return (
          <Fragment>
            <Navigation user={auth.user} />
            <Component {...props} />
          </Fragment>
        )
      }
    }}
  />
)

const mapStateToProps = (state) => ({
  auth: state.auth,
})

export default connect(mapStateToProps)(PrivateRoute)
