const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: "./src/index.js",
    devtool: 'source-map',
    mode: "development",
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'bundle.js'//,
        //publicPath: '/'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['es2015', 'react']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    'file-loader'
                ]
            }
        ]
    }
};