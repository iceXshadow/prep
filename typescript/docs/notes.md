# Notes

- ts can't be executed directly, it has to be converted to js code to run it.
- create new project using `npm init -y`
- install ts as dev dependency with `npm i typescript --save-dev`
- create config file with `npx tsc --init`
- we first compile ts code and then exe the js file for output
- `tsc test.ts` and `node test.js`
- setup new vite project with ts template

## The TSCONFIG.json file

- target (the target version of js that we will get after compiling ts code.)
- module (commonjs, es6/esNext)
- 