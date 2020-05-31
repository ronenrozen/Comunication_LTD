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
            blockedUser: false,
            maxAttempts: false,
            invalidPassword: false,
            invalidEmail: false,
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
        this.setState({
            blockedUser: false,
            maxAttempts: false,
            invalidPassword: false,
            invalidEmail: false,
        });
        let userInfo = {
            email: this.state.email,
            password: this.state.password
        };
        try {
            const {data} = await userAxios.post('login', userInfo, {httpsAgent: agent});
            sessionStorage.clear();
            sessionStorage.setItem('user', JSON.stringify(data));
            this.setState({redirect: true}, () => console.log(this.state));
        } catch (error) {
            if (error.response && error.response.status === 400) {
                this.setState({blockedUser: true})
            } else if (error.response && error.response.status === 401) {
                this.setState({maxAttempts: true})
            } else if (error.response && error.response.status === 404) {
                this.setState({invalidPassword: true})
            } else if (error.response && error.response.status === 403) {
                this.setState({invalidEmail: true})
            }
            console.log('Error on login', error);
        }
    };

    render() {
        if (this.state.redirect || sessionStorage.getItem('user')) {
            return <Redirect to={'./home'}/>
        }
        const showBlockedUserTextError = this.state.blockedUser ? "text-danger d-block" : "d-none";
        const showMaxAttemptsTextError = this.state.maxAttempts ? "text-danger d-block" : "d-none";
        const showPasswordTextError = this.state.invalidPassword ? "text-danger display-block" : "display-none";
        const showPasswordInputError = this.state.invalidPassword ? "form-control is-invalid" : "form-control";
        const showEmailTextError = this.state.invalidEmail ? "text-danger display-block" : "display-none";
        const showEmailInputError = this.state.invalidEmail ? "form-control is-invalid" : "form-control";

        return (
            <div className={"wrapperContainer"}>
                <div className="innerContainer">
                    <h1 className={"header"}>Welcome</h1>
                    <form onSubmit={this.onSubmit}>
                        <div className={"input"}>
                            <i className={"fa fa-user"}/>
                            <input
                                className={showEmailInputError}
                                type="text"
                                placeholder={"Email"}
                                name={"email"}
                                onChange={this.inputChange}
                            />
                        </div>
                        <div className={"input"}>
                            <i className={"fa fa-unlock"}/>
                            <input
                                className={showPasswordInputError}
                                type="password"
                                placeholder={"Password"}
                                name={"password"}
                                onChange={this.inputChange}
                            />
                        </div>
                        <small className={showBlockedUserTextError}>Too many login attempts. user is blocked</small>
                        <small className={showEmailTextError}>There is no user with the email {this.state.email}</small>
                        <small className={showPasswordTextError}>Wrong password, try again</small>
                        <small className={showMaxAttemptsTextError}>You have reached max attempts, user will be blocked</small>
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
