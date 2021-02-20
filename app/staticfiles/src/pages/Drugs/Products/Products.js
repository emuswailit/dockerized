import React, {useState, useEffect} from "react"
import PageHeader from "../../../components/common/PageHeader"
import ProductsForm from "./ProductsForm"
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
  addProduct,
  getProducts,
  changeProduct,
  deleteProduct,
} from "../../../actions/products"
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
  {id: "preparation", label: "Preparation"},
  // {id: "generic", label: "Generic"},
  {id: "formulation", label: "Formulation"},

  {id: "manufacturer", label: "Manufacturer"},
  {id: "units_per_pack", label: "Units Per Pack"},
  {id: "packaging", label: "Packaging"},
  {id: "category", label: "Category"},
  {id: "is_prescription_only", label: "Prescription Only"},
  {id: "actions", label: "Actions", disableSorting: true},
]
const Products = (props) => {
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
    props.getProducts()
    setRows(props.products)
  }, [])

  useEffect(() => {
    setRows(props.products)
  }, [props.products])

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
      props.addProduct(preparation)
    } else {
      props.changeProduct(preparation, preparation.id)
    }
    props.getProducts()
    resetForm()
    setOpenPopup(false)
    setRecordForEdit(null)
    setNotify({
      isOpen: true,
      message: "Submitted succesfully",
      type: "success",
    })
    props.getProducts()
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
    props.deleteProduct(id)
    setNotify({
      isOpen: true,
      message: "Deleted Successfully",
      type: "error",
    })
    // props.getProducts()
  }

  return (
    <div>
      <PageHeader
        title="Drug Products"
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
                <TableCell>{item ? item.title : "N/A"}</TableCell>
                <TableCell>
                  {item.preparation_details
                    ? item.preparation_details.title
                    : "N/A"}
                </TableCell>
                <TableCell>
                  {item.preparation_details
                    ? item.preparation_details.formulation_details.title
                    : "N/A"}
                </TableCell>

                <TableCell>
                  {item.manufacturer_details
                    ? item.manufacturer_details.title
                    : "N/A"}
                </TableCell>
                <TableCell>{item.units_per_pack}</TableCell>
                <TableCell>{item.packaging}</TableCell>
                <TableCell>
                  {item.category_details ? item.category_details.title : "N/A"}
                </TableCell>
                <TableCell>
                  {item.is_prescription_only ? "Yes" : "No"}
                </TableCell>
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
        title="Drug Products"
        openPopup={openPopup}
        setOpenPopup={setOpenPopup}
      >
        <ProductsForm addOrEdit={addOrEdit} recordForEdit={recordForEdit} />
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
    products: state.products.products,
    update: state.preparations.update,
  }
}

export default connect(mapStateToProps, {
  addProduct,
  getProducts,
  changeProduct,
  deleteProduct,
})(Products)
