import React, {useState} from "react"
import {makeStyles} from "@material-ui/core"

const useStyles = makeStyles((theme) => ({
  root: {
    "& .MuiFormControl-root": {
      width: "90%",
      margin: theme.spacing(1),
    },
  },
}))
export function useForm(initialFValues, validateOnChange = false, validate) {
  const classes = useStyles()
  const [values, setValues] = useState(initialFValues)
  const [errors, setErrors] = useState({})

  const handleInputChange = (e) => {
    const {name, value} = e.target
    setValues({
      ...values,
      [name]: value,
    })
    console.log("Changed", value)

    if (validateOnChange) validate({[name]: value})
  }

  const resetForm = () => {
    setValues(initialFValues)
    setErrors({})
  }
  return {
    values,
    setValues,
    handleInputChange,
    errors,
    setErrors,
    resetForm,
  }
}

export function Form(props) {
  const classes = useStyles()
  const {children, ...other} = props
  return (
    <form className={classes.root} autoComplete="off" {...other}>
      {props.children}
    </form>
  )
}
