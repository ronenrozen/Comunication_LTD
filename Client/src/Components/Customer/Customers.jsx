import React, {Component} from 'react'
import Customer from './Customer'
import AddCustomer from './AddCustomer'
import customerAxios from "./customerAxios";
import Modal from '../Modal/Modal'
import EditCustomer from "./EditCustomer";
import {Redirect} from "react-router-dom";
import axios from "axios";
import './Customers.css';
import packageAxios from "../Axios/packageAxios";
import https from 'https';

const agent = new https.Agent({
    rejectUnauthorized: false
});

class Customers extends Component {

    constructor(props) {
        super(props);
        this.state = {
            customersList: [],
            packageList: [],
            show: false,
            currentCustomer: {},
            lastAddedCustomer: {},
            packageIntId: 1
        };
    }

    CancelToken = axios.CancelToken;
    source = this.CancelToken.source();

    componentDidMount = async () => {
        try {
            const {data} = await customerAxios.get(`/getall`, {
                cancelToken: this.source.token,
                headers: {
                    'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                },
                httpsAgent: agent
            });
            this.setState({customersList: data}, () => console.log(this.state));
            const response = await packageAxios.get(`/getall`, {
                cancelToken: this.source.token,
                headers: {
                    'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                },
                httpsAgent: agent
            });
            this.setState({packageList: response.data})
        } catch (error) {
            console.log('error on retrieving all Customers', error);
        }
    };

    componentWillUnmount() {
        this.source.cancel("Operation canceled by the user.");
    }

    showModal = () => {
        this.setState({show: true});
    };

    hideModal = () => {
        this.setState({show: false, currentCustomer: {}}, () => this.updateTable());
    };

    createTable = (customer) => {
        return (<Customer
            key={customer.id}
            id={customer.id}
            companyName={customer.customer_name}
            email={customer.email}
            sector={customer.sector}
            packageId={customer.package_id}
            packagePrice={customer.package_price}
            packageSize={customer.package_size}
            edit={this.handleEdit}/>)
    };

    handleEdit = (customer) => {
        this.setState({currentCustomer: customer}, () => console.log("handleEei", this.state));
        this.showModal()
    };

    handleAdd = (data) => {
        this.setState({lastAddedCustomer: data}, () => this.updateTable());
    };

    updateTable = async () => {
        try {
            const {data} = await customerAxios.get(`/getall`, {
                headers: {
                    'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                },
                httpsAgent: agent
            });
            this.setState({customersList: data})
        } catch (error) {
            console.log('error on delete', error);
        }
    };

    handleDelete = async () => {
        try {
            const {status} = await customerAxios.delete(`/delete/${this.state.currentCustomer.id}`, {
                headers: {
                    'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                },
                httpsAgent: agent
            });
            if (status) {
                this.hideModal()
            } else {
                this.setState({status: 500});
            }
        } catch (error) {
            console.log('error on delete', error);
        }
    };

    handleCurrentCustomer = (e) => {
        this.setState({
            currentCustomer: {
                ...this.state.currentCustomer,
                [e.target.name]: e.target.value
            }
        }, () => console.log(this.state.currentCustomer));
        if (e.target.name === "packageId") {
            this.changeToPackageId(e.target.value)
        }
    };

    changeToPackageId = (targetValue) => {
        let packId;
        for (let [key, value] of this.state.packageList.entries()) {
            console.log(key);
            if (value["package_name"] === targetValue)
                packId = value["package_id"];
        }

        this.setState({packageIntId: packId})
    };

    handleUpdate = async (e) => {
        e.preventDefault();
        let currentCustomer = this.state.currentCustomer;
        currentCustomer.packageId = this.state.packageIntId;
        try {
            const {status} = await customerAxios.put(`/update/${this.state.currentCustomer.id}`, currentCustomer, {
                cancelToken: this.source.token,
                headers: {
                    'Authorization': `Bearer ${JSON.parse(sessionStorage.getItem('user'))['access_token']}`,
                },
                httpsAgent: agent
            });
            if (status) {
                this.hideModal()
            } else {
                this.setState({status: 500});
            }
        } catch (error) {
            console.log('error on delete', error);
        }
    };


    render() {
        if (!sessionStorage.getItem('user')) {
            return <Redirect to={'./'}/>
        }
        return (
            <div>
                <AddCustomer handleAdd={this.handleAdd} packages={this.state.packageList}/>
                <table className="container table table-striped text-center table-dark mt-5">
                    <thead className="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Sector</th>
                        <th>Package Price</th>
                        <th>Package Size</th>
                        <th>Edit</th>
                    </tr>
                    </thead>
                    {this.state.customersList &&
                    <tbody>{this.state.customersList.map(customer => this.createTable(customer))}</tbody>}
                </table>
                <Modal show={this.state.show} handleClose={this.hideModal}>
                    <EditCustomer handleClose={this.hideModal} handleCurrentCustomer={this.handleCurrentCustomer}
                                  customer={this.state.currentCustomer} packages={this.state.packageList}
                                  delete={this.handleDelete} update={this.handleUpdate}/>
                </Modal>
            </div>
        )
    }
}

export default Customers