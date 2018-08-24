#!/bin/bash

cf push -n "staging-${CF_APP}" "${CF_APP}"
# View logs
# cf logs "${CF_APP}" --recent
