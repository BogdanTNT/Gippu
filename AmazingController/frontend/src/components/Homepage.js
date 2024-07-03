import React, { Component } from 'react'
import Settings from './Settings'
import { BrowserRouter as router, Route, Link, Redirect, Routes } from 'react-router-dom'

export default class HomePage extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
        <Router>
            <Routes>
                <Route exact path='/'><h1>ja</h1></Route>
                <Route path="/settings" component={Settings}/>
            </Routes>
        </Router>)
    }
}