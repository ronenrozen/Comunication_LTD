import React, {Component} from 'react';

class Option extends Component {
    constructor(props) {
        super(props);

        this.state = {
            value: ''
        }
    }

    handleChange = ({target}) => {
        this.setState({value: target.value})
    };


    render() {
        const {value, text} = this.props;
        return (
            <>
                <option onChange={this.handleChange} value={value}>{text}</option>
            </>
        );
    }
}

export default Option;