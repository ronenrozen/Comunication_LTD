import React, {Component} from "react";
import "./login.css";
import userAxios from "../Axios/userAxios";
import {Link, Redirect} from "react-router-dom"
import https from 'https';

const agent = new https.Agent({
    rejectUnauthorized: false
});
class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: "",
            password: "",
            wrongEmailOrPassword: false,
            redirect: false,
        };
    }

    inputChange = ({target: {name, value}}) => {
        this.setState({
            [name]: value,
        });
    };

    onSubmit = async (e) => {
        e.preventDefault();
        this.setState({wrongEmailOrPassword: false});
        let userInfo = {
            email: this.state.email,
            password: this.state.password
        };
        try {
            const {data} = await userAxios.post('login', userInfo,{ httpsAgent: agent });
            sessionStorage.clear();
            sessionStorage.setItem('user',JSON.stringify(data));
            this.setState({redirect: true},()=>console.log(this.state));
        } catch (error) {
            this.setState({wrongEmailOrPassword: true});
            console.log('Error on login', error);
        }
    };

    render() {
        if (this.state.redirect || sessionStorage.getItem('user')) {
            return <Redirect to={'./home'}/>
        }
        const showEmailAndPasswordError = this.state.wrongEmailOrPassword ? "text-danger display-block" : "display-none";
        const showInputErrors = this.state.wrongEmailOrPassword ? "form-control is-invalid" : "form-control";

        return (
            <div className={"wrapperContainer"}>
                <div className="innerContainer">
                    <h1 className={"header"}>Welcome</h1>
                    <form onSubmit={this.onSubmit}>
                        <div className={"input"}>
                            <i className={"fa fa-user"}/>
                            <input
                                className={showInputErrors}
                                type="text"
                                placeholder={"Email"}
                                name={"email"}
                                onChange={this.inputChange}
                            />
                        </div>
                        <div className={"input"}>
                            <i className={"fa fa-unlock"}/>
                            <input
                                className={showInputErrors}
                                type="password"
                                placeholder={"Password"}
                                name={"password"}
                                onChange={this.inputChange}
                            />
                        </div>
                        <small className={showEmailAndPasswordError}>Email or Password is incorrect please try
                            again</small>
                        <input type={"submit"} value={"Login"} onClick={this.onSubmit}/>
                        <Link className="nav-link" to={"/register"}>Register</Link>
                        <Link className="nav-link" to={"/forgotpassword"}>Forgot Password?</Link>
                    </form>
                </div>
            </div>
        );
    }
}

export default Login;
