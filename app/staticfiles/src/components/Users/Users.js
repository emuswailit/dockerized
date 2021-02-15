import React, {useState, useEffect, Fragment} from "react"
import PropTypes from "prop-types"
import clsx from "clsx"
import {lighten, makeStyles} from "@material-ui/core/styles"
import Table from "@material-ui/core/Table"
import TableBody from "@material-ui/core/TableBody"
import TableCell from "@material-ui/core/TableCell"
import TableContainer from "@material-ui/core/TableContainer"
import TableHead from "@material-ui/core/TableHead"
import TablePagination from "@material-ui/core/TablePagination"
import TableRow from "@material-ui/core/TableRow"
import Toolbar from "@material-ui/core/Toolbar"
import Checkbox from "@material-ui/core/Checkbox"
import IconButton from "@material-ui/core/IconButton"
import Tooltip from "@material-ui/core/Tooltip"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import Switch from "@material-ui/core/Switch"
import DeleteIcon from "@material-ui/icons/Delete"
import FilterListIcon from "@material-ui/icons/FilterList"
import TableSortLabel from "@material-ui/core/TableSortLabel"
import Paper from "@material-ui/core/Paper"
import TextField from "@material-ui/core/TextField"
import InputAdornment from "@material-ui/core/InputAdornment"
import SearchIcon from "@material-ui/icons/Search"
import TableFooter from "@material-ui/core/TableFooter"
import Button from "@material-ui/core/Button"
import FirstPageIcon from "@material-ui/icons/FirstPage"
import KeyboardArrowLeft from "@material-ui/icons/KeyboardArrowLeft"
import KeyboardArrowRight from "@material-ui/icons/KeyboardArrowRight"
import LastPageIcon from "@material-ui/icons/LastPage"
import {getUsers, addUser, deleteUser, changeUser} from "../../actions/users"
import {connect} from "react-redux"
import Grid from "@material-ui/core/Grid"
import Dialog from "@material-ui/core/Dialog"
import DialogActions from "@material-ui/core/DialogActions"
import DialogContent from "@material-ui/core/DialogContent"
import DialogContentText from "@material-ui/core/DialogContentText"
import DialogTitle from "@material-ui/core/DialogTitle"
import FormControl from "@material-ui/core/FormControl"
import Select from "@material-ui/core/Select"
import InputLabel from "@material-ui/core/InputLabel"
import {Formik, Form, Field, ErrorMessage} from "formik"
import * as Yup from "yup"
import "date-fns"
import {format} from "date-fns"
import DateFnsUtils from "@date-io/date-fns"
import Snackbar from "@material-ui/core/Snackbar"

import EditIcon from "@material-ui/icons/Edit"
import Card from "@material-ui/core/Card"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import Typography from "@material-ui/core/Typography"
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
  KeyboardDatePicker,
} from "@material-ui/pickers"
import MuiAlert from "@material-ui/lab/Alert"
function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />
}

// const rows = [
//   createData("Cupcake", 305, 3.7, 67, 4.3),
//   createData("Donut", 452, 25.0, 51, 4.9),
//   createData("Eclair", 262, 16.0, 24, 6.0),
//   createData("Frozen yoghurt", 159, 6.0, 24, 4.0),
//   createData("Gingerbread", 356, 16.0, 49, 3.9),
//   createData("Honeycomb", 408, 3.2, 87, 6.5),
//   createData("Ice cream sandwich", 237, 9.0, 37, 4.3),
//   createData("Jelly Bean", 375, 0.0, 94, 0.0),
//   createData("KitKat", 518, 26.0, 65, 7.0),
//   createData("Lollipop", 392, 0.2, 98, 0.0),
//   createData("Marshmallow", 318, 0, 81, 2.0),
//   createData("Nougat", 360, 19.0, 9, 37.0),
//   createData("Oreo", 437, 18.0, 63, 4.0),
// ];

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1
  }
  if (b[orderBy] > a[orderBy]) {
    return 1
  }
  return 0
}

