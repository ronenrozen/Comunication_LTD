import React, {Component} from 'react'
import userAxios from './customerAxios'
import Input from '../Utils/Input'
import Button from "../Utils/Button";
import https from 'https';

const agent = new https.Agent({
    rejectUnauthorized: false
});

export default class AddCustomer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: "",
            email: "",
            sector: "",
            packageStr: "",
            packageIdInt: 1
        }
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
        if (e.target.name === "packageStr") {
            this.changeToPackageId(e.target.value)
        }
    };

    changeToPackageId = (targetValue) => {
        let packId;
        for (let [key, value] of this.props.packages.entries()) {
            console.log(key);
            if (value["package_name"] === targetValue)
                packId = value["package_id"];
        }

        this.setState({packageIdInt: packId}, () => console.log("statepackage", this.state))
    };

    handleAdd = async () => {
        let data = {
            name: this.state.name,
            email: this.state.email,
            sector: this.state.sector,
            packageId: this.state.packageIdInt
        };
        console.log("data", data);
        try {
            await userAxios.post('addcustomer', data,
                {
                    headers: {
                        'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                        'Content-Type': 'application/json'
                    },
                    httpsAgent: agent
                });
            this.props.handleAdd(data);
        } catch (error) {
            console.log('error on add user', error);
        }
    };


    render() {
        return (
            <div className='container'>
                <h1 className="text-center mb-3">Add New Customer</h1>
                <form className="container form-inline">
                    <Input
                        label="Customer Name"
                        type="text"
                        name="name"
                        change={this.handleChange}
                    />
                    <Input
                        label="Email"
                        type="email"
                        name="email"
                        change={this.handleChange}
                    />
                    <Input
                        label="Sector"
                        type="text"
                        name="sector"
                        change={this.handleChange}
                    />
                    <label>Package</label>
                    <select name={"packageStr"} onChange={this.handleChange}
                            value={this.state.packageStr ? this.state.packageStr : "3"}>
                        {this.props.packages.map(item => (
                            <option key={item.package_id} value={item.package_name}>
                                {item.package_name}
                            </option>
                        ))}
                    </select>
                    <Button
                        type={"button"}
                        onClick={this.handleAdd}
                        value={"Add"}
                        className={"btn btn-info btn-rounded btn-sm mr-2 ml-2 z-depth-0 my-4 waves-effect"}
                    />
                </form>
            </div>
        )
    }
}
