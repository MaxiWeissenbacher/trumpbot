#!/usr/bin/env node

import { App } from "aws-cdk-lib";
import { TrumpbotbackendStack } from "../lib/trumpbotbackend-stack.js";

const app = new App();
new TrumpbotbackendStack(app, "TrumpbotbackendStack", {
  env: { account: "045308209786", region: "eu-central-1" },
});
