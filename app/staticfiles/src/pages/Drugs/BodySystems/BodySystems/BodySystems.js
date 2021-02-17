import React, {useState, useEffect} from "react"
import PageHeader from "../../../../components/common/PageHeader"
import BodySystemsForm from "./BodySystemsForm"
import PeopleOutlineIcon from "@material-ui/icons/PeopleOutline"
import {
  makeStyles,
  Paper,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@material-ui/core"
import useTable from "../../../../components/common/useTable"
import {getBodySystems} from "../../../../actions/body_systems"
import {connect} from "react-redux"
const useStyles = makeStyles((theme) => ({
  pageContent: {
    margin: theme.spacing(1),
    padding: theme.spacing(1),
  },
}))


const headCells = [
  {id: "title", label: "Title"},
  {id: "description", label: "Description"},
]
const BodySystems = (props) => {
  const classes = useStyles()
  const [rows, setRows] = React.useState([])

  const {TblContainer, TblHead, TblPagination, recordsAfterPagingAndSorting} = useTable(rows, headCells)

  useEffect(() => {
    props.getBodySystems()
    setRows(props.bodysystems)
  }, [])

  useEffect(() => {
    setRows(props.bodysystems)
    console.log(rows.length)
  }, [props.bodysystems])
  return (
    <div>
      <PageHeader
        title="Human Body Systems"
        subTitle="Listing and description of human body systems"
        icon={<PeopleOutlineIcon fontSize="large" />}
      />

      <Paper className={classes.pageContent}>
        {/* <BodySystemsForm /> */}
        <TblContainer>
          <TblHead />
          <TableBody>
            {recordsAfterPagingAndSorting().map((item) => (
              <TableRow>
                <TableCell>{item.title}</TableCell>
                <TableCell>{item.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </TblContainer>
        <TblPagination  />
      </Paper>
    </div>
  )
}
const mapStateToProps = (state) => {
  return {
    snackbarreducer: state.snackbarreducer,
    bodysystems: state.bodysystems.bodysystems,
    update: state.bodysystems.update,
  }
}

export default connect(mapStateToProps, {
  getBodySystems,
})(BodySystems)
