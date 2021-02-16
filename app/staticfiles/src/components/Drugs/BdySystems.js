import React from "react"
import PageHeader from "../common/PageHeader"
import PeopleOutlineIcon from "@material-ui/icons/PeopleOutline"

export default function BdySystems() {
  return (
    <PageHeader
      title="Human Body Systems"
      subTitle="Listing and description of human body systems"
      icon={<PeopleOutlineIcon fontSize="large" />}
    />
  )
}
