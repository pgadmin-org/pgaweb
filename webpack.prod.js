/* eslint-disable no-undef */
var path = require('path');
var MiniCssExtractPlugin = require('mini-css-extract-plugin');
var autoprefixer = require('autoprefixer');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
var webpack = require('webpack');
var CopyPlugin = require('copy-webpack-plugin');
var ImageminPlugin = require('imagemin-webpack-plugin').default;

var ProcessAfterBuild = require('./critical-css-postprocessor');

// Resolved rather than assumed at ./node_modules, so the copy below works in a
// worktree with a symlinked node_modules as well as in a plain checkout. The
// package's exports map only exposes the unminified builds, so the directory is
// resolved through the main entry and the minified filenames joined onto it.
const photoswipeDist = path.dirname(require.resolve('photoswipe'));

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
        postcssOptions: {
          plugins: [autoprefixer()],
        },
      },
    },
    {
      loader: 'resolve-url-loader',
    },
    {
      loader: 'sass-loader',
      options: {
        sourceMap: true,
      },
    },
  ],
};

var plugins = [
  new MiniCssExtractPlugin({
    filename: 'assets/css/[name].css',
    ignoreOrder: false,
  }),
  new CopyPlugin({
    patterns: [
      {
        from: './static/img/*.*',
        to: 'assets/img/[name][ext]',
      },
      {
        from: './static/img/screenshots',
        to: 'assets/img/screenshots',
      },
      // PhotoSwipe is loaded as ES modules by the gallery, so it is copied
      // rather than bundled. It used to come from a CDN, unpinned. Only the
      // three files the gallery imports are taken: dist also ships UMD builds,
      // type definitions and source maps.
      {
        from: path.join(photoswipeDist, 'photoswipe.esm.min.js'),
        to: 'photoswipe/[name][ext]',
      },
      {
        from: path.join(photoswipeDist, 'photoswipe-lightbox.esm.min.js'),
        to: 'photoswipe/[name][ext]',
      },
      {
        from: path.join(photoswipeDist, 'photoswipe.css'),
        to: 'photoswipe/[name][ext]',
      },
    ],
  }),
  new ImageminPlugin(
    {
      pngquant: ({ quality: '50' }),
      jpegtran: ({ quality: '50' }),
    },
  ),
  new CleanWebpackPlugin(),
];

module.exports = (env, argv) => {
  const isProductionMode = argv.mode === 'production';
  const isOptimizeMode = (argv.optimize === 'false') ? false : true;

  isOptimizeMode ? plugins.push(new ProcessAfterBuild()) : false;
  isProductionMode ?  plugins.push(new webpack.SourceMapDevToolPlugin({ filename: '[file].map[query]', exclude: ['vendor.js'] })) : false;

  return {
    context: __dirname,
    mode: env.NODE_ENV,
    entry: {
      'webp': './static/js/webp.js',
      'main': './static/js/index.js',
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
              plugins: ['@babel/plugin-transform-runtime'],
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
    plugins: plugins,
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
  };
};
