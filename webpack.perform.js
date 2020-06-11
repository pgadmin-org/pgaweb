/* eslint-disable no-undef */
var path = require('path');
var MiniCssExtractPlugin = require('mini-css-extract-plugin');
var autoprefixer = require('autoprefixer');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
var webpack = require('webpack');
var CopyPlugin = require('copy-webpack-plugin');
var ImageminPlugin = require('imagemin-webpack-plugin').default;

var ProcessAfterBuild = require('./critical-css-postprocessor');

const SpeedMeasurePlugin = require('speed-measure-webpack-plugin');
const smp = new SpeedMeasurePlugin();

const sourceDir = __dirname + '/static/';
const outputPath = __dirname + '/static/COMPILED/';

const newStyleRule = {
  test: /\.(sa|sc|c)ss$/,
  use: [
    MiniCssExtractPlugin.loader,
    {
      loader: 'css-loader',
      options: {
        url: false,
        sourceMap: false,
      },
    },
    {
      loader: 'postcss-loader',
      options: {
        plugins: () => [autoprefixer()],
      },
    },
    {
      loader: 'resolve-url-loader',
    },
    {
      loader: 'sass-loader',
      options: {
        sourceMap: false,
      },
    },
  ],
};

const webpackConfig = smp.wrap({

  context: __dirname,
  mode: 'production',
  entry: {
    'webp': ['@babel/polyfill', './static/js/webp.js'],
    'main': './static/js/index.js',
    'fotoramajs': './node_modules/fotorama/fotorama.js',
    'fotorama': './node_modules/fotorama/fotorama.css',
    'banner': './static/js/banner.js',
    'styleguide': './pgaweb/static/css/styleguide.scss',
  },
  output: {
    path: outputPath,
    filename: '[name].js',
    libraryExport: 'default',
  },
  devtool: false,
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: [
              [
                '@babel/plugin-transform-async-to-generator',
                {
                  module: 'bluebird',
                  method: 'coroutine',
                },
              ],
            ],
          },
        },
      },
      newStyleRule,
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        include: [/node_modules/, path.join(sourceDir, '/assets/img')],
        loader: 'file-loader',
        options: {
          name: 'assets/css/[name].[ext]',
          limit: 10000,
        },
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf|png)?$/,
        include: [
          /node_modules/,
          path.join(sourceDir, '/assets/css/'),
          path.join(sourceDir, '/assets/fonts/'),
        ],
        loader: 'file-loader',
        options: {
          limit: 1000,
          useRelativePath: true,
          name: 'assets/css/[name].[ext]',
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.css', '.less', '.json'],
    modules: ['./node_modules'],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'assets/css/[name].css',
      ignoreOrder: false,
    }),
    new webpack.SourceMapDevToolPlugin({
      filename: '[file].map[query]',
      exclude: ['vendor.js'],
    }),
    new webpack.ProvidePlugin({
      $: ['jquery', 'jQuery'],
      jQuery: 'jquery',
    }),
    new CopyPlugin([
      {
        from: './static/img/*.*',
        to: 'assets/img',
        flatten: true,
      },
      {
        from: './static/img/screenshots',
        to: 'assets/img/screenshots',
        flatten: false,
      },
    ]),
    new ImageminPlugin(
      {
        pngquant: ({ quality: '50' }),
        jpegtran: ({ quality: '50' }),
      },
    ),
    new ProcessAfterBuild(),
    new CleanWebpackPlugin(),
  ],
  performance: {
    maxEntrypointSize: 1024000,
    maxAssetSize: 1024000,
    hints: 'warning',
  },
  stats: {
    children: false,
    assets: false,
    warnings: false,
  },
});

module.exports = (env, argv) => {

  // const isProductionMode = argv.mode === 'production';
  //   // const ifProd = (x) => isProductionMode && x;
  return webpackConfig;
};
