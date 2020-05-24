import React, {Component} from "react";
import Navbar from "./Components/Navbar";
import Login from "./Components/Login/Login";
import Register from "./Components/Regiester/Register";
import ForgotPassword from "./Components/ForgotPassword/ForgotPassword";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
import "./App.css";
import ForgotChangePassword from "./Components/ForgotPassword/ForgotChangePassword";
import Customers from "./Components/Customer/Customers";
import Home from "./Components/Home";
import ChangePassword from "./Components/ChangePassword";

class App extends Component {
    handleLogOut = () => {
        sessionStorage.clear()
    };

    render() {
        return (
            <Router>
                <div className="App">
                    <header className="App-header">
                        <Navbar logout={this.handleLogOut}/>
                    </header>
                    <div className="App-body">
                        <Switch>
                            <Route path="/changepassword">
                               <ChangePassword/>
                            </Route>
                            <Route path="/customers">
                                <Customers/>
                            </Route>
                            <Route path="/home">
                                <Home/>
                            </Route>
                            <Route path="/register">
                                <Register/>
                            </Route>
                            <Route path={"/forgotpassword"}>
                                <ForgotPassword/>
                            </Route>
                            <Route path={"/forgetchangepassword"}>
                                <ForgotChangePassword/>
                            </Route>
                            <Route path="/">
                                <Login/>
                            </Route>
                        </Switch>
                    </div>
                </div>
            </Router>
        );
    }
}

export default App;