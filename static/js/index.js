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

// Track Outbound Link Clicks
(function trackOutbounds() {

    let hitCallbackHandler = function (url, win) {
        if (win) {
            window.open(url, win);
        } else {
            window.location.href = url;
        }
    };

    let addEvent = function (el, eventName, handler) {

        if (el.addEventListener) {
            el.addEventListener(eventName, handler);
        } else {
            el.attachEvent('on' + eventName, function () {
                handler.call(el);
            });
        }
    }

    if (document.getElementsByTagName) {
        let el = document.getElementsByTagName('a');
        let getDomain = document.domain.split('.').reverse()[1] + '.' + document.domain.split('.').reverse()[0];

        // Look thru each a element
        for (let i = 0; i < el.length; i++) {

            // Extract it's href attribute
            let href = (typeof (el[i].getAttribute('href')) == 'string') ? el[i].getAttribute('href') : '';

            // Query the href for the top level domain (xxxxx.com)
            let myDomain = href.match(getDomain);

            // If link is outbound and is not to this domain
            if ((href.match(/^(https?:|\/\/)/i) && !myDomain) || href.match(/^mailto\:/i)) {

                // Add an event to click
                addEvent(el[i], 'click', function (e) {
                    let url = this.getAttribute('href'),
                        win = (typeof (this.getAttribute('target')) == 'string') ? this.getAttribute('target') : '';

                    console.log("add event", url);
                    // Log even to Analytics, once done, go to the link
                    ga('send', 'event', 'outbound', 'click', url,
                        {'hitCallback': hitCallbackHandler(url, win)},
                        {'nonInteraction': 1}
                    );

                    e.preventDefault();
                });
            }
        }
    }
})();
