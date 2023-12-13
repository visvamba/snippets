# AWS Lambda

## Creating Lambda container image

### Node.JS

Use AWS Lambda base image and add your code e.g.

```dockerfile
FROM public.ecr.aws/lambda/nodejs:14
# Alternatively, you can pull the base image from Docker Hub: amazon/aws-lambda-nodejs:12

# Assumes your function is named "app.js", and there is a package.json file in the app directory 
COPY app.js package.json  ${LAMBDA_TASK_ROOT}

# Install NPM dependencies for function
RUN npm install

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]  
```

Build the Docker iamge

```bash
docker build -t <image_name> .
```

### Deploying the image

1. Authenticate Docker CLI to Amazon ECR registry

   ```bash
   aws ecr --profile <profile> get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <account-num>.dkr.ecr.ap-southeast-1.amazonaws.com
   ```

2. Create repo if necessary

   ```bash
   aws ecr --profile <profile> create-repository --repository-name <repo-name> --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
   ```

3. Tag image to match repo name

   ```bash
   docker tag <image-name>:latest <account-num>.dkr.ecr.ap-southeast-1.amazonaws.com/<image-name>:latest
   ```

4. Push image to repo

   ```bash
   docker push <image-name>:latest <account-num>.dkr.ecr.ap-southeast-1.amazonaws.com/<image-name>:latest
   ```

   

### Testing images

```bash
docker run -p 9000:8080 <image_name>:latest
```

## TypeScript

### Initialise TypeScript Project

1. Set up NPM packages - Lambda types and esbuild
   ```bash
   npm init
   npm i -D @types/node @types/aws-lambda esbuild
   ```

2. Create `index.ts` file e.g.:
   ```typescript
   import { Context, APIGatewayProxyResult, APIGatewayEvent } from 'aws-lambda';
   
   export const handler = async (event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> => {
     console.log(`Event: ${JSON.stringify(event, null, 2)}`);
     console.log(`Context: ${JSON.stringify(context, null, 2)}`);
     return {
         statusCode: 200,
         body: JSON.stringify({
             message: 'hello world',
         }),
      };
   };
   ```

3. Add build scripts to `package.json`. Only index.ts needs to be specified as it is the only entrypoint to the code.
   ```json
     "scripts": {
     "prebuild": "rm -rf dist",
     "build": "esbuild index.ts --bundle --minify --sourcemap --platform=node --target=es2020 --outfile=dist/index.js",
     "postbuild": "cd dist && zip -r index.zip index.js*"
   },
   ```

4. Build
   ```bash
   npm run build
   ```

   

### AWS API Gateway event types

1. Install types
   ```bash
   npm i --save-dev @types/aws-lambda
   ```

2. Import
  ```typescript
  import { 
    APIGatewayProxyEvent, 
    APIGatewayProxyResult } 
  from "aws-lambda/trigger/api-gateway-proxy";
  ```

### Sample code

```typescript
export const lambdaHandler = async (
   event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const queries = JSON.stringify(event.queryStringParameters);
  return {
    statusCode: 200,
    body: `Queries: ${queries}`
  }
```

