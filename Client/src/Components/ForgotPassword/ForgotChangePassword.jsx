import React, {Component} from 'react';
import userAxios from "../Axios/userAxios";
import {Link, Redirect} from "react-router-dom";
import '../Login/login.css'
import Modal from '../Modal/Modal'
import PasswordModal from "../Modal/PasswordModal";
import https from 'https';

const agent = new https.Agent({
    rejectUnauthorized: false
});
class ForgotChangePassword extends Component {
    constructor(props) {
        super(props);
        this.state = {
            key: "",
            email: "",
            password: "",
            invalidEmail: false,
            invalidKey: false,
            invalidPassword: false,
            samePassword: false,
            redirect: false,
            show: false
        };
    }

    handleChange = ({target: {name, value}}) => {
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
        this.setState({invalidKey: false, invalidPassword: false, invalidEmail: false, samePassword: false});
        let userInfo = {
            email: this.state.email,
            key: this.state.key,
            password: this.state.password
        };
        try {
            await userAxios.post('forgot_change_password', userInfo,{httpsAgent: agent});
            this.setState({redirect: true});
        } catch (error) {
            console.log(error.response)
            if (error.response) {
                if (error.response.status === 400) {
                    this.setState({invalidKey: true})
                } else if (error.response.status === 403) {
                    this.setState({invalidPassword: true})
                } else if (error.response.status === 409) {
                    this.setState({invalidEmail: true})
                } else if (error.response.status === 401) {
                    this.setState({samePassword: true})
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
        const showKeyTextError = this.state.invalidKey ? "text-danger display-block" : "d-none";
        const showKeyError = this.state.invalidKey ? "form-control is-invalid" : "form-control";
        const showPasswordInputError = this.state.invalidPassword ? "form-control is-invalid" : "form-control";
        const showPasswordTextError = this.state.invalidPassword ? "text-danger display-block" : "d-none";
        const showSamePasswordTextError = this.state.samePassword ? "text-danger display-block" : "d-none";
        return (
            <div className={"wrapperContainer"}>
                <div className="innerContainer">
                    <h1 className={"header"}>Change Password</h1>
                    <form onSubmit={this.onSubmit}>
                        <div className={"input"}>
                            <i className={"fa fa-user"}/>
                            <input
                                className={showEmailInputError}
                                type="text"
                                placeholder={"Email"}
                                name={"email"}
                                onChange={this.handleChange}
                            />
                        </div>
                        <div className={"input"}>
                            <i className={"fa fa-key"}/>
                            <input
                                className={showKeyError}
                                type="text"
                                placeholder={"Key"}
                                name={"key"}
                                onChange={this.handleChange}
                            />
                        </div>

                        <div>
                            <div className={"input"}>
                                <i className={"fa fa-key"}/>
                                <input
                                    className={showPasswordInputError}
                                    type="password"
                                    name={"password"}
                                    onChange={this.handleChange}
                                />
                            </div>
                            <small className={showKeyTextError}>Wrong key, go to - <Link className="nav-link"
                                                                                         to={"/forgotpassword"}>Forgot
                                Password</Link>
                            </small>
                            <small className={showEmailTextError}>No such email in the system</small>
                            <small onClick={this.showModal}>click for password rules</small>
                            <small className={showPasswordTextError}>This is not a valid password, try again.</small>
                            <small className={showSamePasswordTextError}>You already used this password, try again</small>
                            <input type={"submit"} value={"Submit"} onClick={this.onSubmit}/>
                        </div>
                    </form>
                </div>
                <Modal show={this.state.show} handleClose={this.hideModal}>
                    <PasswordModal handleClose={this.hideModal}/>
                </Modal>
            </div>
        );
    }


}

export default ForgotChangePassword;