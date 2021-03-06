import {connect} from "react-redux"
import React, {useState, useEffect} from "react"
import {useForm, Form} from "../../../components/common/useForm"
import Controls from "../../../components/controls/Control"
import { Grid } from "@material-ui/core"

const categoryItems = [
  {id: "choice1", title: "Choice 1"},
  {id: "choice2", title: "Choice 2"},
  {id: "choice3", title: "Choice 3"},
]

const initialFValues = {
  id: "",
  url: "",
  title: "",
  description: "",
}
const BodySystemsForm = (props) => {
  const {addOrEdit, recordForEdit} = props
  const validate = (fieldValues = values) => {
    let temp = {...errors}
    if ("title" in fieldValues)
      temp.title = fieldValues.title ? "" : "This field is required"
    if ("description" in fieldValues)
      temp.description = fieldValues.description ? "" : "This field is required"
    // if ("departmentId" in fieldValues)
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
            label="Title"
            name="title"
            value={values.title}
            onChange={handleInputChange}
            error={errors.title}
          />
          <Controls.Input
            variant="outlined"
            label="Description"
            name="description"
            value={values.description}
            onChange={handleInputChange}
            error={errors.description}
          />
        </Grid>
        <Grid item sm={6} xs={12}>
          {/* <Controls.RadioGroup
            name="category"
            label="Category"
            value={values.gender}
            onChange={handleInputChange}
            items={categoryItems}
          /> */}

          {/* <Controls.Select
            name="departmentId"
            label="Department"
            value={values.departmentId}
            onChange={handleInputChange}
            options={employeeService.getDepartmentCollection()}
            error={errors.departmentId}
          /> */}
          {/* <Controls.DatePicker
            name="entry"
            label="Entry date"
            value={values.entry}
            onChange={handleInputChange}
          /> */}
          {/* <Controls.Checkbox
            name="is_active"
            label="Is Active"
            value={values.is_active}
            onChange={handleInputChange}
          /> */}
          <div>
            <Controls.Button type="submit" text="Submit" />
            <Controls.Button text="Reset" color="default" onClick={resetForm} />
          </div>
        </Grid>
      </Grid>
    </Form>
  )
}

export default BodySystemsForm
