#!/bin/bash
# deploy a cloud foundry app

#cf delete -r -f "${CF_APP}"
cf push -n "${CF_APP}" "${CF_APP}"
# View logs
# cf logs "${CF_APP}" --recent
