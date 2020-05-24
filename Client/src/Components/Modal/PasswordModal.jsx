import React, {Component} from 'react';
import Button from "../Utils/Button";

class PasswordModal extends Component {
    render() {
        return (
            <>
                <div className={"container"}>
                    <div className={"modal-header"}>
                        <h5 className="modal-title">Password Rules</h5>
                    </div>
                </div>
                <div className={"modal-body"}>
                    <i className="fas fa-angle-right"/>The password must contain at least 1 lowercase alphabetical character<br/>
                    <i className="fas fa-angle-right"/>The password must contain at least 1 uppercase alphabetical character<br/>
                    <i className="fas fa-angle-right"/>The password must contain at least 1 numeric character<br/>
                    <i className="fas fa-angle-right"/>The password must contain at least one special character<br/>
                    <i className="fas fa-angle-right"/>The password must be ten characters or longer<br/>
                </div>
                <div className="modal-footer">
                    <Button
                        type={"button"}
                        value={"Close"}
                        className={"btn btn-secondary"}
                        onClick={this.props.handleClose}/>
                </div>
            </>
        );
    }
}

export default PasswordModal;