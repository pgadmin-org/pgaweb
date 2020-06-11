/* eslint-disable no-console */

const critical = require('critical');
const PATH = require('path');
const _FILES_ = [
  'base.html',
  'index.html',
  'action.html',
  'ad.html',
];
const removeFilePart = dirname => PATH.basename(dirname);
var optimize_html_path = PATH.resolve('./static/', 'optimize/');
var index_critical_file = PATH.join(optimize_html_path, 'index_critical.html');

const getLogger = require('webpack-log');
const log = getLogger({ name: 'webpack-batman' });

class ProcessAfterBuild {
  constructor(options) {
    this.options = options;
  }

  apply(compiler) {
    compiler.hooks.beforeRun.tap('ProcessAfterBuild', compiler => { //write a combination of base and index html file to static/optimize/index_critical.html for creating critical css

      const fs = require('fs');
      const glob = require('glob');

      if (!fs.existsSync(optimize_html_path)) {
        fs.mkdirSync(optimize_html_path);
      }

      if (fs.existsSync(index_critical_file)) {
        fs.unlinkSync(index_critical_file);
      }

      var files = glob('./pgaweb/templates/pgaweb/*.html', { sync: true });

      files.forEach((filename_with_path) => {

        let filename = removeFilePart(filename_with_path);

        var readStream;
        if (_FILES_.indexOf(filename) > -1) {

          var buffer;
          readStream = fs.createReadStream(filename_with_path, 'utf8');

          readStream.on('data', function (chunk) {
            buffer += chunk;
          }).on('end', function () {
            let index_critical_file = PATH.join(optimize_html_path, 'index_critical.html');
            fs.appendFileSync(index_critical_file, buffer);
          });
        }
      });
      log.info('Critical html snippet generated successfully..');
    }),
      compiler.hooks.done.tap('ProcessAfterBuild', stats => { //logic for creating critical css based on combination of base and index html
        const { path } = stats.compilation.options.output;
        var cssPath = PATH.join(path, 'assets/css/');

        critical.generate({
          base: '/',
          src: index_critical_file,
          target: {
            css: PATH.join(cssPath, 'main.css'),
            uncritical: PATH.join(cssPath, 'main_uncritical.css'),
          },
          width: 1300,
          height: 900,
          //Minify critical-path CSS when inlining
          minify: true,
          // Extract inlined styles from referenced stylesheets
          extract: true,
        });
        log.info('Critical css generated successfully..');
      });
  }
}

module.exports = ProcessAfterBuild;
