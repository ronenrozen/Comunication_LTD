import React, {Component} from 'react'
import Button from "../Utils/Button";
import Input from "../Utils/Input";


export default class EditCustomer extends Component {

    render() {
        const {companyName, email, sector} = this.props.customer;
        return (
            <>
                <div className={"container"}>
                    <div className={"modal-header"}>
                        <h5 className="modal-title">Edit User</h5>
                    </div>
                    <form onSubmit={this.props.update}>
                        <Input
                            label="Customer Name"
                            type="text"
                            name="companyName"
                            value = {companyName ? companyName:''}
                            change={this.props.handleCurrentCustomer}
                        />
                        <Input
                            label="Email"
                            type="email"
                            name="email"
                            value = {email ? email: ''}
                            change={this.props.handleCurrentCustomer}
                        />
                        <Input
                            label="Sector"
                            type="text"
                            name="sector"
                            value = {sector ? sector:''}
                            change={this.props.handleCurrentCustomer}
                        />
                        <label>Package</label>
                        <select onChange={this.props.handleCurrentCustomer} name={'packageId'}>
                            {this.props.packages.map(item => (
                                <option key={item.package_id} value={item.package_name}>
                                    {item.package_name}
                                </option>
                            ))}
                        </select>
                    </form>
                </div>
                <div className="modal-footer">
                    <Button
                        type={"button"}
                        value={"Close"}
                        className={"btn btn-secondary"}
                        onClick={this.props.handleClose}/>
                    <Button
                        type={"button"}
                        value={"Delete"}
                        className={"btn btn-danger"}
                        onClick={this.props.delete}/>
                    <Button
                        type={"button"}
                        value={"Update"}
                        className={"btn btn-primary"}
                        onClick={this.props.update}/>
                </div>
            </>
        );
    }
}