function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy)
}

function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index])
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0])
    if (order !== 0) return order
    return a[1] - b[1]
  })
  return stabilizedThis.map((el) => el[0])
}

const headCells = [
  {
    id: "first_name",
    numeric: false,
    disablePadding: true,
    label: "First Name",
  },
  {
    id: "last_name",
    numeric: false,
    disablePadding: false,
    label: "Last Name",
  },
  {id: "email", numeric: false, disablePadding: false, label: "Email"},
  {id: "phone", numeric: false, disablePadding: false, label: "Phone"},
  {id: "gender", numeric: false, disablePadding: false, label: "Gender"},
  {id: "actions", numeric: false, disablePadding: false, label: "Actions"},
]

function EnhancedTableHead(props) {
  const {
    classes,
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
  } = props
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property)
  }

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{"aria-label": "select all desserts"}}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? "right" : "left"}
            padding={headCell.disablePadding ? "none" : "default"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <span className={classes.visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </span>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  )
}

EnhancedTableHead.propTypes = {
  classes: PropTypes.object.isRequired,
  numSelected: PropTypes.number.isRequired,
  onRequestSort: PropTypes.func.isRequired,
  onSelectAllClick: PropTypes.func.isRequired,
  order: PropTypes.oneOf(["asc", "desc"]).isRequired,
  orderBy: PropTypes.string.isRequired,
  rowCount: PropTypes.number.isRequired,
}

const useToolbarStyles = makeStyles((theme) => ({
  root: {
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(1),
  },
  highlight:
    theme.palette.type === "light"
      ? {
          color: theme.palette.secondary.main,
          backgroundColor: lighten(theme.palette.secondary.light, 0.85),
        }
      : {
          color: theme.palette.text.primary,
          backgroundColor: theme.palette.secondary.dark,
        },
  title: {
    flex: "1 1 100%",
  },
}))

const EnhancedTableToolbar = (props) => {
  const classes = useToolbarStyles()
  const {numSelected} = props

  return (
    <Toolbar
      variant="dense"
      className={clsx(classes.root, {
        [classes.highlight]: numSelected > 0,
      })}
    >
      {numSelected > 0 ? (
        <Typography
          className={classes.title}
          color="inherit"
          variant="subtitle1"
          component="div"
        >
          {numSelected} selected
        </Typography>
      ) : (
        <Typography
          className={classes.title}
          variant="subtitle1"
          id="tableTitle"
          component="div"
        >
          Active Users
        </Typography>
      )}
      {/* 
      {numSelected > 0 ? (
        <Tooltip title="Delete">
          <IconButton aria-label="delete">
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      ) : (
        <Tooltip title="Filter list">
          <IconButton aria-label="filter list">
            <FilterListIcon />
          </IconButton>
        </Tooltip>
      )} */}
    </Toolbar>
  )
}

EnhancedTableToolbar.propTypes = {
  numSelected: PropTypes.number.isRequired,
}

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
  },
  paper: {
    width: "100%",
    marginBottom: theme.spacing(2),
  },
  table: {
    minWidth: 750,
  },
  visuallyHidden: {
    border: 0,
    clip: "rect(0 0 0 0)",
    height: 1,
    margin: -1,
    overflow: "hidden",
    padding: 0,
    position: "absolute",
    top: 20,
    width: 1,
  },
  paper: {
    margin: theme.spacing(2),
    padding: theme.spacing(2),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },

  formControl: {
    margin: theme.spacing(1),
    minWidth: 200,
  },
}))

