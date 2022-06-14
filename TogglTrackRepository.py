# go to https://track.toggl.com/profile on the section "API token" you can get yours
# Get workspace id
# curl -v -u API_TOKEN:api_token -X GET https://api.track.toggl.com/api/v8/workspaces
# other way to get workspace id is going into reports section on the web. In the URL
# after the summary you will see the ID
# https://track.toggl.com/reports/summary/WORKSPACE_ID/period/thisMonth


# Common and basic parameters for request
# https://github.com/toggl/toggl_api_docs/blob/master/reports.md#request-parameters

# Detailed report docs
# https://github.com/toggl/toggl_api_docs/blob/master/reports/detailed.md

# sample request
# curl -v -u MY_API_TOKEN:api_token -X GET "https://api.track.toggl.com/reports/api/v2/details?workspace_id=WOKSPACE_ID&since=2022-05-01&until=2022-06-01&user_agent=mail@some.domain"
