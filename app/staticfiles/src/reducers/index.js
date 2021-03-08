import {combineReducers} from "redux"
import auth from "./auth"
import users from "./users"
import utility from "./utility"
import messages from "./messages"
import bodysystems from "./bodysystems"
import drugclasses from "./drugclasses"
import snackbarreducer from "./snackbarreducer"
import distributors from "./distributors"
import posologies from "./posologies"
import frequencies from "./frequencies"
import instructions from "./instructions"
import drugsubclasses from "./drugsubclasses"
import formulations from "./formulations"
import generics from "./generics"
import preparations from "./preparations"
import manufacturers from "./manufacturers"
import products from "./products"
import categories from "./categories"
export default combineReducers({
  auth,
  users,
  utility,
  messages,
  bodysystems,
  drugclasses,
  snackbarreducer,
  distributors,
  posologies,
  frequencies,
  instructions,
  drugsubclasses,
  formulations,
  generics,
  preparations,
  manufacturers,
  products,
  categories,
})
