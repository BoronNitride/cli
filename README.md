# Data Contract CLI

<p>
  <a href="https://github.com/datacontract/cli/actions/workflows/ci.yaml?query=branch%3Amain">
    <img alt="Test Workflow" src="https://img.shields.io/github/actions/workflow/status/datacontract/cli/ci.yaml?branch=main"></a>
  <a href="https://img.shields.io/github/stars/datacontract/cli">
    <img alt="Stars" src="https://img.shields.io/github/stars/datacontract/cli" /></a>
</p>

The `datacontract` CLI is an open source command-line tool for working with [Data Contracts](https://datacontract.com/).
It uses data contract YAML files to lint the data contract, connect to data sources and execute schema and quality tests, detect breaking changes, and export to different formats. The tool is written in Python. It can be used as a standalone CLI tool, in a CI/CD pipeline, or directly as a Python library.

> **_NOTE:_**  This project has been migrated from Go to Python which adds the possibility to use `datacontract` within Python code as library, but it comes with some [breaking changes](CHANGELOG.md). The Go version has been [forked](https://github.com/datacontract/cli-go), if you still rely on that.


## Getting started

Let's use [pip](https://pip.pypa.io/en/stable/getting-started/) to install the CLI.
```bash
$ pip3 install datacontract-cli
```

Now, let's look at this data contract:
[https://datacontract.com/examples/covid-cases/datacontract.yaml](https://datacontract.com/examples/covid-cases/datacontract.yaml)

We have a _servers_ section with endpoint details to the (public) S3 bucket, _models_ for the structure of the data, and _quality_ attributes that describe the expected freshness and number of rows.

This data contract contains all information to connect to S3 and check that the actual data meets the defined schema and quality requirements.

We run the tests:

```bash
$ datacontract test https://datacontract.com/examples/covid-cases/datacontract.yaml
# returns: 🟢 data contract is valid. Run 12 checks.
```

Voilà, the CLI tested that the _datacontract.yaml_ itself is valid, all records comply with the schema, and all quality attributes are met.

## Usage

```bash
# create a new data contract from example and write it to datacontract.yaml
$ datacontract init datacontract.yaml

# lint the datacontract.yaml
$ datacontract lint datacontract.yaml

# execute schema and quality checks
$ datacontract test datacontract.yaml

# find differences between to data contracts (Coming Soon)
$ datacontract diff datacontract-v1.yaml datacontract-v2.yaml

# fail pipeline on breaking changes  (Coming Soon)
$ datacontract breaking datacontract-v1.yaml datacontract-v2.yaml

# export model as jsonschema
$ datacontract export --format jsonschema datacontract.yaml

# export model as dbt
$ datacontract export --format dbt datacontract.yaml

# import protobuf as model (Coming Soon)
$ datacontract import --format protobuf --source my_protobuf_file.proto datacontract.yaml
```

## Programmatic (Python)
```python
from datacontract.data_contract import DataContract

data_contract = DataContract(data_contract_file="datacontract.yaml")
run = data_contract.test()
if not run.has_passed():
    print("Data quality validation failed.")
    # Abort pipeline, alert, or take corrective actions...
```

## Scenario: Integration with Data Mesh Manager

If you use [Data Mesh Manager](https://datamesh-manager.com/), you can use the data contract URL and append the `--publish` option to send and display the test results. Set an environment variable for your API key.

```bash
# Fetch current data contract, execute tests on production, and publish result to data mesh manager
$ EXPORT DATAMESH_MANAGER_API_KEY=xxx
$ datacontract test https://demo.datamesh-manager.com/demo279750347121/datacontracts/4df9d6ee-e55d-4088-9598-b635b2fdcbbc/datacontract.yaml --server production --publish
```





## Installation

Choose the most appropriate installation method for your needs:

### pip
Python 3.11 recommended.
Python 3.12 available as pre-release release candidate for 0.9.3

```bash
pip3 install datacontract-cli
```

### pipx
pipx installs into an isolated environment.
```bash
pipx install datacontract-cli
```

### Docker

```bash
docker pull --platform linux/amd64 datacontract/cli
docker run --rm --platform linux/amd64 -v ${PWD}:/home/datacontract datacontract/cli
```

Or via an alias that automatically uses the latest version:

```bash
alias datacontract='docker run --rm -v "${PWD}:/home/datacontract" --platform linux/amd64 datacontract/cli:latest'
```

## Documentation

### Tests

Data Contract CLI can connect to data sources and run schema and quality tests to verify that the data contract is valid.

```bash
$ datacontract test --server production datacontract.yaml
```

To connect to the databases the `server` block in the datacontract.yaml is used to set up the connection. In addition, credentials, such as username and passwords, may be defined with environment variables.

The application uses different engines, based on the server `type`.

| Type         | Format     | Description                                                               | Status      | Engines                             |
|--------------|------------|---------------------------------------------------------------------------|-------------|-------------------------------------|
| `s3`         | `parquet`  | Works for any S3-compliant endpoint., e.g., AWS S3, GCS, MinIO, Ceph, ... | ✅           | soda-core-duckdb                    |
| `s3`         | `json`     | Support for `new_line` delimited JSON files and one JSON record per file. | ✅           | fastjsonschema<br> soda-core-duckdb |
| `s3`         | `csv`      |                                                                           | ✅           | soda-core-duckdb                    |
| `s3`         | `delta`    |                                                                           | Coming soon | TBD                                 |
| `postgres`   | n/a        |                                                                           | Coming soon | TBD                                 |
| `snowflake`  | n/a        |                                                                           | ✅           | soda-core-snowflake                 |
| `bigquery`   | n/a        |                                                                           | ✅           | soda-core-bigquery                  |
| `redshift`   | n/a        |                                                                           | Coming soon | TBD                                 |
| `databricks` | n/a        | Support for Databricks SQL with Unity catalog and Hive metastore.         | ✅           | soda-core-spark                     |
| `databricks` | n/a        | Support for Spark for programmatic use in Notebooks.                      | ✅           | soda-core-spark                     |
| `kafka`      | `json`     |                                                                           | Coming soon | TBD                                 |
| `kafka`      | `avro`     |                                                                           | Coming soon | TBD                                 |
| `kafka`      | `protobuf` |                                                                           | Coming soon | TBD                                 |
| `local`      | `parquet`  |                                                                           | ✅           | soda-core-duckdb                    |
| `local`      | `json`     | Support for `new_line` delimited JSON files and one JSON record per file. | ✅           | fastjsonschema<br> soda-core-duckdb |
| `local`      | `csv`      |                                                                           | ✅           | soda-core-duckdb                    |

Feel free to create an issue, if you need support for an additional type.

### Server Type S3

Data Contract CLI can test data that is stored in S3 buckets or any S3-compliant endpoints in various formats.

#### Example

datacontract.yaml
```yaml
servers:
  production:
    type: s3
    endpointUrl: https://minio.example.com # not needed with AWS S3
    location: s3://bucket-name/path/*/*.json
    format: json
    delimiter: new_line # new_line, array, or none
```

#### Environment Variables

| Environment Variable              | Example                       | Description           |
|-----------------------------------|-------------------------------|-----------------------|
| `DATACONTRACT_S3_REGION`            | `eu-central-1`                  | Region of S3 bucket   |
| `DATACONTRACT_S3_ACCESS_KEY_ID`     | `AKIAXV5Q5QABCDEFGH`            | AWS Access Key ID     |
| `DATACONTRACT_S3_SECRET_ACCESS_KEY` | `93S7LRrJcqLaaaa/XXXXXXXXXXXXX` | AWS Secret Access Key |


### Server Type BigQuery

We support authentication to BigQuery using Service Account Key. The used Service Account should include the roles:
* BigQuery Job User
* BigQuery Data Viewer


#### Example

datacontract.yaml
```yaml
servers:
  production:
    type: bigquery
    project: datameshexample-product
    dataset: datacontract_cli_test_dataset
models:
  datacontract_cli_test_table: # corresponds to a BigQuery table
    type: table
    fields: ...
```

#### Environment Variables

| Environment Variable                         | Example                   | Description                                             |
|----------------------------------------------|---------------------------|---------------------------------------------------------|
| `DATACONTRACT_BIGQUERY_ACCOUNT_INFO_JSON_PATH` | `~/service-access-key.json` | Service Access key as saved on key creation by BigQuery |


### Server Type Databricks

Works with Unity Catalog and Hive metastore.

Needs a running SQL warehouse or compute cluster.

#### Example

datacontract.yaml
```yaml
servers:
  production:
    type: databricks
    host: dbc-abcdefgh-1234.cloud.databricks.com
    catalog: acme_catalog_prod
    schema: orders_latest
models:
  orders: # corresponds to a table
    type: table
    fields: ...
```

#### Environment Variables

| Environment Variable                         | Example                              | Description                                           |
|----------------------------------------------|--------------------------------------|-------------------------------------------------------|
| `DATACONTRACT_DATABRICKS_TOKEN` | `dapia00000000000000000000000000000` | The personal access token to authenticate             |
| `DATACONTRACT_DATABRICKS_HTTP_PATH` | `/sql/1.0/warehouses/b053a3ffffffff` | The HTTP path to the SQL warehouse or compute cluster |


### Server Type Databricks (programmatic)

Works with Unity Catalog and Hive metastore.
When running in a notebook or pipeline, the provided `spark` session can be used.
An additional authentication is not required.

Requires a Databricks Runtime with Python >= 3.10.

#### Example

datacontract.yaml
```yaml
servers:
  production:
    type: databricks
    host: dbc-abcdefgh-1234.cloud.databricks.com # ignored, always use current host
    catalog: acme_catalog_prod
    schema: orders_latest
models:
  orders: # corresponds to a table
    type: table
    fields: ...
```

Notebook
```python
%pip install git+https://github.com/datacontract/cli.git
dbutils.library.restartPython()

from datacontract.data_contract import DataContract

data_contract = DataContract(
  data_contract_file="/Volumes/acme_catalog_prod/orders_latest/datacontract/datacontract.yaml", 
  spark=spark)
run = data_contract.test()
run.result
```


### Exports

Available export options:

| Type         | Description                                    | Status |
|--------------|------------------------------------------------|--------|
| `jsonschema` | Export to JSON Schema                          | ✅      | 
| `sodacl`     | Export to SodaCL quality checks in YAML format | ✅      |
| `dbt`        | Export to dbt model in YAML format             | ✅      |
| `avro`       | Export to AVRO models                          | TBD    |
| `pydantic`   | Export to pydantic models                      | TBD    |
| `sql`        | Export to SQL DDL                              | TBD    |
| `protobuf`   | Export to Protobuf                             | TBD    |

## Development Setup

Python base interpreter should be 3.11.x (unless
working on 3.12 release candidate).

```bash
# create venv
python3 -m venv venv
source venv/bin/activate

# Install Requirements
pip install --upgrade pip setuptools wheel
pip install -e '.[dev]'
cd tests/
pytest
```

Release

```
git tag v0.9.0
git push origin v0.9.0
python3 -m pip install --upgrade build twine
rm -r dist/
python3 -m build
# for now only test.pypi.org
python3 -m twine upload --repository testpypi dist/*
```

Docker Build

```
docker build -t datacontract/cli .
docker run --rm -v ${PWD}:/home/datacontract datacontract/cli
```

## Contribution

We are happy to receive your contributions. Propose your change in an issue or directly create a pull request with your improvements.

## License

[MIT License](LICENSE)

## Credits

Created by [Stefan Negele](https://www.linkedin.com/in/stefan-negele-573153112/) and [Jochen Christ](https://www.linkedin.com/in/jochenchrist/).
