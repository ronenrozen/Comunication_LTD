import React, {Component} from 'react';

export default class Input extends Component {

    render() {
        const {label, type, name,value,tooltip} = this.props;
        return (
            <div className="form-group">
                <label>{label}</label>
                <input type={type} disabled={this.props.disabled} className="form-control rounded" name={name} onChange={this.props.change}
                       value={value} title={tooltip}/>
            </div>
        );
    };
}