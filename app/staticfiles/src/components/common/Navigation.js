import React, {useState, Fragment} from "react"
import {withStyles} from "@material-ui/core/styles"
import Drawer from "@material-ui/core/Drawer"
import Grid from "@material-ui/core/Grid"
import Button from "@material-ui/core/Button"
import List from "@material-ui/core/List"
import ListItem from "@material-ui/core/ListItem"
import ListItemIcon from "@material-ui/core/ListItemIcon"
import ListItemText from "@material-ui/core/ListItemText"
import ListSubheader from "@material-ui/core/ListSubheader"
import Typography from "@material-ui/core/Typography"
import Collapse from "@material-ui/core/Collapse"
import AddIcon from "@material-ui/icons/Add"
import RemoveIcon from "@material-ui/icons/Remove"
import ShowChartIcon from "@material-ui/icons/ShowChart"
import AppBar from "@material-ui/core/AppBar"
import Toolbar from "@material-ui/core/Toolbar"
import IconButton from "@material-ui/core/IconButton"
import MenuIcon from "@material-ui/icons/Menu"
import {useHistory} from "react-router-dom"
import {logout} from "../../actions/auth"
import {useDispatch, useSelector} from "react-redux"
import {Badge, InputBase} from "@material-ui/core"
import NotificationsNoneIcon from "@material-ui/icons/NotificationsNone"
import PowerSettingsNewIcon from "@material-ui/icons/PowerSettingsNew"
import ChatBubbleOutlineIcon from "@material-ui/icons/ChatBubbleOutline"
import SearchIcon from "@material-ui/icons/Search"
const styles = (theme) => ({
  root: {
    flexGrow: 1,
  },

  searchInput: {
    opacity: "0.6",
    padding: "0px 8px",
    fontSize: "0.8rem",
    "&:hover": {
      backgroundColor: "#f2f2f2",
    },
    "& .MuiSvgIcon-root": {
      marginRight: "8px",
    },
  },
  flex: {
    flex: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  toolbarMargin: theme.mixins.toolbar,
  aboveDrawer: {
    zIndex: theme.zIndex.drawer + 1,
    backgroundColor: "#fff",
  },
  alignContent: {
    alignSelf: "center",
  },
  listSubheader: {
    padding: 0,
    minWidth: 0,
    color: "inherit",
    "&:hover": {
      background: "inherit",
    },
  },
})

const ListItems = ({items, visible, onClick}) => (
  <Collapse in={visible}>
    {items
      .filter(({hidden}) => !hidden)
      .map(({label, disabled, Icon}, i) => (
        <ListItem button key={i} disabled={disabled} onClick={onClick(label)}>
          <ListItemIcon>
            <Icon />
          </ListItemIcon>
          <ListItemText>{label}</ListItemText>
        </ListItem>
      ))}
  </Collapse>
)

const Navigation = withStyles(styles)(({classes, user}) => {
  const dispatch = useDispatch()
  console.log("user here", user)

  const history = useHistory()
  const [open, setOpen] = useState(false)
  const [drawer, setDrawer] = useState(false)
  const [content, setContent] = useState("Home")
  const [items] = useState({
    ADMIN: [
      {label: "Users", Icon: AddIcon},
      {label: "Body Systems", Icon: RemoveIcon},
      {label: "Drug Classes", Icon: ShowChartIcon},
      {label: "Drug Sub Classes", Icon: ShowChartIcon},
      {label: "Drug Formulations", Icon: ShowChartIcon},
      {label: "Drug Generics", Icon: ShowChartIcon},
      {label: "Drug Preparations", Icon: ShowChartIcon},
      {label: "Drug Posologies", Icon: ShowChartIcon},
      {label: "Drug Intake Frequencies", Icon: ShowChartIcon},
      {label: "Drug Intake Instructions", Icon: ShowChartIcon},
      {label: "Drug Products", Icon: ShowChartIcon},
      {label: "Drug Manufacturers", Icon: ShowChartIcon},
      {label: "Drug Distributors", Icon: ShowChartIcon},
    ],
    CLIENTS: [
      {label: "Add Memory", Icon: AddIcon},
      {label: "Usage", Icon: ShowChartIcon},
    ],
    PHARMACISTS: [
      {label: "Add Storage", Icon: AddIcon},
      {label: "Usage", Icon: ShowChartIcon},
    ],
    PRESCRIBERS: [
      {label: "Add Network", Icon: AddIcon, disabled: true},
      {label: "Usage", Icon: ShowChartIcon},
    ],
  })
  const [sections, setSections] = useState({
    ADMIN: true,
    CLIENTS: false,
    PHARMACISTS: false,
    PRESCRIBERS: false,
  })

  const onClick = (content) => () => {
    setOpen(false)
    setContent(content)
    if (content == "Users") {
      history.push("/users")
    }

    if (content == "Body Systems") {
      history.push("/body_systems")
    }

    if (content == "Drug Classes") {
      history.push("/drug_classes")
    }

    if (content == "Drug Sub Classes") {
      history.push("/sub_classes")
    }
    if (content == "Drug Formulations") {
      history.push("/formulations")
    }

    if (content == "Drug Generics") {
      history.push("/generics")
    }

    if (content == "Drug Preparations") {
      history.push("/preparations")
    }

    if (content == "Drug Posologies") {
      history.push("/posologies")
    }

    if (content == "Drug Intake Frequencies") {
      history.push("/frequencies")
    }

    if (content == "Drug Intake Instructions") {
      history.push("/instructions")
    }

    if (content == "Drug Manufacturers") {
      history.push("/manufacturers")
    }

    if (content == "Drug Distributors") {
      history.push("/distributors")
    }

    if (content == "Drug Products") {
      history.push("/products")
    }
    if (content == "") {
      history.push("/")
    }
  }
  const toggleDrawer = () => {
    setOpen(!open)
  }
  const onLogOut = () => {
    dispatch(logout())
    console.log("logout again")
  }

  const toggleSection = (name) => () => {
    setSections({...sections, [name]: !sections[name]})
  }

  const MyToolbar = withStyles(styles)(({classes, title, onMenuClick}) => (
    <Fragment>
      <AppBar className={classes.aboveDrawer}>
        <Toolbar>
          <Grid container xs={12} alignItems="center">
            <Grid item>
              <IconButton
                className={classes.menuButton}
                color="inherit"
                aria-label="Menu"
                onClick={onMenuClick}
              >
                <MenuIcon />
              </IconButton>
              {/* <Typography variant="h6" color="inherit">
                {title}
              </Typography> */}
            </Grid>

            <Grid sm alignItems="center">
              <InputBase
                className={classes.searchInput}
                placeholder="Search topics"
                startAdornment={<SearchIcon fontSize="small" />}
              />
            </Grid>
            <Grid item alignItems="flex-end">
              <IconButton>
                <Badge badgeContent={4} color="primary">
                  <NotificationsNoneIcon />
                </Badge>
              </IconButton>
              <IconButton>
                <Badge badgeContent={4} color="secondary">
                  <ChatBubbleOutlineIcon />
                </Badge>
              </IconButton>

              <IconButton onClick={onLogOut}>
                <PowerSettingsNewIcon />
              </IconButton>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
      <div className={classes.toolbarMargin} />
    </Fragment>
  ))

  return (
    <div className={classes.root}>
      <MyToolbar title={content} onMenuClick={toggleDrawer} />

      <Grid container justify="space-between">
        {/* <Grid item className={classes.alignContent}>
          <Typography>{content} Here</Typography>
        </Grid> */}
        <Grid item>
          <Drawer open={open} onClose={() => setOpen(false)}>
            <List>
              {user.is_staff ? (
                <Fragment>
                  <ListSubheader>
                    <Button
                      disableRipple
                      classes={{root: classes.listSubheader}}
                      onClick={toggleSection("ADMIN")}
                    >
                      ADMIN
                    </Button>
                  </ListSubheader>
                  <ListItems
                    visible={sections.ADMIN}
                    items={items.ADMIN}
                    onClick={onClick}
                  />
                </Fragment>
              ) : null}

              <ListSubheader>
                <Button
                  disableRipple
                  classes={{root: classes.listSubheader}}
                  onClick={toggleSection("CLIENTS")}
                >
                  CLIENTS
                </Button>
              </ListSubheader>
              <ListItems
                visible={sections.CLIENTS}
                items={items.CLIENTS}
                onClick={onClick}
              />

              {user.is_pharmacist ? (
                <Fragment>
                  {" "}
                  <ListSubheader>
                    <Button
                      disableRipple
                      classes={{root: classes.listSubheader}}
                      onClick={toggleSection("PHARMACISTS")}
                    >
                      PHARMACISTS
                    </Button>
                  </ListSubheader>
                  <ListItems
                    visible={sections.PHARMACISTS}
                    items={items.PHARMACISTS}
                    onClick={onClick}
                  />
                </Fragment>
              ) : null}

              {user.is_prescriber ? (
                <Fragment>
                  {" "}
                  <ListSubheader>
                    <Button
                      disableRipple
                      classes={{root: classes.listSubheader}}
                      onClick={toggleSection("PRESCRIBERS")}
                    >
                      PRESCRIBERS
                    </Button>
                  </ListSubheader>
                  <ListItems
                    visible={sections.PRESCRIBERS}
                    items={items.PRESCRIBERS}
                    onClick={onClick}
                  />
                </Fragment>
              ) : null}
            </List>
          </Drawer>
        </Grid>
      </Grid>
    </div>
  )
})

export default Navigation
