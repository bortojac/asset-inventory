import React from 'react';
import './exceptionTable.css';
import ReactTable from 'react-table';
import 'react-table/react-table.css';
import _ from 'lodash';

class ExceptionTable extends React.Component {

    static getDerivedStateFromProps(nextProps, prevState) {
        const exceptions = nextProps.json.map(
            (item) => ({
                day: item.day,
                asset: item.asset,
                sod: item.sod,
                transactions: item.transactions,
                eod: item.eod,
            })
        ).filter((item) => item.eod < 0)
        return {
            tableDat: exceptions
        }
    }
    constructor(props) {
        super(props);
        this.state = {
            tableDat: []
        }
    }

    render() {
        return (
            <ReactTable
                data={this.state.tableDat}
                columns={[
                    {
                        Header: "Transaction Failures",
                        columns: [
                            {
                                Header: "Day",
                                accessor: "day"
                            },
                            {
                                Header: "Asset",
                                accessor: "asset"
                            },
                            {
                                Header: "SoD Amount",
                                accessor: "sod"
                            },
                            {
                                Header: "Transactions",
                                accessor: "transactions"
                            },
                            {
                                Header: "EoD Amount",
                                accessor: "eod"
                            }
                        ]
                    }
                ]
                }
                defaultPageSize={5}
                className="-striped -highlight exceptionTable"
            />
        )
    }
}

export default ExceptionTable;