# Node.JS

## Initialising a project

```bash
npm init
npx gitignore node 
```

## Using an environment file

```bash
npm install dotenv
```

Then create .env file.

```bash
HOSTNAME=www.google.com
```

Usage:

```javascript
require('dotenv').config()

hostname = process.env.HOSTNAME
```

## Filesystem

### Read JSON file into object

```javascript
import { readFileSync }from 'fs'

let rawdata = readFileSync('data.json')
let jsonObj = JSON.parse(rawdata)
```



## Streams

### Wait for stream to finish piping

```javascript
function readStream(stream) {

  return new Promise((resolve, reject) => {
      let data = "";
      
      stream.on("data", chunk => data += chunk);
      stream.on("end", () => resolve(data));
      stream.on("error", error => reject(error));
  });
}

var streamA = createAStreamSomehow()
var streamB = createAStreamSomehow()
var result = await readStream(streamA.pipe(streamB))
```

## Dates

## Random numbers

```javascript
function getRandomFloat(min, max, decimals) {
  const str = (Math.random() * (max - min) + min).toFixed(decimals);

  return parseFloat(str);
}
```

## Testing - Jest

### Set up TypeScript tests

1. Install Jest and bindings
   ```bash
   npm i --save-dev jest ts-jest @types/jest
   ```

2. Generate Jest config
   ```bash
   npx ts-jest config:init
   ```

3. Add `build` and `test` scripts to `package.json`
   ```json
   "scripts": {
       "build": "tsc",
       "test": "jest"
     }
   ```

4. Create tests e.g. under `tests` folder with filenames in format `*.test.ts`

5. Run tests
   ```bash
   npm test
   ```

   
