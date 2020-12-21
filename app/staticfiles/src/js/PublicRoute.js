
import React from "react";
import { Route, Redirect } from "react-router-dom";
import { connect } from "react-redux";

const PrivateRoute = ({ component: Component, auth, ...rest }) => (
  <Route
    {...rest}
    render={(props) => {
      if (!auth.isAuthenticated) {
      
        console.log("Logged in..");
        return <Component {...props} />;
      } else {
        console.log("user not authenticated!");
        return <Redirect to="/dashboard" />;

      }
    }}
  />
);

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps)(PrivateRoute);
