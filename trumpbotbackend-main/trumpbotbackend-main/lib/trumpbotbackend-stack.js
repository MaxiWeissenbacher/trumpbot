import { Stack, Duration } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import {
  Cors,
  Deployment,
  EndpointType,
  LambdaIntegration,
  LambdaRestApi,
  Stage,
} from "aws-cdk-lib/aws-apigateway";
import { resolve } from "path";

export class TrumpbotbackendStack extends Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    const lambda = new Function(this, "TrumpbotLambda", {
      runtime: Runtime.PYTHON_3_8,
      memorySize: 512,
      timeout: Duration.seconds(10),
      handler: "handler.handler",
      code: Code.fromAsset(resolve("./src/lambda")),
    });

    const api = new LambdaRestApi(this, "TrumpbotGateway", {
      restApiName: "Trumpbot Gateway",
      description: "This service handles API Calls from Trumpbot Frontend",
      handler: lambda,
      endpointConfiguration: {
        types: [EndpointType.REGIONAL],
      },
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["POST", "OPTIONS"],
      },
      proxy: false,
    });

    const endpoint = api.root.addMethod("POST", new LambdaIntegration(lambda), {
      apiKeyRequired: false,
    });

    const deployment = new Deployment(this, "TrumpbotDeployment", {
      api: api,
    });

    const stage = new Stage(this, "TrumpbotStage", {
      deployment: deployment,
      throttlingBurstLimit: 5,
      throttlingRateLimit: 10,
    });
  }
}
