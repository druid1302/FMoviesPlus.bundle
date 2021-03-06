// Usage: phantomjs fmovies.js <video_url>
// if that doesn't work try: phantomjs --ssl-protocol=any fmovies.js <video_page_url>
// Author: Coder Alpha
//

var separator = ' | ';
var page = require('webpage').create(),
  system = require('system'),
  id, match;

if(system.args.length < 2) {
  console.error('No URL provided');
  phantom.exit(1);
}

var page_url = system.args[1];

// thanks @Mello-Yello :)
page.onInitialized = function() {
  page.evaluate(function() {
    delete window._phantom;
    delete window.callPhantom;
	window.outerHeight = 1200;
	window.outerWidth = 1600;
  });
  var MAXIMUM_EXECUTION_TIME = 2 * 60 * 1000; // 1 min. thanks @Zablon :)
  setTimeout(function() {
	phantom.exit();
  }, MAXIMUM_EXECUTION_TIME);
};
page.settings.userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36";

// thanks @skidank (https://forums.plex.tv/discussion/comment/1582115/#Comment_1582115)
page.onError = function(msg, trace) {
	//console.log(msg);
}

page.open(page_url, function(status) {

	console.log(page.content);

});

page.onLoadFinished = function(status) {
	//console.log('Status: ' + status);
	phantom.exit();
};