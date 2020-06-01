import React, {Component} from 'react';
import './ChangePassword.css'
import Modal from "./Modal/Modal";
import PasswordModal from "./Modal/PasswordModal";
import userAxios from "./Axios/userAxios";
import https from 'https';
const agent = new https.Agent({
    rejectUnauthorized: false
});
class ChangePassword extends Component {
    constructor(props) {
        super(props);
        this.state = {
            oldPassword: "",
            newPassword: "",
            invalidOldPassword: false,
            invalidNewPassword: false,
            newPasswordSameAsOld: false,
            successfulUpdate: false,
            redirect: false,
            show: false
        };
    }

    showModal = () => {
        this.setState({show: true});
    };

    hideModal = () => {
        this.setState({show: false});
    };


    inputChange = ({target: {name, value}}) => {
        this.setState({
            [name]: value,
        });
    };

    onSubmit = async (e) => {
        e.preventDefault();
        this.setState({
            invalidOldPassword: false,
            invalidNewPassword: false,
            newPasswordSameAsOld: false,
            successfulUpdate: false
        });
        let data = {
            old_password: this.state.oldPassword,
            new_password: this.state.newPassword,
        };
        try {
            await userAxios.put(`/change_password/${JSON.parse(sessionStorage.getItem('user'))['id']}`, data,
                {
                    headers: {
                        'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                        'Content-Type': 'application/json'
                    },
                    httpsAgent: agent
                });
            this.setState({successfulUpdate: true})
        } catch (error) {
            if (error.response && error.response.status === 400) {
                this.setState({invalidOldPassword: true})
            } else if (error.response && error.response.status === 401) {
                this.setState({invalidNewPassword: true})
            } else if (error.response && error.response.status === 403) {
                this.setState({newPasswordSameAsOld: true})
            }
        }
    };

    render() {
        const showOldPasswordTextError = this.state.invalidOldPassword ? "text-danger d-block" : "d-none";
        const showOldPasswordInputError = this.state.invalidOldPassword ? "form-control is-invalid" : "form-control";
        const showNewPasswordTextError = this.state.invalidNewPassword ? "text-danger d-block" : "d-none";
        const showNewPasswordInputError = this.state.invalidNewPassword ? "form-control is-invalid" : "form-control";
        const showNewPasswordSameAsOldTextError = this.state.newPasswordSameAsOld ? "text-danger d-block" : "d-none";
        const successfulUpdate = this.state.successfulUpdate ? "text-success d-block" : "d-none";
        return (
            <div className={"container set-width"}>
                <h1 className={"mb-4"}>Change Password</h1>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>Old Password</label>
                        <input
                            className={showOldPasswordInputError}
                            type="password"
                            name="oldPassword"
                            onChange={this.inputChange}
                        />
                        <label>New Password</label>
                        <input
                            className={showNewPasswordInputError}
                            type="password"
                            name="newPassword"
                            onChange={this.inputChange}
                        />
                        <small onClick={this.showModal}>click for password rules</small>
                        <button type="submit" className="btn d-block  btn-primary">Submit</button>
                        <small className={showOldPasswordTextError}>The old password didn't match, try again</small>
                        <small className={showNewPasswordTextError}>The new password didn't match, try again</small>
                        <small className={showNewPasswordSameAsOldTextError}>The new password matched your latest 3
                            passwords</small>
                        <small className={successfulUpdate}>Your new password saved in the DB</small>
                    </div>
                </form>
                <Modal show={this.state.show} handleClose={this.hideModal}>
                    <PasswordModal handleClose={this.hideModal}/>
                </Modal>
            </div>
        );
    }
}

export default ChangePassword;