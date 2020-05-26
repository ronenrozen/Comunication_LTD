import React, {Component} from "react";
import userAxios from "../Axios/userAxios";
import {Link, Redirect} from "react-router-dom"
import Modal from "../Modal/Modal";
import PasswordModal from "../Modal/PasswordModal";
import https from 'https';
const agent = new https.Agent({
    rejectUnauthorized: false
});

class Register extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: "",
            password: "",
            invalidEmail: false,
            invalidPassword: false,
            redirect: false,
            show:false
        };
    }

    inputChange = ({target: {name, value}}) => {
        this.setState({
            [name]: value,
        });
    };

    showModal = () => {
        this.setState({show: true});
    };

    hideModal = () => {
        this.setState({show: false});
    };

    onSubmit = async (e) => {
        e.preventDefault();
        this.setState({invalidEmail: false , invalidPassword: false});
        let userInfo = {
            email: this.state.email,
            password: this.state.password
        };
        try {
            await userAxios.post('register', userInfo, { httpsAgent: agent });
            this.setState({redirect: true});
        } catch (error) {
            console.log("error.response.code",error.response);
            if (error.response) {
                if (error.response.status === 409) {
                    this.setState({invalidEmail: true})
                } else if (error.response.status === 400) {
                    this.setState({invalidPassword: true})
                }
            }
            console.log('Error on login', error);
        }
    };

    render() {
        if (this.state.redirect) {
            return <Redirect to={'/'}/>
        }
        const showEmailTextError = this.state.invalidEmail ? "text-danger d-block" : "d-none";
        const showEmailInputError = this.state.invalidEmail ? "form-control is-invalid" : "form-control";
        const showPasswordTextError = this.state.invalidPassword ? "text-danger d-block" : "d-none";
        const showPasswordInputError = this.state.invalidPassword ? "form-control is-invalid" : "form-control";
        console.log("showPasswordTextError",showPasswordTextError);
        return (
            <div className={"wrapperContainer"}>
                <div className="innerContainer">
                    <h1 className={"header"}>Register New User</h1>
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
                                name="password"
                                onChange={this.inputChange}
                            />
                        </div>
                        <small className={showEmailTextError}>Email already in the system, try - <Link className="nav-link" to={"/forgotpassword"}>Forgot Password?</Link></small>
                        <small className={showPasswordTextError}>Invalid Password,please see password rules</small>
                        <small onClick={this.showModal}>click for password rules</small>
                        <input type={"submit"} value={"Register"} onClick={this.onSubmit}/>
                    </form>
                </div>
                <Modal show={this.state.show} handleClose={this.hideModal}>
                    <PasswordModal handleClose={this.hideModal} />
                </Modal>
            </div>
        );
    }
}

export default Register;
