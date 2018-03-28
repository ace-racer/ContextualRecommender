module.exports = function(grunt) {
  grunt.initConfig({
    less_formatter: {
      options: {
        files: {
          src: ['test/styles.less']
        }
      }
    }
  });
  grunt.loadTasks('tasks');
  grunt.registerTask('default', ['less_formatter']);
};
