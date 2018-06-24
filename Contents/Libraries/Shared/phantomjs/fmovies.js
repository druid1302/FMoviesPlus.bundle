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
	window.innerHeight = 1200; 
	window.innerWidth = 1600;
  });
};
page.settings.userAgent = "mozilla/5.0 (windows nt 6.1; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/67.0.3396.87 safari/537.36";

// thanks @skidank (https://forums.plex.tv/discussion/comment/1582115/#Comment_1582115)
page.onError = function(msg, trace) {
	//console.log(msg);
}

page.open(page_url, function(status) {

	//page.includeJs('https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js', function() {
		var info = page.evaluate(function() {

			function GetIframeLink() {
				var elms = document.getElementsByTagName("iframe");
				for (var j = 0; j < elms.length; j++) {
					if (elms[j].src != null && elms[j].src.length > 0) {
						var txt = elms[j].src;
						return txt;
					}
				}
				return null;
			};
			
			var spanID = GetIframeLink();
			
			if (spanID == null || spanID.length == 0 || spanID.indexOf('Exception') > -1) {
				return {
					decoded_id: spanID
				};
			}
			return {
				decoded_id: spanID
			};
		  });

		var myInfo = info.decoded_id;
		if (myInfo == null || myInfo.length == 0 || myInfo.indexOf('Exception') > -1) {
			console.log('ERROR: ID not found. ' + myInfo);
		} else {
			var url = info.decoded_id;
			console.log(url);
		}
	//});
});

page.onLoadFinished = function(status) {
	//console.log('Status: ' + status);
	phantom.exit();
};