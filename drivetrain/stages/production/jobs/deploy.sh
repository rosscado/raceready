#!/bin/bash
# deploy a cloud foundry app

cf delete -r -f "${CF_APP}"
cf push "${CF_APP}"
# View logs
# cf logs "${CF_APP}" --recent
