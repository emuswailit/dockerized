import {connect} from "react-redux"
import React, {useState, useEffect} from "react"
import {useForm, Form} from "../../../components/common/useForm"
import Controls from "../../../components/controls/Control"
import moment from "moment"
import {
  Grid,
  List,
  ListItem,
  ListItemText,
  makeStyles,
  Typography,
} from "@material-ui/core"

const genderItems = [
  {id: "Female", title: "Female"},
  {id: "Male", title: "Male"},
]
const useStyles = makeStyles((theme) => ({
  demo: {
    backgroundColor: theme.palette.background.paper,
  },
}))
const initialFValues = {
  id: "",
  url: "",
  first_name: "",
  middle_name: "",
  last_name: "",
  email: "",
  phone: "",
  national_id: "",
  gender: "",
  date_of_birth: moment(new Date()).format("YYYY-MM-DD"),
  password: "",
  confirm_password: "",
  is_active: true,
}
const UsersForm = (props) => {
  const classes = useStyles()
  const [dense, setDense] = React.useState(false)
  const [secondary, setSecondary] = React.useState(false)

  const {addOrEdit, recordForEdit} = props
  const validate = (fieldValues = values) => {
    let temp = {...errors}
    if ("first_name" in fieldValues)
      temp.first_name = fieldValues.first_name ? "" : "This field is required"
    if ("last_name" in fieldValues)
      temp.last_name = fieldValues.last_name ? "" : "This field is required"
    if ("email" in fieldValues)
      temp.email = fieldValues.email ? "" : "This field is required"
    if ("phone" in fieldValues)
      temp.phone = fieldValues.phone ? "" : "This field is required"
    if ("national_id" in fieldValues)
      temp.national_id = fieldValues.national_id ? "" : "This field is required"

    if ("date_of_birth" in fieldValues)
      temp.date_of_birth = fieldValues.date_of_birth
        ? ""
        : "This field is required"

    // if ("national_id" in fieldValues)
    //   temp.departmentId =
    //     fieldValues.departmentId.length != 0 ? "" : "This field is required"

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
    if (validate()) addOrEdit(values, resetForm)
  }

  useEffect(() => {
    if (props.user != null) {
      setErrors(props.auth.error)
      if (validate()) addOrEdit(props.user, resetForm)
    }
 
  }, [props.auth.error])

  useEffect(() => {
    if (recordForEdit != null) {
      setValues({
        ...recordForEdit,
      })
    }
  }, [recordForEdit])

  return (
    <Form onSubmit={handleSubmit}>
      <Grid container>
        <Grid item sm={6} xs={12}>
          <Controls.Input
            variant="outlined"
            label="First Name"
            name="first_name"
            value={values.first_name}
            onChange={handleInputChange}
            error={errors.first_name}
          />
          <Controls.Input
            variant="outlined"
            label="Middle Name"
            name="middle_name"
            value={values.middle_name}
            onChange={handleInputChange}
            error={errors.middle_name}
          />
          <Controls.Input
            variant="outlined"
            label="Last Name"
            name="last_name"
            value={values.last_name}
            onChange={handleInputChange}
            error={errors.last_name}
          />
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
            label="Phone"
            name="phone"
            value={values.phone}
            onChange={handleInputChange}
            error={errors.phone}
          />
          <Controls.Input
            variant="outlined"
            label="National ID"
            name="national_id"
            value={values.national_id}
            onChange={handleInputChange}
            error={errors.national_id}
          />
        </Grid>
        <Grid item sm={6} xs={12}>
          <Controls.RadioGroup
            name="gender"
            label="Gender"
            value={values.gender}
            onChange={handleInputChange}
            items={genderItems}
          />

          {/* <Controls.Select
            name="departmentId"
            label="Department"
            value={values.departmentId}
            onChange={handleInputChange}
            options={employeeService.getDepartmentCollection()}
            error={errors.departmentId}
          /> */}
          <Controls.DatePicker
            name="date_of_birth"
            label="Date of birth"
            value={values.date_of_birth}
            onChange={handleInputChange}
          />
          <Controls.Input
            variant="outlined"
            label="Password"
            name="password"
            value={values.password}
            onChange={handleInputChange}
            error={errors.password}
          />
          <Controls.Input
            variant="outlined"
            label="Confirm password"
            name="confirm_password"
            value={values.confirm_password}
            onChange={handleInputChange}
            error={errors.confirm_password}
          />
          <div>
            <Controls.Button type="submit" text="Submit" />
            <Controls.Button text="Reset" color="default" onClick={resetForm} />
          </div>
          <div>
            {props.auth.error ? (
              <div className={classes.demo}>
                <List dense={dense}>
                  {Object.entries(props.auth.error).map(([key, value]) => {
                    return (
                      <ListItem>
                        <Typography variant="caption" color="secondary">
                          {value}
                        </Typography>
                      </ListItem>
                    )
                  })}
                </List>
              </div>
            ) : (
              // <div>
              //   {Object.entries(props.form_errors).map(([key, value]) => {
              //       return (
              //         <li>
              //          <h6 color={}> {value}</h6>
              //         </li>
              //       );
              //       })}
              // </div>
              <h2>No errors</h2>
            )}
          </div>
        </Grid>
      </Grid>
    </Form>
  )
}

const mapStateToProps = (state) => {
  return {
    auth: state.auth,
    user: state.users.user,
  }
}

export default connect(mapStateToProps, {})(UsersForm)
