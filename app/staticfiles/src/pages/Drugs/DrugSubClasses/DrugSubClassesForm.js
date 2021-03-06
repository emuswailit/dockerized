import {connect} from "react-redux"
import React, {useState, useEffect} from "react"
import {useForm, Form} from "../../../components/common/useForm"
import Controls from "../../../components/controls/Control"
import {Grid} from "@material-ui/core"
import {getDrugClasses} from "../../../actions/drug_classes"
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
  drug_class: "",
  system_details: {
    id: "",
    url: "",
    title: "",
    description: "",
    owner: "",
    created: "",
    updated: "",
  },
}
const DrugSubClassesForm = (props) => {
  const {addOrEdit, recordForEdit} = props

  const validate = (fieldValues = values) => {
    let temp = {...errors}
    if ("title" in fieldValues)
      temp.title = fieldValues.title ? "" : "This field is required"
    if ("description" in fieldValues)
      temp.description = fieldValues.description ? "" : "This field is required"
    if ("drug_class" in fieldValues)
      temp.drug_class =
        fieldValues.drug_class.length != 0 ? "" : "This field is required"

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
    props.getDrugClasses()
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
            name="drug_class"
            label="Drug class"
            value={values.drug_class}
            onChange={handleInputChange}
            options={props.drugclasses}
            error={errors.drug_class}
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
    drugclasses: state.drugclasses.drugclasses,
    drugsubclasses: state.drugsubclasses.drugsubclasses,
    update: state.drugsubclasses.update,
  }
}

export default connect(mapStateToProps, {
  getDrugClasses,
})(DrugSubClassesForm)
