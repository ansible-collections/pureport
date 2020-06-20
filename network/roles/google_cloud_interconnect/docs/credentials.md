# Configuring Credentials

In order for this role to execute properly, it requires service account and/or
API credentials to be provided for both Google Cloud and Pureport.  Currently
this role uses credentials set as environment variables.  

The following environment variables are required to be set in order for this 
role to work properly.

| Name                       | Description                                                               |
| -------------------------- | ------------------------------------------------------------------------- |
| `GCP_SERVICE_ACCOUNT_FILE` | The full path to the Google Cloud service account JSON file               |
| `GCP_AUTH_KIND`            | Currently only `serviceaccount` is supported in this role                 |
| `GCP_PROJECT`              | The name of the Google Cloud project where the connection should be built |
| `PUREPORT_API_KEY`         | The API key value created in the Pureport Console                         |
| `PUREPORT_API_SECRET`      | The API secret value from the Pureport Console                            |
| `PUREPORT_ACCOUNT_ID`      | The Pureport account ID for this connection (usually starts with `ac-`)   |

## Example

```bash
export GCP_SERVICE_ACCOUNT_FILE=<path to service account JSON>
export GCP_AUTH_KIND=serviceaccount
export GCP_PROJECT=XXXXXX
export PUREPORT_API_KEY=XXXXXX
export PUREPORT_API_SECRET=XXXXXX
export PUREPORT_ACCOUNT_ID=XXXXXX
```

