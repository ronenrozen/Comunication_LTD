import React, {Component} from "react";

export default class Button extends Component {

    render() {
        const {type,value, className, dataToggle, dataTarget,onClick} = this.props;
        if (dataTarget)
            return (
                <button type={type} className={className} data-target={dataTarget} onClick={onClick}>
                    {value}
                </button>
            );
        else if (dataToggle)
            return (
                <button type={type} className={className} data-toggle={dataToggle} onClick={onClick}>
                    {value}
                </button>
            );
        else if(dataTarget && dataToggle)
            return (
                <button type={type} className={className} data-toggle={dataToggle} data-target={dataTarget} onClick={onClick}>
                    {value}
                </button>
            );
        else
            return (
                <button type={type} className={className} onClick={onClick}>
                    {value}
                </button>
            );
    }
}