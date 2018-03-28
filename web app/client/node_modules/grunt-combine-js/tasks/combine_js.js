/*
 * grunt-combine-js
 * https://github.com/grumpydev22/grunt-combine-js
 *
 * Copyright (c) 2016 Andy Blackledge
 * Licensed under the MIT license.
 */

'use strict';

var fs = require('fs');
module.exports = function(grunt) {

    grunt.registerMultiTask('combine_js', 'combine js modules into one file', function() {
        // Merge task-specific and/or target-specific options with these defaults.
        var options = this.options({
            punctuation: '.',
            separator: ', '
        });

        var done = this.async();
        var plugins = [];
        var jsonSrc = this.data[0].src;
        var folder = this.data[0].combine_folder;
        var additionalScripts = this.data[0].additional_files;
        var finalScripts = this.data[0].final_files;
        var baseFiles = this.data[0].base_files;
        var pluginsArray = [];

        var modules = function () {

            jsonSrc = grunt.file.readJSON(jsonSrc);
            var jsonSrcLength = jsonSrc.length;

            jsonSrc.forEach(function(item, index) {
                var src = item.modules;
                var destFolder = item.dest_path;
                var destName = item.dest_name;
                var includeBase = true;

                if (typeof item.useBase !== 'undefined') {
                    includeBase = item.useBase;
                }

                if (!destFolder || !destName) {
                    console.log('Grunt Combine JS: No destination folder or no destination name');
                    return;
                }

                if (baseFiles && includeBase) {
                    baseFiles.reverse();
                    baseFiles.map(function (path) {
                        src.unshift(path);
                    });
                }

                if (pluginsArray) {
                    pluginsArray.reverse();
                    pluginsArray.map(function (path) {
                        var pathEnd = path.lastIndexOf('.');
                        var fileExtension = path.substring(pathEnd + 1);
                        fileExtension = fileExtension.toLowerCase();
                        if (fileExtension && typeof fileExtension !== 'undefined' && fileExtension === 'js') {
                            src.unshift(path);
                        }
                        //src.unshift(path);
                    });
                }

                if (additionalScripts) {
                    additionalScripts.reverse();
                    additionalScripts.map(function (path) {
                        src.unshift(path);
                    });
                }

                // FINAL FILES
                // -----------
                // Places provided file(s) at the end of the 
                // generated script file
                if (finalScripts) {
                    finalScripts.reverse();
                    finalScripts.map(function (path) {
                        src.push(path);
                    });
                }


                var paths = src.map(function (path) {
                    var src = grunt.file.read(path);
                    src = grunt.template.process(src, options.process);
                    return src;
                }).join('');

                grunt.file.write(destFolder + destName, paths);
                console.log('Created file: ' + destName);

                if (index === (jsonSrcLength - 1)) {
                    console.log('grunt combine js END');
                    done();
                }
            });
        }

        if (folder) {
            fs.readdir(folder, function (err, files) {
                if (!err) {
                } else {
                    throw err;
                }

                plugins = files;
                pluginsArray = plugins.map(function (path) {
                    path = folder + path;
                    return path;
                });

                modules(pluginsArray);
            });
        } else {
            modules();
        }
    });
};
