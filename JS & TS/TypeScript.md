# TypeScript

## Node.JS

### Set up

```bash
npm i typescript --save-dev
npm i @types/node --save-dev
npx tsc --init --rootDir src --outDir build \
	--esModuleInterop --resolveJsonModule --lib es6 \
	--module commonjs --allowJs true --noImplicitAny true
```

Add build command in `package.json`

```json
"scripts": {
  "build": "tsc"
}
```



## VS Code launch.json config

```json
{
            "type": "pwa-node",
            "request": "launch",
            "name": "Launch Program",
            "skipFiles": [
                "<node_internals>/**"
            ],
            "program": "${workspaceFolder}/src/index.ts",
            "preLaunchTask": "tsc: build - tsconfig.json",
            "outFiles": [
                "${workspaceFolder}/dist/**/*.js"
            ],
            "outputCapture": "std"
        },
```

## Cold reload with nodemon

Install `nodemon` and `ts-node`.

```bash
npm i --save-dev ts-node nodemon
```



## Jest

### Set up TypeScript tests with ESModules

1. Install Jest and bindings

   ```bash
   npm i --save-dev jest ts-jest @types/jest
   ```

2. Generate Jest config

   ```bash
   npx ts-jest config:init
   ```

   1. Add `build` and `test` scripts to `package.json`


   ```json
   "scripts": {
       "build": "tsc",
       "test": "jest"
     }
   ```

3. Create tests e.g. under `tests` folder with filenames in format `*.test.ts`

4. Run tests

   ```bash
   npm test
   ```

### VS Code launch config for debugging tests

```json
{
      "name": "Debug Jest Tests",
      "type": "node",
      "runtimeVersion": "16.14.0",
      "request": "launch",
      "runtimeArgs": [
        "--inspect-brk",
        "${workspaceRoot}/node_modules/.bin/jest",
        "--runInBand"
      ],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    }
```

## Express

### Request object typing

```typescript
interface e.Request<P = ParamsDictionary, ResBody = any, ReqBody = any, ReqQuery = QueryString.ParsedQs, Locals extends Record<string, any> = Record<string, any>>
```

## Keyof, typeof

### Create a type from an object's keys

```typescript
const person = {
  name: 'Bobby Hadz',
  age: 30,
  country: 'Chile',
};

// 👇️ type Keys = "name" | "age" | "country"
type Keys = keyof typeof person;

```

