import React from 'react';
import './table.css';
import ReactTable from 'react-table';
import 'react-table/react-table.css';
import _ from 'lodash';

class PnlTable extends React.Component {

    static getDerivedStateFromProps(nextProps, prevState) {
        return {
            tableDat: nextProps.json.map((item) => ({
                day: item.day,
                asset: item.asset,
                selfPrice: item.selfPrice,
                avgPrice: item.avgPrice,
                pnlPer: item.pnlPer,
                pnl: item.pnl,
            }))
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
                        Header: "Profit and Loss Table",
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
                                Header: "Self Price",
                                accessor: "selfPrice"
                            },
                            {
                                Header: "Avg Price",
                                accessor: "avgPrice"
                            },
                            {
                                Header: "Marginal PnL",
                                accessor: "pnlPer"
                            },
                            {
                                Header: "PnL",
                                accessor: "pnl"
                            }
                        ]
                    }
                ]
                }
                defaultPageSize={5}
                className="-striped -highlight"
            />
        )
    }
}

export default PnlTable;