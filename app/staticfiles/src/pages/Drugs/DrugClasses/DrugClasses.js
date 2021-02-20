import React, {useState, useEffect} from "react"
import PageHeader from "../../../components/common/PageHeader"
import DrugClassesForm from "./DrugClassesForm"
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
  Grid,
} from "@material-ui/core"
import useTable from "../../../components/common/useTable"

import {
  addDrugClass,
  getDrugClasses,
  changeDrugClass,
  deleteDrugClass,
} from "../../../actions/drug_classes"
import {connect} from "react-redux"
import Controls from "../../../components/controls/Control"
import AddIcon from "@material-ui/icons/Add"
import Popup from "../../../components/common/Popup"
import Notification from "../../../components/common/Notification"
import ConfirmDialog from "../../../components/common/ConfirmDialog"
const useStyles = makeStyles((theme) => ({
  pageContent: {
    margin: theme.spacing(1),
    padding: theme.spacing(1),
  },

  searchInput: {
    width: "100%",
  },
  newButton: {
    position: "absolute",
    right: "10px",
  },
}))

const headCells = [
  {id: "title", label: "Title"},
  {id: "description", label: "Description"},
  {id: "bodysystem", label: "Body System"},
  {id: "actions", label: "Actions", disableSorting: true},
]
const DrugClasses = (props) => {
  const classes = useStyles()
  const [rows, setRows] = React.useState([])
  const [openPopup, setOpenPopup] = useState(false)
  const [recordForEdit, setRecordForEdit] = useState(null)
  const [filterFn, setFilterFn] = useState({
    fn: (items) => {
      return items
    },
  })
  const [confirmDialog, setConfirmDialog] = useState({
    isOpen: false,
    title: "",
    subTitle: "",
  })

  const [notify, setNotify] = useState({
    isOpen: false,
    message: "",
    type: "",
  })
  const {
    TblContainer,
    TblHead,
    TblPagination,
    recordsAfterPagingAndSorting,
  } = useTable(rows, headCells, filterFn)

  useEffect(() => {
    props.getDrugClasses()
    setRows(props.drugclasses)
  }, [])

  useEffect(() => {
    setRows(props.drugclasses)
    console.log(rows.length)
  }, [props.drugclasses])

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

  const addOrEdit = (DrugClass, resetForm) => {
    if (DrugClass.id == "") {
      props.addDrugClass(DrugClass)
    } else {
      props.changeDrugClass(DrugClass, DrugClass.id)
      props.getDrugClasses()
    }
    console.log("Final: ", DrugClass)
    resetForm()
    setOpenPopup(false)
    setRecordForEdit(null)
    setNotify({
      isOpen: true,
      message: "Submitted succesfully",
      type: "success",
    })
    props.getDrugClasses()
  }

  const openInPopUp = (item) => {
    setRecordForEdit(item)
    setOpenPopup(true)
  }
  const onDelete = (id) => {
    setConfirmDialog({
      ...confirmDialog,
      isOpen: false,
    })
    props.deleteDrugClass(id)
    setNotify({
      isOpen: true,
      message: "Deleted Successfully",
      type: "error",
    })
    // props.getDrugClasses()
  }

  return (
    <div>
      <PageHeader
        title="Drug classes"
        subTitle="Pharmacological drugs classifications"
        icon={<PeopleOutlineIcon fontSize="large" />}
      />

      <Paper className={classes.pageContent}>
        <Toolbar>
          <Grid container>
            <Grid item xs={6}>
              <Controls.Input
                label="Search drug classes"
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
            </Grid>

            <Grid item xs={6}>
              {" "}
              <Controls.Button
                text="Add New"
                variant="outlined"
                startIcon={<AddIcon />}
                className={classes.newButton}
                onClick={() => {
                  setOpenPopup(() => setOpenPopup(true)),
                    (setRecordForEdit = null)
                }}
              />
            </Grid>
          </Grid>
        </Toolbar>
        <TblContainer>
          <TblHead />
          <TableBody>
            {recordsAfterPagingAndSorting().map((item) => (
              <TableRow>
                <TableCell>{item.title}</TableCell>
                <TableCell>{item.description}</TableCell>
                <TableCell>{item.system_details.title}</TableCell>
                <TableCell>
                  <Controls.ActionButton
                    color="primary"
                    onClick={() => openInPopUp(item)}
                  >
                    <EditOutlinedIcon fontSize="small" />
                  </Controls.ActionButton>

                  <Controls.ActionButton
                    color="secondary"
                    onClick={() => {
                      setConfirmDialog({
                        isOpen: true,
                        title: "Are you sure to delete this record?",
                        subTitle: "You can't undo this operation",
                        onConfirm: () => {
                          onDelete(item.id)
                        },
                      })
                    }}
                  >
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
        <DrugClassesForm addOrEdit={addOrEdit} recordForEdit={recordForEdit} />
      </Popup>

      <Notification notify={notify} setNotify={setNotify} />

      <ConfirmDialog
        confirmDialog={confirmDialog}
        setConfirmDialog={setConfirmDialog}
      />
    </div>
  )
}
const mapStateToProps = (state) => {
  return {
    bodysystems: state.bodysystems.bodysystems,
    drugclasses: state.drugclasses.drugclasses,
    update: state.drugclasses.update,
  }
}

export default connect(mapStateToProps, {
  addDrugClass,
  getDrugClasses,
  changeDrugClass,
  deleteDrugClass,
})(DrugClasses)
