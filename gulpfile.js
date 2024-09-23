// Copyright (C) 2024 jmh
// SPDX-License-Identifier: GPL-3.0-only

"use strict";

import gulp from "gulp";
import environments from "gulp-environments";

import gulpSass from "gulp-sass"
import * as dartSass from "sass";
import cleanCSS from "gulp-clean-css"
import autoprefixer from "gulp-autoprefixer";

import babel from "gulp-babel";
import terser from "gulp-terser"
import {createGulpEsbuild} from "gulp-esbuild";

const esbuild = createGulpEsbuild({
    incremental: false,
    piping: true
});

const sass = gulpSass(dartSass);

const development = environments.development;
const production = environments.production;

const paths = {
    js: {
        src: "./js/**/*.js",
        watch: "./js/**/*.js",
        dest: "./stratum/static/dist/"
    },
    scss: {
        entrypoints: ["./scss/main.scss"],
        watch: ["./scss/*.scss", "./scss/**/*.scss"],
        dest: "./stratum/static/dist/"
    }
};

function scss() {
    return gulp.src(paths.scss.entrypoints)
        .pipe(sass.sync({
            outputStyle: production() ? "compressed" : "expanded",
            sourceMap: development()
        })
        .on("error", sass.logError))
        .pipe(autoprefixer({
            overrideBrowsersList: ["last 2 versions"],
            cascade: false
        }))
        .pipe(cleanCSS({
            level: {
                1: {
                    all: production(),
                    specialComments: 0
                }
            }
        }))
        .pipe(gulp.dest(paths.scss.dest));
}

function js() {
    return gulp.src(paths.js.src)
        .pipe(babel({
            presets: ["@babel/env"]
        }))
        .pipe(esbuild({
            entryNames: "[dir]",
            bundle: true,
            treeShaking: production(),
            legalComments: "none"
        }))
        .pipe(terser({
            mangle: {
                toplevel: true
            }
        }))
        .pipe(gulp.dest(paths.js.dest));
}

function watch() {
    gulp.watch(paths.scss.watch, scss);
    gulp.watch(paths.js.watch, js);
}

gulp.task("default", gulp.series(gulp.parallel(scss, js), watch));
gulp.task("build", gulp.parallel(scss, js));
