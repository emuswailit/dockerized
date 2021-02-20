import {connect} from "react-redux"
import React, {useState, useEffect} from "react"
import {useForm, Form} from "../../../components/common/useForm"
import Controls from "../../../components/controls/Control"
import {Grid} from "@material-ui/core"
import {getGenerics} from "../../../actions/generics"
import {getFormulations} from "../../../actions/formulations"

const initialFValues = {
  id: "",
  url: "",
  title: "",
  description: "",
  formulation: "",
  generic: "",
  unit: "",
  drug_sub_class_details: "",
  formulation_details: {
    id: "",
    url: "",
    title: "",
    description: "",
    owner: "",
    created: "",
    updated: "",
  },
  generic_details: {
    id: "",
    url: "",
    title: "",
    description: "",
    owner: "",
    created: "",
    updated: "",
  },
}
const PreparationsForm = (props) => {
  const {addOrEdit, recordForEdit} = props

  const validate = (fieldValues = values) => {
    let temp = {...errors}
    if ("title" in fieldValues)
      temp.title = fieldValues.title ? "" : "This field is required"
    // if ("description" in fieldValues)
    //   temp.description = fieldValues.description ? "" : "This field is required"
    if ("generic" in fieldValues)
      temp.generic =
        fieldValues.generic.length != 0 ? "" : "This field is required"
    if ("formulation" in fieldValues)
      temp.formulation =
        fieldValues.formulation.length != 0 ? "" : "This field is required"

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

  useEffect(() => {
    props.getFormulations()
    props.getGenerics()
  }, [])

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

          <Controls.Select
            name="generic"
            label="Drug Generic"
            value={values.generic}
            onChange={handleInputChange}
            options={props.generics}
            error={errors.generic}
          />

          <Controls.Select
            name="formulation"
            label="Formulation"
            value={values.formulation}
            onChange={handleInputChange}
            options={props.formulations}
            error={errors.formulation}
          />
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

const mapStateToProps = (state) => {
  return {
    generics: state.generics.generics,
    formulations: state.formulations.formulations,
    update: state.preparations.update,
  }
}

export default connect(mapStateToProps, {
  getGenerics,
  getFormulations,
})(PreparationsForm)
