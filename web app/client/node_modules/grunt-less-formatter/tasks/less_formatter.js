var fs = require('fs'),
  q = require('q'),
  request = require('request'),
  cheerio = require('cheerio');
module.exports = function(grunt) {
  grunt.registerTask('less_formatter', 'The best Grunt plugin ever.', function() {
    var done = this.async();
    var format = function(f) {
      var defer = q.defer();
      console.log('Reading/formatting file "' + f + '"');
      request.post({
        url: 'http://www.calluna-software.com/Formatter/Css',
        form: {
          Source: fs.readFileSync(f)
        }
      }, function(error, resp, body) {
        var $ = cheerio.load(body);
        var formattedSrc = $('pre#result-container').text();
        // This formatter breaks LESS import statements. Unbreak.
        var re = new RegExp("url('.*');", 'g');
        formattedSrc = formattedSrc.replace(re, '');
        grunt.file.write(f, formattedSrc);
        grunt.log.writeln('File "' + f + '" formatted.');
      });
      return defer.promise;
    };
    var promises = [];
    this.options().files.src.forEach(function(f) {
      if (!grunt.file.exists(f)) {
        grunt.log.warn('Source file "' + f + '" not found.');
        return false;
      } else {
        promises.push(format(f));
      }
    });
    q.all(promises).then(done);
  });
};
