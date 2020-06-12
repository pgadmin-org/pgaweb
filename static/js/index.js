import 'popper.js';
import $ from 'jquery';
window.jQuery = $;
window.$ = $;

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';

import '../../pgaweb/static/css/pgaweb.scss';

import { library, dom } from '@fortawesome/fontawesome-svg-core';
import { faLaptop, faDownload, faInfo, faBook, faQuestionCircle, faDesktop, faBug, faSearch } from '@fortawesome/free-solid-svg-icons';
import { faWindows, faApple, faDocker, faUbuntu, faPython, faRedhat } from '@fortawesome/free-brands-svg-icons';
import { faFileArchive } from '@fortawesome/free-solid-svg-icons';

library.add(faLaptop, faDownload, faInfo, faBook, faQuestionCircle, faDesktop, faBug, faSearch, faWindows, faApple, faDocker, faFileArchive, faUbuntu, faPython, faRedhat);
dom.watch();

//Do not delete
//The HTML5 Shiv enables use of HTML5 sectioning elements in legacy Internet Explorer and provides basic HTML5 styling
//for Internet Explorer 6-9, Safari 4.x (and iPhone 3.x), and Firefox 3.x.
//import 'html5shiv/dist/html5shiv.js'
//import 'respond.js/src/respond.js' //A fast & lightweight polyfill for min/max-width CSS3 Media Queries (for IE 6-8, and more)

function importAll(r) {
  return r.keys().map(r);
}

importAll(require.context('fotorama/', false, /\.(png|jpe?g|svg)$/));
importAll(require.context('@fortawesome/fontawesome-free/webfonts/', false, /\.(eot|svg|ttf|woff|woff2|)$/));
