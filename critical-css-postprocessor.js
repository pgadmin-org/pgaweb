/* eslint-disable no-console */

// Critical is loaded lazily to avoid ESM top-level await issues
let critical = null;
const FS = require('fs');
const PATH = require('path');

/*
 * The templates whose markup, concatenated, stands in for a rendered page whilst
 * working out which CSS is above the fold. The order matters: base.html carries
 * the doctype, head and navbar, so it has to come first or the stand-in document
 * has content before its doctype.
 */
const _FILES_ = [
  'base.html',
  'index.html',
  'action.html',
  'ad.html',
];

const template_dir = PATH.resolve('./pgaweb/templates/pgaweb/');
const optimize_html_path = PATH.resolve('./static/', 'optimize/');
const index_critical_file = PATH.join(optimize_html_path, 'index_critical.html');

// Simple logger replacement for webpack-log
const log = {
  info: (msg) => console.log('[ProcessAfterBuild]', msg),
  warn: (msg) => console.warn('[ProcessAfterBuild]', msg),
  error: (msg) => console.error('[ProcessAfterBuild]', msg),
};

class ProcessAfterBuild {
  constructor(options) {
    this.options = options;
  }

  apply(compiler) {
    // Write a combination of the base and index templates to
    // static/optimize/index_critical.html, for critical to work from.
    compiler.hooks.beforeRun.tap('ProcessAfterBuild', () => {
      if (!FS.existsSync(optimize_html_path)) {
        FS.mkdirSync(optimize_html_path, { recursive: true });
      }

      /*
       * Read synchronously and in the declared order. This used to stream each
       * file and append it on the 'end' event, which meant three things: the
       * success message below was logged before any content had been written,
       * the order of the concatenated files was whatever glob returned
       * (alphabetical, so fragments landed ahead of base.html's doctype), and
       * the accumulator was declared without an initial value, so string
       * concatenation prefixed every file with the literal text "undefined".
       */
      const parts = [];
      const missing = [];

      _FILES_.forEach((filename) => {
        const filename_with_path = PATH.join(template_dir, filename);

        if (!FS.existsSync(filename_with_path)) {
          missing.push(filename);
          return;
        }

        parts.push(FS.readFileSync(filename_with_path, 'utf8'));
      });

      FS.writeFileSync(index_critical_file, parts.join('\n'));

      if (missing.length) {
        log.warn(`Templates missing from ${template_dir}, so the critical css ` +
                 `will be computed without them: ${missing.join(', ')}`);
      }

      log.info(`Critical html snippet generated from ${parts.length} of ` +
               `${_FILES_.length} templates..`);
    });

    // Generate the critical css from that combination.
    compiler.hooks.done.tapPromise('ProcessAfterBuild', async stats => {
      const { path } = stats.compilation.options.output;
      const cssPath = PATH.join(path, 'assets/css/');
      const uncriticalCss = PATH.join(cssPath, 'main_uncritical.css');

      try {
        // Lazy load critical to avoid ESM top-level await issues
        if (!critical) {
          critical = await import('critical');
          critical = critical.default || critical;
        }

        /*
         * This must be awaited. Without it the success message below was logged
         * unconditionally, whether or not anything had been generated, and a
         * failure arrived later as an unhandled rejection: Node aborted after
         * webpack had already reported the build good, which left a non-zero
         * exit status and skipped everything chained after webpack in the build
         * script, the gzip step included.
         */
        await critical.generate({
          base: '/',
          src: index_critical_file,
          target: {
            css: PATH.join(cssPath, 'main.css'),
            uncritical: uncriticalCss,
          },
          width: 1300,
          height: 900,
          // Extract inlined styles from referenced stylesheets
          extract: true,
        });

        log.info('Critical css generated successfully..');
      } catch (err) {
        /*
         * Not fatal. critical only rewrites main.css on success, so on failure
         * it is left as the complete stylesheet and the site renders correctly,
         * just with more blocking CSS than it needs. Fail loudly but let the
         * build finish, so that whatever is chained after webpack still runs.
         */
        log.warn('Critical css generation FAILED. main.css has been left as the ' +
                 'complete stylesheet, so the site will render correctly but ' +
                 'first paint will be slower than it should be.');
        log.warn(err && err.message ? err.message : String(err));

        /*
         * base.html loads the uncritical stylesheet asynchronously, so write an
         * empty one rather than leaving visitors a 404 for a file that no longer
         * has anything to say.
         */
        try {
          FS.mkdirSync(PATH.dirname(uncriticalCss), { recursive: true });
          FS.writeFileSync(uncriticalCss,
            '/* Critical css generation failed during the build, so main.css\n' +
            '   contains the complete stylesheet and there is nothing to defer. */\n');
        } catch (writeErr) {
          log.error(`Could not write ${uncriticalCss}: ${writeErr.message}`);
        }
      }
    });
  }
}

module.exports = ProcessAfterBuild;
