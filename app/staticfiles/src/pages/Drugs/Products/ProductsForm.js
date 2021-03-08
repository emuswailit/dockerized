import {connect} from "react-redux"
import React, {useState, useEffect} from "react"
import {useForm, Form} from "../../../components/common/useForm"
import Controls from "../../../components/controls/Control"
import {Grid} from "@material-ui/core"
import {getManufacturers} from "../../../actions/manufacturers"
import {getPreparations} from "../../../actions/preparations"
import {getCategories} from "../../../actions/categories"
import Notification from "../../../components/common/Notification"
const initialFValues = {
  id: "",
  url: "",
  title: "",
  description: "",
  preparation: "",
  category: "",
  manufacturer: "",
  units_per_pack: "",
  packaging: "",
  is_prescription_only: false,
}
const ProductsForm = (props) => {
  const {addOrEdit, recordForEdit} = props

  const validate = (fieldValues = values) => {
    let temp = {...errors}
    if ("title" in fieldValues)
      temp.title = fieldValues.title ? "" : "This field is required"
    if ("packaging" in fieldValues)
      temp.packaging = fieldValues.packaging ? "" : "This field is required"
    if ("units_per_pack" in fieldValues)
      temp.units_per_pack = fieldValues.units_per_pack
        ? ""
        : "This field is required"
    if ("category" in fieldValues)
      temp.category =
        fieldValues.category.length != 0 ? "" : "This field is required"
    if ("manufacturer" in fieldValues)
      temp.manufacturer =
        fieldValues.manufacturer.length != 0 ? "" : "This field is required"

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
    props.getPreparations()
    props.getManufacturers()
    props.getCategories()
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

          <Controls.Input
            variant="outlined"
            label="Packaging"
            name="packaging"
            value={values.packaging}
            onChange={handleInputChange}
            error={errors.packaging}
          />
          <Controls.Input
            variant="outlined"
            type="number"
            label="Units Per Pack"
            name="units_per_pack"
            value={values.units_per_pack}
            onChange={handleInputChange}
            error={errors.units_per_pack}
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
            name="category"
            label="Select Category"
            value={values.category}
            onChange={handleInputChange}
            options={props.categories}
            error={errors.category}
          />
          <Controls.Select
            name="preparation"
            label="Select Preparation"
            value={values.preparation}
            onChange={handleInputChange}
            options={props.preparations}
            error={errors.preparation}
          />

          <Controls.Select
            name="manufacturer"
            label="Select Manufacturer"
            value={values.manufacturer}
            onChange={handleInputChange}
            options={props.manufacturers}
            error={errors.manufacturer}
          />
          {/* <Controls.DatePicker
            name="entry"
            label="Entry date"
            value={values.entry}
            onChange={handleInputChange}
          /> */}
          <Controls.Checkbox
            name="is_prescription_only"
            label="Prescription Only?"
            value={values.is_prescription_only}
            onChange={handleInputChange}
          />
          <div>
            <Controls.Button type="submit" text="Submit" />
            <Controls.Button text="Reset" color="default" onClick={resetForm} />
          </div>
          {/* TODO : Display this error to user in a firndly way*/}
         {props.error && <h1>{props.error}</h1>}

        </Grid>
      </Grid>
    </Form>
  )
}

const mapStateToProps = (state) => {
  return {
    categories: state.categories.categories,
    manufacturers: state.manufacturers.manufacturers,
    error: state.products.error,
    preparations: state.preparations.preparations,
  }
}

export default connect(mapStateToProps, {
  getPreparations,
  getManufacturers,
  getCategories,
})(ProductsForm)
