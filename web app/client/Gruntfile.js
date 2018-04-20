module.exports = function (grunt) {
    // Project configuration.
    grunt.initConfig({
        jade: {
            compile: {
                options: {
                    pretty: true
                },
                files: {
                    'assets/main.html': 'source/jade/main.jade',
                    'assets/recommended.html': 'source/jade/recommended.jade',
                    'components/cards/html/stream-card.html': 'components/cards/jade/stream-card.jade',
                    'components/cards/html/reco-stream-card.html': 'components/cards/jade/reco-stream-card.jade',
                    'components/related-stream-card/html/related-card.html': 'components/related-stream-card/jade/related-card.jade',
                    'components/template/html/temp.html': 'components/template/jade/temp.jade',
                    'components/template/html/related-temp.html': 'components/template/jade/related-temp.jade'
                }
            }
        },
        less: {
            development: {
                options: {
                    compress: false,
                    yuicompress: false,
                    optimization: 2
                },
                files: {
                    "assets/css/styles.css": "source/less/styles.less"
                    // destination file and source file
                }
            }
        },
        jshint: {
            all: ['Gruntfile.js', 'js/*.js']
        },
        watch: {
            grunt: {
                files: ['Gruntfile.js']
            },
            options: {
                livereload: true
            },
            config: {
                files: ['Gruntfile.js'],
                options: {
                    reload: true
                }
            },
            jade: {
                files: [
                    'components/**/**/*.jade',
                    'source/jade/*.jade',
                    'assets/js/*js'
                ],
                tasks: ['jade']
            },
            styles: {
                files: ['less/*.less',
                    'components/**/**/*.less',
                    'source/less/*.less'
                ], // which files to watch
                tasks: ['less']
                //,
                // options: {
                //     nospawn: true
                // }
            },
            jshint: {
                files: ['js/*.js'], // which files to watch
                tasks: ['jshint']

            }
        },
        serve: {
            options: {
                port: 9000,
                path: 'assets/main.html'
            }
        },
        open: {
            build: {
                path: 'http://127.0.0.1:9000/assets/main.html'
            }
        }
    });
    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jade');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-serve');
    grunt.loadNpmTasks('grunt-open');
    //grunt.registerTask('default', 'watch less and jade', ['jade', 'less', 'watch', 'jshint']);
    grunt.registerTask('default', ['jade', 'less', 'jshint', 'serve', 'open']);
};