var gulp = require('gulp');
var gulpif = require('gulp-if');
var changed = require('gulp-changed');
var tinypng = require('gulp-tinypng');

gulp.task('images', function() {
    return gulp.src("assets/res/*")
        .pipe(changed('assets/images'))
        .pipe(gulpif(/.*\.png$/, tinypng('9kl3nT2f8qC-AaApBVXDeQt-37ArLMNs')))
        .pipe(gulp.dest('assets/images/'));
});
