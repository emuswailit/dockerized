import React, {useState, useEffect} from "react"
import PageHeader from "../../../../components/common/PageHeader"
import BodySystemsForm from "./BodySystemsForm"
import {EditOutlined, Search} from "@material-ui/icons"
import PeopleOutlineIcon from "@material-ui/icons/PeopleOutline"
import EditOutlinedIcon from "@material-ui/icons/EditOutlined"
import CloseIcon from "@material-ui/icons/Close"
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

import {addBodySystem, getBodySystems, changeBodySystem} from "../../../../actions/body_systems"
import {connect} from "react-redux"
import Controls from "../../../../components/controls/Control"
import AddIcon from "@material-ui/icons/Add"
import Popup from "../../../../components/common/Popup"
import Notification from "../../../../components/common/Notification"
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
  {id: "actions", label: "Actions", disableSorting: true},
]
const BodySystems = (props) => {
  const classes = useStyles()
  const [rows, setRows] = React.useState([])
  const [openPopup, setOpenPopup] = useState(false)
  const [recordForEdit, setRecordForEdit] = useState(null)
  const [filterFn, setFilterFn] = useState({
    fn: (items) => {
      return items
    },
  })

  const[notify, setNotify]=useState({isOpen:false, message:'', type:''})
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




  const addOrEdit = (bodySystem, resetForm) => {
    if (bodySystem.id=="") {
      props.addBodySystem(bodySystem)
    }else{
     props.changeBodySystem(bodySystem, bodySystem.id)
    }
  console.log("Final: ",bodySystem)
    resetForm()
    setOpenPopup(false)
    setRecordForEdit(null)
    setNotify({
       isOpen: true,
      message: "Submitted succesfully",
      type:"success"
    }
     
    )
    props.getBodySystems()
  }

  const openInPopUp = (item) => {

    setRecordForEdit(item)
    setOpenPopup(true)
  }

  return (
    <div>
      <PageHeader
        title="Human Body Systems"
        subTitle="Listing and description of human body systems"
        icon={<PeopleOutlineIcon fontSize="large" />}
      />

      <Paper className={classes.pageContent}>
 
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
          <Controls.Button
            text="Add New"
            variant="outlined"
            startIcon={<AddIcon />}
            className={classes.newButton}
            onClick={() => {
              setOpenPopup(() => setOpenPopup(true)), setRecordForEdit=null
            }}
          />
        </Toolbar>
        <TblContainer>
          <TblHead />
          <TableBody>
            {recordsAfterPagingAndSorting().map((item) => (
              <TableRow>
                <TableCell>{item.title}</TableCell>
                <TableCell>{item.description}</TableCell>
                <TableCell>
                  <Controls.ActionButton
                    color="primary"
                    onClick={()=>openInPopUp(item)}
                  >
                    <EditOutlinedIcon fontSize="small" />
                  </Controls.ActionButton>

                  <Controls.ActionButton color="secondary">
                    <CloseIcon fontSize="small" />
                  </Controls.ActionButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </TblContainer>
        <TblPagination />
      </Paper>

      <Popup
        title="Body Systems"
        openPopup={openPopup}
        setOpenPopup={setOpenPopup}
      >
        <BodySystemsForm addOrEdit={addOrEdit} recordForEdit={recordForEdit} />
      </Popup>

      <Notification notify={notify} setNotify={setNotify}/>
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
  addBodySystem,
  getBodySystems,changeBodySystem
})(BodySystems)
