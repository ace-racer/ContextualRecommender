# grunt-combine-js

> combine js modules into one file

## Getting Started
This plugin requires Grunt `~0.4.0`

If you haven't used [Grunt](http://gruntjs.com/) before, be sure to check out the [Getting Started](http://gruntjs.com/getting-started) guide, as it explains how to create a [Gruntfile](http://gruntjs.com/sample-gruntfile) as well as install and use Grunt plugins. Once you're familiar with that process, you may install this plugin with this command:

```shell
npm install grunt-combine-js --save-dev
```

Once the plugin has been installed, it may be enabled inside your Gruntfile with this line of JavaScript:

```js
grunt.loadNpmTasks('grunt-combine-js');
```

## The "combine_js" task

### Overview
In your project's Gruntfile, add a section named `combine_js` to the data object passed into `grunt.initConfig()`.

The idea behind this plugin is that you can pick and choose from your javascript modules to combine them into one file with the name and destination of your choosing.

In the grunt file you will have 4 options:
1. "src" - this is the path to the json build file which will contain the JS module paths and the destination name and destination folder.
2. "combine_folder" - you may have a folder that contains scripts you also want to include in your final js file, for plugins perhaps.
3. "additional_files" - literally just extra scripts you would like included, so this could be scripts that are to be included in every js file build, e.g. a pub/sub script.
4. "base_files" - this will allow you to set some predefined files to include in every build, these will be inserted before the 'src' files.

In the JSON file you use for "src" there are the following options:
1. "modules" - an array of file paths to the files you want to combine *REQUIRED
2. "dest_name" - what the file will be called when built *REQUIRED
3. "dest_path" - where the built file should go *REQUIRED
4. "useBase" - by default this is true, if you don't want to use a set of base files then set to false

The order these scripts will be combined in the final file is:
1. additional_files
2. combine_folder
3. base_files
4. src

### Usage Examples

```js
grunt.initConfig({
  combine_js: {
    files: [{
      src: '/path/to/json/file/build.json',
      combine_folder: '/path/to/directory/where/all/files/will/be/combined/',
      additional_files: [
        '/path/to/extra/scripts/file-a.js',
        '/another/path/to/extra/scripts/file-b.js'
      ],
      base_files: [
        'path/to/file.js',
        'path/to/another/file.js'
      ]
    }]
  },
});
```

### Example JSON build file

```js
[
    {
        "modules": [
            "src/assets/scripts/modules/file-a.js",
            "src/assets/scripts/modules/file-b.js"
        ],
        "dest_name": "test_a.js",
        "dest_path": "dist/_scripts/",
        "useBase": false
    },
    {
        "modules": [
            "src/assets/scripts/modules/file-c.js",
            "src/assets/scripts/modules/file-d.js"
        ],
        "dest_name": "test_b.js",
        "dest_path": "dist/_scripts/"
    }
]
```

## Contributing
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests for any new or changed functionality. Lint and test your code using [Grunt](http://gruntjs.com/).

## Release History
_(Nothing yet)_
