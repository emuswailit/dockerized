import React, {useState, useEffect} from "react"
import PageHeader from "../../../components/common/PageHeader"
import UsersForm from "./UsersForm"
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

import {addUser, getUsers, changeUser, deleteUser} from "../../../actions/users"
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
  {id: "first_name", label: "First Name"},
  {id: "middle_name", label: "Middle Name"},
  {id: "last_name", label: "Last Name"},
  {id: "email", label: "Email"},
  {id: "phone", label: "Phone"},
  {id: "national_id", label: "National ID"},
  {id: "date_of_birth", label: "Date of birth"},
  {id: "gender", label: "Gender"},
  {id: "actions", label: "Actions", disableSorting: true},
]
const Users = (props) => {
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
    props.getUsers()
    setRows(props.users)
  }, [])

  useEffect(() => {
    setRows(props.users)
    console.log(rows.length)
  }, [props.users])

  const handleSearch = (e) => {
    let target = e.target
    setFilterFn({
      fn: (items) => {
        if (target.value == "") return items
        else
          return items.filter((x) => {
            if (
              x.first_name.toLowerCase().includes(target.value) ||
              x.middle_name.toLowerCase().includes(target.value) ||
              x.last_name.toLowerCase().includes(target.value) ||
              x.phone.toLowerCase().includes(target.value) ||
              x.national_id.toLowerCase().includes(target.value) ||
              x.email.toLowerCase().includes(target.value)
            ) {
              return true
            }
          })
      },
    })
  }

  const addOrEdit = (user, resetForm) => {
    if (user.id == "") {
      props.addUser(user)
    } else {
      props.changeUser(user, user.id)
    }

    if (props.auth.error === null) {
      resetForm()
      setOpenPopup(false)
      setRecordForEdit(null)
      // setNotify({
      //   isOpen: true,
      //   message: props.auth.message,
      //   type: "success",
      // })
      props.getUsers()
    } else if (props.auth.error) {
      
      setNotify({
        isOpen: true,
        message: props.auth.error,
        type: "error",
      })
    }
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
    props.deleteUser(id)

    setNotify({
      isOpen: true,
      message: "Deleted Successfully",
      type: "error",
    })
    // props.getUsers()
  }

  return (
    <div>
      <PageHeader
        title="Users"
        subTitle="All registered users"
        icon={<PeopleOutlineIcon fontSize="large" />}
      />

      <Paper className={classes.pageContent}>
        <Toolbar>
          <Grid container>
            <Grid item xs={6}>
              <Controls.Input
                label="Search users"
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
                <TableCell>{item.first_name}</TableCell>
                <TableCell>{item.middle_name}</TableCell>
                <TableCell>{item.last_name}</TableCell>
                <TableCell>{item.email}</TableCell>
                <TableCell>{item.phone}</TableCell>
                <TableCell>{item.national_id}</TableCell>
                <TableCell>{item.date_of_birth}</TableCell>
                <TableCell>{item.gender}</TableCell>
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

      <Popup title="Users" openPopup={openPopup} setOpenPopup={setOpenPopup}>
        <UsersForm addOrEdit={addOrEdit} recordForEdit={recordForEdit} />
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
    snackbarreducer: state.snackbarreducer,
    users: state.users.users,
    user: state.users.user,
    response_code: state.users.response_code,
    response_message: state.users.response_message,
    update: state.bodysystems.update,
  }
}

export default connect(mapStateToProps, {
  addUser,
  getUsers,
  changeUser,
  deleteUser,
})(Users)
