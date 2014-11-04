var gulp = require('gulp');
var gulpif = require('gulp-if');
var changed = require('gulp-changed');
var tinypng = require('gulp-tinypng');
var fs = require('fs');
var less = require('gulp-less');
var merge = require('merge-stream');
var streamify = require('gulp-streamify')
var uglify = require('gulp-uglify');
var browserify = require('browserify');
var source = require('vinyl-source-stream')
var developing = process.env.NODE_ENV === 'development';

try {
    var notify = require('display-notification');
} catch (e) {
    var notify = function() {};
}

function browserifyStream(entry, filename) {
    var b = browserify(entry);

    b.transform({
        global: true
    }, 'brfs');
    b.transform({
        global: true
    }, 'browserify-shim');

    var stream = b.bundle();
    return stream.on('error', onError(function() {
            stream.end();
        })).pipe(source(filename))
        .pipe(gulpif(!developing, streamify(uglify({
            preserveComments: 'some'
        }))));
}

function onError(fn) {
    return function(err) {
        console.error(err);
        notify({
            title: 'Error',
            subtitle: 'fail to compiling scripts',
            text: err,
            sound: 'Bottle'
        });

        if (fn) {
            fn.call(err);
        }
    }
}

gulp.task("less", function() {
    return gulp.src("backend/client/less/*.less")
        .pipe(less({
            compress: true,
            paths: ["assets", "assets/components", "assets/less"]
            }))
        .on("error", console.error)
        .pipe(gulp.dest("assets/css/backend"));
});

gulp.task('login', function() {
	return browserifyStream("./backend/client/js/login.js", "login.js")
        .pipe(gulp.dest('assets/js/backend'));

});

gulp.task('scripts', function() {
    var fetch = browserifyStream("./backend/client/js/fetch.js", "fetch.js")
        .pipe(gulp.dest('assets/js/backend'));

    return merge(fetch);
});

gulp.task('images', function() {
    return gulp.src("assets/res/*")
        .pipe(changed('assets/images'))
        .pipe(gulpif(/.*\.png$/, tinypng('9kl3nT2f8qC-AaApBVXDeQt-37ArLMNs')))
        .pipe(gulp.dest('assets/images/'));
});

