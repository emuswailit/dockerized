import React, {Component} from "react"
import {connect} from "react-redux"

export class Dashy extends Component {
  componentDidMount() {
    console.log(this.props)
  }
  render() {
    return <div>
  
    </div>
  }
}

const mapStateToProps = (state) => {
  return {
    auth: state.auth,
  }
}

export default connect(mapStateToProps, null)(Dashy)
