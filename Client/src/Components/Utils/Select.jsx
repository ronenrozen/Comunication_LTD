import React, {Component} from "react";
import Option from "./Option";

class Select extends Component {

    addOption = (option, i) => {
        return <Option
            key={i}
            value={option["key"]}
            text={option["value"]}/>
    };

    render() {
        const {label, options, name, defaultValue, className} = this.props;
        return (
            <div className="form-group">
                <label>{label}</label>
                <select className={className} name={name} onChange={this.props.onChange} value={defaultValue}>
                    {this.props.options && options.map((option, i) => this.addOption(option, i))}
                </select>
            </div>
        );
    };


}

export default Select;