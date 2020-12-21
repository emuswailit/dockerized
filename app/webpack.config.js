var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        loader: "file-loader",
        options: {
          outputPath: "images",
        },
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },

      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
          // Compiles Sass to CSS
          "sass-loader",
        ],
      },
    ],
  },

  entry: path.join(__dirname, "staticfiles/src/js/index"),
  output: {
    path: path.join(__dirname, "staticfiles/dist"),
    filename: "[name]-[hash].js",
  },
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: "webpack-stats.json",
    }),
  ],
};