const Users = (props) => {
  const classes = useStyles()
  const [search, setSearch] = useState("")
  const [rows, setRows] = React.useState([])
  const [order, setOrder] = React.useState("asc")
  const [orderBy, setOrderBy] = React.useState("last_name")
  const [selected, setSelected] = React.useState([])
  const [selectedUser, setSelectedUser] = useState({})
  const [editingUser, setEditingUser] = useState(false)

  const [page, setPage] = React.useState(0)
  const [dense, setDense] = React.useState(false)
  const [rowsPerPage, setRowsPerPage] = React.useState(5)
  const [isSubmitionCompleted, setSubmitionCompleted] = useState(false)

  //Snack bar state
  const [message, setMessage] = useState(props.message.message)
  const [openSnackBar, setOpenSnackBar] = useState(true)
  const [openErrorSnackBar, setOpenErrorSnackBar] = useState(false)

  //Create new user state
  const [creatingUser, setCreatingUser] = useState(false)
  const [selectedDate, setSelectedDate] = React.useState(new Date())

  useEffect(() => {
    props.getUsers()
  }, [])

  useEffect(() => {
    setMessage(props.message.message)
    setOpenSnackBar(true)
  }, [props.message.message])

  //Check for successful requests
  useEffect(() => {
    //Close edit user modal
    setEditingUser(false)
    //Close create user modal
    setCreatingUser(false)
    setSubmitionCompleted(true)
  }, [props.snackbarreducer.success])

  useEffect(() => {
    setRows(props.users)
  }, [props.users])

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === "asc"
    setOrder(isAsc ? "desc" : "asc")
    setOrderBy(property)
  }

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelecteds = rows.map((n) => n.id)
      setSelected(newSelecteds)
      return
    }
    setSelected([])
  }

  const handleClick = (event, id) => {
    const selectedIndex = selected.indexOf(id)
    let newSelected = []

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id)
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1))
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1))
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      )
    }

    setSelected(newSelected)
  }

  const handleChangePage = (event, newPage) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  const handleChangeDense = (event) => {
    setDense(event.target.checked)
  }

  const isSelected = (id) => selected.indexOf(id) !== -1

  const emptyRows =
    rowsPerPage - Math.min(rowsPerPage, rows.length - page * rowsPerPage)

  const onSearchChange = (e) => {
    setSearch(e.target.value)
  }

  const handleCreateNewUser = () => {
    setSubmitionCompleted(false)
    setCreatingUser(true)
  }

  //Edit user

  const handleDeleteUser = (user_id) => {
    console.log(user_id)
    props.deleteUser(user_id)
  }

  //Delete user

  const handleEditUser = (user) => {
    console.log("Edit User", user)
    setEditingUser(!editingUser)
    setSelectedUser(user)

    // props.deleteUser(user_id);
  }

  //Close modals
  const handleClose = () => {
    setCreatingUser(false)
  }

  //Close SnackBars
  const handleSnackClose = (event, reason) => {
    if (reason === "clickaway") {
      return
    }

    setOpenSnackBar(false)
    setOpenErrorSnackBar(false)
  }

  //Handle date change
  const handleDateChange = (setFieldValue, date) => {
    // setSelectedDate(moment(date, "yyyy-MM-dd").format());
    setFieldValue("date_of_birth", format(date, "yyyy-MM-dd"))
  }

  //Cancel editing user
  const handleCancelEdit = () => {
    setEditingUser(false)
  }

  return (
    <div className={classes.root}>
      <Paper className={classes.paper}>
        {/* <EnhancedTableToolbar numSelected={selected.length} /> */}
        <TableContainer>
          <Paper className={classes.root}>
            <Table dense table size="small">
              <TableBody>
                <TableRow>
                  <TableCell align="left">
                    <TextField
                      color="primary"
                      placeholder="Search"
                      value={search}
                      onChange={onSearchChange}
                      className={classes.search}
                      id="input-search"
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <SearchIcon />
                          </InputAdornment>
                        ),
                      }}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={handleCreateNewUser}
                    >
                      + Add new
                    </Button>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </Paper>

          {/* Dialogs ho here */}

          {/* 2. Edit user dialog */}

          <Fragment>
            {/* //Alert for messages */}
            {props.message.message == null ? null : (
              <Snackbar
                open={openSnackBar}
                autoHideDuration={3000}
                onClose={handleSnackClose}
              >
                <Alert
                  onClose={handleSnackClose}
                  severity={props.message.severity}
                >
                  {message}
                </Alert>
              </Snackbar>
            )}
            {/* Creating user */}
            <Dialog
              open={creatingUser}
              onClose={handleClose}
              aria-labelledby="form-dialog-title"
            >
              {creatingUser && (
                <Fragment>
                  <DialogTitle id="form-dialog-title">Edit User</DialogTitle>
                  <DialogContent>
                    <DialogContentText>Unda user</DialogContentText>
                    <Formik
                      initialValues={{
                        email: "",
                        first_name: "",
                        middle_name: "",
                        last_name: "",
                        national_id: "",
                        phone: "",
                        date_of_birth: null,
                        gender: "",
                        password: "",
                        confirm_password: "",
                      }}
                      onSubmit={(values, {setSubmitting}) => {
                        props.addUser(values)

                        setOpenErrorSnackBar(true)

                        console.log(values)
                      }}
                      validationSchema={Yup.object().shape({
                        first_name: Yup.string().required(
                          "First name is required"
                        ),
                        last_name: Yup.string().required(
                          "Last name is required"
                        ),
                        phone: Yup.string().required(
                          "Phone number is required"
                        ),
                        email: Yup.string()
                          .email()
                          .required("Email address is required"),
                        national_id: Yup.string().required(
                          "Phone number is required"
                        ),
                        password: Yup.string().required("Password is required"),
                        confirm_password: Yup.string().oneOf(
                          [Yup.ref("password"), null],
                          "Passwords must match"
                        ),
                      })}
                    >
                      {(props) => {
                        const {
                          values,
                          setFieldValue,
                          touched,
                          errors,
                          dirty,
                          isSubmitting,
                          handleChange,
                          handleBlur,
                          handleSubmit,
                          handleReset,
                        } = props
                        return (
                          <form onSubmit={handleSubmit}>
                            <div>
                              <Grid container>
                                <Grid item xs={6}>
                                  <TextField
                                    fullWidth
                                    margin="normal"
                                    variant="outlined"
                                    error={
                                      errors.first_name && touched.first_name
                                    }
                                    label="First Name:"
                                    name="first_name"
                                    type="text"
                                    value={values.first_name}
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    helperText={
                                      errors.first_name &&
                                      touched.first_name &&
                                      errors.first_name
                                    }
                                    autoFocus
                                  />
                                </Grid>
                                <Grid item xs={6}></Grid>
                              </Grid>

                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.last_name && touched.last_name}
                                label="Middle Name:"
                                name="middle_name"
                                type="text"
                                value={values.middle_name}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.middle_name &&
                                  touched.middle_name &&
                                  errors.middle_name
                                }
                              />
                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.last_name && touched.last_name}
                                label="Last Name:"
                                name="last_name"
                                type="text"
                                value={values.last_name}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.last_name &&
                                  touched.last_name &&
                                  errors.last_name
                                }
                              />

                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.email && touched.email}
                                label="Email:"
                                name="email"
                                type="email"
                                value={values.email}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.email && touched.email && errors.email
                                }
                              />

                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.phone && touched.phone}
                                label="Phone:"
                                name="phone"
                                type="text"
                                value={values.phone}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.phone && touched.phone && errors.phone
                                }
                              />
                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={
                                  errors.national_id && touched.national_id
                                }
                                label="National ID:"
                                name="national_id"
                                type="text"
                                value={values.national_id}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.national_id &&
                                  touched.national_id &&
                                  errors.national_id
                                }
                              />
                              <Grid container justify="space-around">
                                <Grid item>
                                  <FormControl
                                    variant="outlined"
                                    className={classes.formControl}
                                  >
                                    <InputLabel htmlFor="outlined-gender-native-simple">
                                      Gender
                                    </InputLabel>
                                    <Select
                                      error={errors.gender && touched.gender}
                                      helperText={
                                        errors.gender &&
                                        touched.gender &&
                                        errors.gender
                                      }
                                      margin="normal"
                                      onBlur={handleBlur}
                                      native
                                      onChange={handleChange}
                                      label="Gender"
                                      inputProps={{
                                        name: "gender",
                                        id: "outlined-gender-native-simple",
                                      }}
                                    >
                                      <option aria-label="None" value="" />
                                      <option value="Female">Female</option>
                                      <option value="Male">Male</option>
                                    </Select>
                                  </FormControl>
                                </Grid>

                                <Grid item>
                                  <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                    <Grid container justify="space-around">
                                      <KeyboardDatePicker
                                        margin="normal"
                                        id="date-picker-dialog"
                                        label="Select date of birth"
                                        format="yyyy-MM-dd"
                                        value={selectedDate}
                                        onChange={(date) =>
                                          handleDateChange(setFieldValue, date)
                                        }
                                        KeyboardButtonProps={{
                                          "aria-label": "change date",
                                        }}
                                      />
                                    </Grid>
                                  </MuiPickersUtilsProvider>
                                </Grid>
                              </Grid>

                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.password && touched.password}
                                label="Password:"
                                name="password"
                                type="text"
                                value={values.password}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.password &&
                                  touched.password &&
                                  errors.password
                                }
                              />
                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={
                                  errors.confirm_password &&
                                  touched.confirm_password
                                }
                                label="Confirm Password:"
                                name="confirm_password"
                                type="text"
                                value={values.confirm_password}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.confirm_password &&
                                  touched.confirm_password &&
                                  errors.confirm_password
                                }
                              />

                              <DialogActions>
                                <Button
                                  color="secondary"
                                  type="button"
                                  className="outline"
                                  onClick={handleCancelEdit}
                                >
                                  Close
                                </Button>
                                <Button
                                  type="submit"
                                  disabled={isSubmitionCompleted}
                                  color="primary"
                                >
                                  Submit
                                </Button>
                                {/* <DisplayFormikState {...props} /> */}
                              </DialogActions>
                            </div>
                          </form>
                        )
                      }}
                    </Formik>
                  </DialogContent>
                </Fragment>
              )}

              {editingUser && props.error.theresError && (
                <Snackbar
                  open={openErrorSnackBar}
                  onClose={handleSnackClose}
                  autoHideDuration={6000}
                >
                  <Alert onClose={handleSnackClose} severity="error">
                    {props.error.msg.phone}
                  </Alert>
                </Snackbar>
              )}
            </Dialog>

            {/* Editing user */}
            <Dialog
              open={editingUser}
              onClose={handleClose}
              aria-labelledby="form-dialog-title"
            >
              {editingUser && (
                <Fragment>
                  <DialogTitle id="form-dialog-title">Edit User</DialogTitle>
                  <DialogContent>
                    <DialogContentText>Edit user</DialogContentText>
                    <Formik
                      initialValues={{
                        first_name: selectedUser.first_name,
                        last_name: selectedUser.last_name,
                      }}
                      onSubmit={(values, {setSubmitting}) => {
                        // setSubmitting(props.submissionSuccessful);

                        // props.addUser(values);
                        // setSubmitionCompleted(props.submissionSuccessful);
                        setOpenErrorSnackBar(true)

                        console.log(values)
                        props.changeUser(values, selectedUser.id)
                      }}
                      validationSchema={Yup.object().shape({
                        first_name: Yup.string().required(
                          "First name is required"
                        ),
                        last_name: Yup.string().required(
                          "Last name is required"
                        ),
                      })}
                    >
                      {(props) => {
                        const {
                          values,
                          setFieldValue,
                          touched,
                          errors,
                          dirty,
                          isSubmitting,
                          handleChange,
                          handleBlur,
                          handleSubmit,
                          handleReset,
                        } = props
                        return (
                          <form onSubmit={handleSubmit}>
                            <div>
                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.first_name && touched.first_name}
                                label="First Name:"
                                name="first_name"
                                type="text"
                                value={values.first_name}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.first_name &&
                                  touched.first_name &&
                                  errors.first_name
                                }
                                autoFocus
                              />
                              <TextField
                                fullWidth
                                margin="normal"
                                variant="outlined"
                                error={errors.last_name && touched.last_name}
                                label="Last Name:"
                                name="last_name"
                                type="text"
                                multiline
                                rows="2"
                                value={values.last_name}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                helperText={
                                  errors.last_name &&
                                  touched.last_name &&
                                  errors.last_name
                                }
                              />

                              <DialogActions>
                                <Button
                                  color="secondary"
                                  type="button"
                                  className="outline"
                                  onClick={handleCancelEdit}
                                >
                                  Close
                                </Button>
                                <Button
                                  type="submit"
                                  disabled={isSubmitionCompleted}
                                  color="primary"
                                >
                                  Submit
                                </Button>
                                {/* <DisplayFormikState {...props} /> */}
                              </DialogActions>
                            </div>
                          </form>
                        )
                      }}
                    </Formik>
                  </DialogContent>
                </Fragment>
              )}

              {editingUser && props.error.theresError && (
                <Snackbar
                  open={openErrorSnackBar}
                  onClose={handleSnackClose}
                  autoHideDuration={6000}
                >
                  <Alert onClose={handleSnackClose} severity="error">
                    {props.error.msg.phone}
                  </Alert>
                </Snackbar>
              )}
            </Dialog>
          </Fragment>

          <Table
            className={classes.table}
            aria-labelledby="tableTitle"
            size={dense ? "small" : "medium"}
            aria-label="enhanced table"
          >
            <EnhancedTableHead
              classes={classes}
              numSelected={selected.length}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={rows.length}
            />
            <TableBody>
              {stableSort(rows, getComparator(order, orderBy))
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .filter(
                  (row) =>
                    !search ||
                    row.first_name.includes(search) ||
                    row.last_name.includes(search)
                )
                .map((row, index) => {
                  const isItemSelected = isSelected(row.id)
                  const labelId = `enhanced-table-checkbox-${index}`

                  return (
                    <TableRow hover>
                      <TableCell padding="checkbox">
                        <Checkbox
                          //Moved this funtionality to checkbox intead of entire row
                          onClick={(event) => handleClick(event, row.id)}
                          role="checkbox"
                          aria-checked={isItemSelected}
                          tabIndex={-1}
                          key={row.id}
                          selected={isItemSelected}
                          checked={isItemSelected}
                          inputProps={{"aria-labelledby": labelId}}
                        />
                      </TableCell>
                      <TableCell
                        component="th"
                        id={labelId}
                        scope="row"
                        padding="none"
                      >
                        {row.first_name}
                      </TableCell>
                      <TableCell align="left">{row.last_name}</TableCell>
                      <TableCell align="left">{row.email}</TableCell>
                      <TableCell align="left">{row.phone}</TableCell>
                      <TableCell align="left">{row.gender}</TableCell>
                      <TableCell>
                        <IconButton
                          aria-label="delete"
                          size="small"
                          color="secondary"
                          onClick={() => handleDeleteUser(row.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                        <IconButton
                          aria-label="edit"
                          size="small"
                          color="primary"
                          onClick={() => handleEditUser(row)}
                        >
                          <EditIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  )
                })}
              {emptyRows > 0 && (
                <TableRow style={{height: (dense ? 33 : 53) * emptyRows}}>
                  <TableCell colSpan={6} />
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onChangePage={handleChangePage}
          onChangeRowsPerPage={handleChangeRowsPerPage}
        />
      </Paper>
      <FormControlLabel
        control={<Switch checked={dense} onChange={handleChangeDense} />}
        label="Dense padding"
      />
    </div>
  )
}

const mapStateToProps = (state) => {
  return {
    snackbarreducer: state.snackbarreducer,
    users: state.users.users,
    submissionSuccessful: state.users.submissionSuccessful,
    message: state.messages,
    error: state.errors,
    utility: state.utility,
  }
}

export default connect(mapStateToProps, {
  getUsers,
  addUser,
  deleteUser,
  changeUser,
})(Users)
