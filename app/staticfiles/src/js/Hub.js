import React from "react"
import {Fragment} from "react"
import PublicRoute from "./PublicRoute"
import PrivateRoute from "./PrivateRoute"
import Home from "../components/Home"
import Login from "../components/Login"
import Dashy from "./Dashy"
import Users from "../components/Users/Users"
import Register from "../components/common/Register"
import DrugClasses from "../components/Drugs/DrugClasses"
import Distributors from "../components/Drugs/Distributors"
import Posologies from "../components/Drugs/Posologies"
import Frequencies from "../components/Drugs/Frequencies"
import DrugSubClasses from "../components/Drugs/DrugSubClasses"
import Formulations from "../components/Drugs/Formulations"
import Generics from "../components/Drugs/Generics"
import Preparations from "../components/Drugs/Preparations"
import Manufacturers from "../components/Drugs/Manufacturers"
import Products from "../components/Drugs/Products"
import Instructions from "../components/Drugs/Instructions"
import BodySystems from "../pages/Drugs/BodySystems/BodySystems/BodySystems"

export default function Hub() {
  return (
    <Fragment>
      <PublicRoute restricted={false} component={Home} path="/" exact />
      <PublicRoute
        restricted={false}
        component={Register}
        path="/register"
        exact
      />
      <PublicRoute restricted={true} component={Login} path="/login" exact />
      <PrivateRoute component={Dashy} path="/dashboard" exact />
      <PrivateRoute component={Users} path="/users" exact />
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

      {/* <Button
                title="Change Themes"
                variant="contained"
                color="secondary"
                onClick={() => {
                  this.changeTheme()
                }}
              >
                Change Theme
              </Button> */}
    </Fragment>
  )
}
