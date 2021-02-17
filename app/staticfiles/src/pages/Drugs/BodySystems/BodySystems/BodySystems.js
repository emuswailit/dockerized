import React, {useState, useEffect} from "react"
import PageHeader from "../../../../components/common/PageHeader"
import BodySystemsForm from "./BodySystemsForm"
import {Search} from "@material-ui/icons"
import PeopleOutlineIcon from "@material-ui/icons/PeopleOutline"
import {
  makeStyles,
  Paper,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Toolbar,
  InputAdornment,
} from "@material-ui/core"
import useTable from "../../../../components/common/useTable"
import {getBodySystems} from "../../../../actions/body_systems"
import {connect} from "react-redux"
import Controls from "../../../../components/controls/Control"
const useStyles = makeStyles((theme) => ({
  pageContent: {
    margin: theme.spacing(1),
    padding: theme.spacing(1),
  },

  searchInput: {
    width: "75%",
  },
  newButton: {
    position: "absolute",
    right: "10px",
  },
}))


const headCells = [
  {id: "title", label: "Title"},
  {id: "description", label: "Description"},
]
const BodySystems = (props) => {
  const classes = useStyles()
  const [rows, setRows] = React.useState([])
  const [filterFn, setFilterFn] = useState({
    fn: (items) => {
      return items
    },
  })
  const {
    TblContainer,
    TblHead,
    TblPagination,
    recordsAfterPagingAndSorting,
  } = useTable(rows, headCells, filterFn)

  useEffect(() => {
    props.getBodySystems()
    setRows(props.bodysystems)
  }, [])

  useEffect(() => {
    setRows(props.bodysystems)
    console.log(rows.length)
  }, [props.bodysystems])

  const handleSearch = (e) => {
    let target = e.target
    setFilterFn({
      fn: (items) => {
        if (target.value == "") return items
        else
          return items.filter((x) => {
            if (
              x.title.toLowerCase().includes(target.value) ||
              x.description.toLowerCase().includes(target.value)
            ) {
              return true
            }
          })
      },
    })
  }
  return (
    <div>
      <PageHeader
        title="Human Body Systems"
        subTitle="Listing and description of human body systems"
        icon={<PeopleOutlineIcon fontSize="large" />}
      />

      <Paper className={classes.pageContent}>
        {/* <BodySystemsForm /> */}

        <Toolbar>
          <Controls.Input
            label="Search body systems"
            className={classes.searchInput}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
            onChange={handleSearch}
          />
        </Toolbar>
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
        <TblPagination />
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
