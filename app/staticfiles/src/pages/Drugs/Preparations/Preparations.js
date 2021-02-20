import React, {useState, useEffect} from "react"
import PageHeader from "../../../components/common/PageHeader"
import PreparationsForm from "./PreparationsForm"
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
  addPreparation,
  getPreparations,
  changePreparation,
  deletePreparation,
} from "../../../actions/preparations"
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
  {id: "generic", label: "Preparation "},
  {id: "formulation", label: "Formulation"},
  {id: "actions", label: "Actions", disableSorting: true},
]
const Preparations = (props) => {
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
    props.getPreparations()
    setRows(props.preparations)
  }, [])

  useEffect(() => {
    setRows(props.preparations)
  }, [props.preparations])

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

  const addOrEdit = (preparation, resetForm) => {
    if (preparation.id == "") {
      props.addPreparation(preparation)
    } else {
      props.changePreparation(preparation, preparation.id)
    }
    props.getPreparations()
    resetForm()
    setOpenPopup(false)
    setRecordForEdit(null)
    setNotify({
      isOpen: true,
      message: "Submitted succesfully",
      type: "success",
    })
    props.getPreparations()
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
    props.deletePreparation(id)
    setNotify({
      isOpen: true,
      message: "Deleted Successfully",
      type: "error",
    })
    // props.getPreparations()
  }

  return (
    <div>
      <PageHeader
        title="Drug Preparations"
        subTitle="Assorment of drug preparations"
        icon={<PeopleOutlineIcon fontSize="large" />}
      />

      <Paper className={classes.pageContent}>
        <Toolbar>
          <Grid container>
            <Grid item xs={6}>
              <Controls.Input
                label="Search drug preparations"
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
                <TableCell>{item.generic_details.title}</TableCell>
                <TableCell>{item.formulation_details.title}</TableCell>

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
        title="Drug Preparations"
        openPopup={openPopup}
        setOpenPopup={setOpenPopup}
      >
        <PreparationsForm addOrEdit={addOrEdit} recordForEdit={recordForEdit} />
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
    generics: state.generics.generics,
    formulations: state.formulations.formulations,
    preparations: state.preparations.preparations,
    update: state.preparations.update,
  }
}

export default connect(mapStateToProps, {
  addPreparation,
  getPreparations,
  changePreparation,
  deletePreparation,
})(Preparations)
