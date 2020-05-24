import React, {Component} from 'react';
import userAxios from "../Axios/userAxios";
import {Redirect} from "react-router-dom";
import '../Login/login.css'

class ForgotPassword extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: "",
            invalidEmail: false,
            redirect: false
        };
    }

    inputChange = ({target: {name, value}}) => {
        this.setState({
            [name]: value,
        });
    };

    onSubmit = async (e) => {
        e.preventDefault();
        this.setState({invalidEmail: false});
        let userInfo = {
            email: this.state.email
        };
        try {
            await userAxios.post('forgot_password', userInfo);
            this.setState({redirect: true});
        } catch (error) {
            this.setState({invalidEmail: true});
            console.log('Error on login', error);
        }
    };

    render() {
        if (this.state.redirect) {
            return <Redirect to={'/forgetchangepassword'}/>
        }
        console.log(this.state);
        const showEmailTextError = this.state.invalidEmail ? "text-danger display-block" : "display-none";
        const showEmailInputError = this.state.invalidEmail ? "form-control is-invalid" : "form-control";
        console.log(showEmailTextError);
        return (
            <div className={"wrapperContainer"}>
                <div className="innerContainer">
                    <h1 className={"header"}>Forgot Password?</h1>
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
                        <small className={showEmailTextError}>No such email in the system</small>
                        <input type={"submit"} value={"Submit"} onClick={this.onSubmit}/>
                    </form>
                </div>
            </div>
        );
    }
}

export default ForgotPassword;