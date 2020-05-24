import React, {Component} from 'react';
import Button from '../Utils/Button'


class Customer extends Component {
    handleEdit = () => {
        const {edit} = this.props;
        edit(this.props)

    };

    render() {
        const {id, companyName, email, sector, packagePrice, packageSize} = this.props;


        return (
            <tr>
                <td>{id}</td>
                <td>{companyName}</td>
                <td>{email}</td>
                <td>{sector}</td>
                <td>{packagePrice}$</td>
                <td>{packageSize}G</td>
                <td>
                    <Button
                        type={"button"}
                        value={"Edit"}
                        className={"btn btn-primary btn-rounded"}
                        dataToggle={"modal"}
                        dataTarget={"#staticBackdrop"}
                        onClick={this.handleEdit}/>
                </td>
            </tr>
        );
    }
}


export default Customer;